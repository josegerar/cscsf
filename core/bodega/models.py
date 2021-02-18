from django.db import models
from django.forms import model_to_dict
from django.utils import timezone

from core.login.models import BaseModel


class UnidadMedida(BaseModel):
    nombre = models.CharField(max_length=10, verbose_name="Nombre de unidad de medida")
    descripcion = models.CharField(max_length=10, verbose_name="Descripción", blank=True,
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


class TipoPresentacion(BaseModel):
    nombre = models.CharField(max_length=10, verbose_name="Nombre de tipo de presentacion")
    descripcion = models.CharField(max_length=10, verbose_name="Descripción de tipo de presentacion", blank=True,
                                   null=True)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE, verbose_name="Unidad de medida",
                                      null=True)
    volumen = models.DecimalField(default=0, verbose_name="Volumen", max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=['unidad_medida'])
        item['unidad_medida'] = self.unidad_medida.toJSON()
        return item

    class Meta:
        verbose_name = "Tipo de presentacion"
        verbose_name_plural = "Tipo de presentaciones"
        db_table = "tipo_presentacion"
        ordering = ["id"]


class Sustancia(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de sustancia", unique=True)
    descripcion = models.CharField(max_length=200, verbose_name="Descripción de la sustancia", blank=True,
                                   null=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        inv = {'id': self.id, 'nombre': self.nombre, 'descripcion': self.descripcion}
        return inv

    class Meta:
        verbose_name = "Sustancia"
        verbose_name_plural = "Sustancias"
        db_table = "sustancia"
        ordering = ["id"]


class StockSustancia(BaseModel):
    sustancia = models.ForeignKey(Sustancia, on_delete=models.CASCADE, verbose_name="Sustancia")
    cantidad = models.DecimalField(default=0, verbose_name="Cantidad presentacion", max_digits=9,
                                   decimal_places=4)
    presentacion = models.ForeignKey(TipoPresentacion, on_delete=models.CASCADE, verbose_name="Tipo de presentacion")

    def __str__(self):
        return '{} {} {}'.format(self.sustancia.nombre, self.cantidad, self.presentacion.nombre)

    def toJSON(self):
        inv = {'id': self.id, 'sustancia': self.sustancia.toJSON(), 'cantidad': self.cantidad,
               'presentacion': self.presentacion.toJSON()}
        return inv

    class Meta:
        verbose_name = "Stock de sustancia"
        verbose_name_plural = "Stock de sustancias"
        db_table = "stock_sustancia"
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
    sustancia_stock = models.ForeignKey(StockSustancia, on_delete=models.CASCADE, verbose_name="Stock de sustancia",
                                        null=True)
    cantidad_movimiento = models.DecimalField(default=0, verbose_name="Cantidad movimiento", max_digits=9,
                                              decimal_places=4)
    tipo_movimiento = models.ForeignKey(TipoMovimientoInventario, on_delete=models.CASCADE,
                                        verbose_name="Tipo de movimiento de inventario", null=True)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = {'id': self.id, 'sustancia_stock': self.sustancia_stock.toJSON(), 'cantidad': self.cantidad_movimiento,
                'tipo_movimiento': self.tipo_movimiento.toJSON()}
        return item

    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        db_table = "inventario"
        ordering = ["id"]
