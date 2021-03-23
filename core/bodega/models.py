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
            item['responsable'] = str(
                '{} {} {}'.format(str(self.responsable.first_name), str(self.responsable.last_name),
                                  str(self.responsable.cedula)))
        else:
            item['responsable'] = None
        return item

    class Meta:
        verbose_name = "Bodega"
        verbose_name_plural = "Bodegas"
        db_table = "bodega"
        ordering = ["id"]


class UnidadMedida(BaseModel):
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

    def toJSON(self, view_stock=False):
        item = {'id': self.id, 'nombre': self.nombre, 'descripcion': self.descripcion,
                'cupo_autorizado': self.cupo_autorizado}
        cupo_consumido = Inventario.objects.filter(
            date_creation__year=datetime.now().year,
            tipo_movimiento__nombre="add",
            stock__sustancia_id=self.id
        ).aggregate(Sum("cantidad_movimiento"))
        item['cupo_consumido'] = cupo_consumido;
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
    cantidad = models.DecimalField(max_digits=9, decimal_places=4)

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
                    item['sustancia'] = self.sustancia.toJSON()

        return item

    class Meta:
        verbose_name = "Stock sustancia"
        verbose_name_plural = "Stock sustancias"
        db_table = "stock"
        ordering = ["id"]


class TipoMovimientoInventario(BaseModel):
    nombre = models.CharField(max_length=20, verbose_name="Nombre", unique=True)
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion", blank=True, null=True)

    def __str__(self):
        return str(self.nombre)

    def toJSON(self):
        item = {'id': self.id, 'nombre': self.nombre, 'descripcion': self.descripcion}
        return item

    class Meta:
        verbose_name = "Tipo de movimiento de inventario"
        verbose_name_plural = "Tipos de movimientos de inventario"
        db_table = "tipo_movimiento_inventario"
        ordering = ["id"]


class Inventario(BaseModel):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name="Stock de sustancia", null=True)
    cantidad_movimiento = models.DecimalField(default=0, verbose_name="Cantidad movimiento", max_digits=9,
                                              decimal_places=4)
    tipo_movimiento = models.ForeignKey(TipoMovimientoInventario, on_delete=models.CASCADE,
                                        verbose_name="Tipo de movimiento de inventario", null=True)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = {'id': self.id, 'cantidad': self.cantidad_movimiento,
                'fecha': self.date_creation.strftime("%Y-%m-%d %H:%M:%S")}
        if self.stock is not None:
            item['stock'] = self.stock.toJSON(view_subtance=True, view_stock_substance=False)
        if self.tipo_movimiento is not None:
            item['tipo_movimiento'] = self.tipo_movimiento.toJSON()
        return item

    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        db_table = "inventario"
        ordering = ["id"]
