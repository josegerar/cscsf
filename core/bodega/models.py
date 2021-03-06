from django.db import models

from core.base.models import BaseModel
from core.login.models import User


class Bodega(BaseModel):
    nombre = models.CharField(max_length=20, verbose_name="Nombre")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción", blank=True, null=True)
    direccion = models.CharField(max_length=200, verbose_name="Direccion", blank=True, null=True)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Responsable", null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Bodega"
        verbose_name_plural = "Bodegas"
        db_table = "bodega"
        ordering = ["id"]
