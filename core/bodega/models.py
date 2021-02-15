from django.db import models
from django.utils import timezone

from core.login.models import BaseModel


class TipoPresentacion(BaseModel):
    nombre = models.CharField(max_length=10, verbose_name="Nombre de tipo de presentacion")
    descripcion = models.CharField(max_length=10, verbose_name="Descripción de tipo de presentacion")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "TipoPresentacion"
        verbose_name_plural = "TipoPresentaciones"
        db_table = "tipo_presentacion"
        ordering = ["id"]


class Sustancia(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de sustancia", unique=True)
    cantidad = models.IntegerField(default=0, verbose_name="Cantidad actal de sustancias")
    tipo_presentacion = models.ForeignKey(TipoPresentacion, on_delete=models.CASCADE,
                                          verbose_name="TIpo de presentacion")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Sustancia"
        verbose_name_plural = "Sustancias"
        db_table = "sustancia"
        ordering = ["id"]


class Inventario(BaseModel):
    sustancia = models.ForeignKey(Sustancia, on_delete=models.CASCADE, verbose_name="Sustancia")
    cantidad_movimiento = models.IntegerField(default=0, verbose_name="Cantidad movimiento")
    fecha_movimiento = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
        db_table = "inventario"
        ordering = ["id"]
