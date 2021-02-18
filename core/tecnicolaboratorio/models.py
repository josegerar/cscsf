from django.db import models
from django.forms import model_to_dict
from django.utils import timezone

from core.login.models import User, BaseModel


class Laboratorio(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de laboratorio", unique=True)
    responsable = models.ForeignKey(User, verbose_name="Responsable", on_delete=models.CASCADE,
                                    related_name="responsable", null=True, blank=True)

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = {'id': self.id, 'nombre': self.nombre,
                'responsable': '{} {} {}'.format(str(self.responsable.first_name), str(self.responsable.last_name),
                                                 str(self.responsable.cedula))}
        return item

    class Meta:
        verbose_name = "Laboratorio"
        verbose_name_plural = "Laboratorios"
        db_table = "laboratorio"
        ordering = ["id"]
