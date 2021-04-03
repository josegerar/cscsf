from datetime import datetime

from django.db import models
from django.db.models import Sum
from django.forms import model_to_dict

from core.login.models import BaseModel, User
from core.tecnicolaboratorio.models import Laboratorio


class Bodega(BaseModel):
    nombre = models.CharField(max_length=20, verbose_name="Nombre")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción", blank=True, null=True)
    direccion = models.CharField(max_length=200, verbose_name="Direccion", blank=True, null=True)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Responsable", null=True, blank=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['responsable'])
        if self.responsable is not None:
            item['responsable'] = self.responsable.get_user_info()
        return item

    class Meta:
        verbose_name = "Bodega"
        verbose_name_plural = "Bodegas"
        db_table = "bodega"
        ordering = ["id"]


class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=20, verbose_name="Nombre de unidad de medida")
    simbolo = models.CharField(max_length=5, verbose_name="Simbolo de la unidad de medida", null=True)
    descripcion = models.CharField(max_length=200, verbose_name="Descripción", blank=True,
                                   null=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = "Unidad de medida"
        verbose_name_plural = "Unidades de medida"
        db_table = "unidad_medida"
        ordering = ["id"]


class Sustancia(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de sustancia", unique=True)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE, verbose_name="Unidad de medida",
                                      null=True)
    descripcion = models.CharField(max_length=200, verbose_name="Descripción de la sustancia", blank=True,
                                   null=True)
    cupo_autorizado = models.DecimalField(default=0, verbose_name="Cupo autorizado", max_digits=9,
                                          decimal_places=4)

    def __str__(self):
        return self.nombre

    def get_cupo_consumido(self):
        cupo_consumido = Inventario.objects.filter(
            date_creation__year=datetime.now().year,
            tipo_movimiento__nombre="addcompra",
            stock__sustancia_id=self.id
        ).aggregate(Sum("cantidad_movimiento"))
        if cupo_consumido['cantidad_movimiento__sum'] is None:
            cupo_consumido['cantidad_movimiento__sum'] = 0
        return float(cupo_consumido['cantidad_movimiento__sum'])

    def toJSON(self, view_stock=False):
        item = {'id': self.id, 'nombre': self.nombre, 'descripcion': self.descripcion,
                'cupo_autorizado': self.cupo_autorizado, 'cupo_consumido': self.get_cupo_consumido()}
        if self.unidad_medida is not None:
            item['unidad_medida'] = self.unidad_medida.toJSON()
        item['stock'] = []
        if self.stock_set is not None:
            if view_stock is True:
                for i in self.stock_set.all():
                    item['stock'].append(i.toJSON(view_subtance=False))
        return item

    class Meta:
        verbose_name = "Sustancia"
        verbose_name_plural = "Sustancias"
        db_table = "sustancia"
        ordering = ["id"]


class Stock(BaseModel):
    sustancia = models.ForeignKey(Sustancia, on_delete=models.CASCADE, null=True)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, null=True)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, null=True)
    cantidad = models.DecimalField(max_digits=9, decimal_places=4, default=0)

    def __str__(self):
        return str(self.id)

    def toJSON(self, view_subtance=False, view_stock_substance=False):
        item = {'id': self.id, 'cantidad': self.cantidad}
        if self.bodega is not None:
            item['bodega'] = self.bodega.toJSON()
        if self.laboratorio is not None:
            item['laboratorio'] = self.laboratorio.toJSON()
        if self.sustancia is not None:
            if view_subtance is True:
                if view_stock_substance is False:
                    item['sustancia'] = self.sustancia.toJSON(view_stock=False)
                else:
                    item['sustancia'] = self.sustancia.toJSON(view_stock=True)

        return item

    class Meta:
        verbose_name = "Stock sustancia"
        verbose_name_plural = "Stock sustancias"
        db_table = "stock"
        ordering = ["id"]
