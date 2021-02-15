from django.db import models
from django.forms import model_to_dict
from django.utils import timezone

from core.login.models import User, BaseModel


class Laboratorio(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de laboratorio", unique=True)
    fecha_creacion = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self, exclude=[])
        return item

    class Meta:
        verbose_name = "Laboratorio"
        verbose_name_plural = "Laboratorios"
        db_table = "laboratorio"
        ordering = ["id"]


class TecnicoLaboratorio(BaseModel):
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(default=timezone.now, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.tecnico.first_name + " - " + self.laboratorio.nombre

    class Meta:
        verbose_name = "TecnicoLaboratorio"
        verbose_name_plural = "TecnicosLaboratorios"
        db_table = "tecnico_laboratorio"
        ordering = ["id"]
