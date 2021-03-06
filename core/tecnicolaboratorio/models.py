from django.db import models

from core.login.models import User, BaseModel


class Laboratorio(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombre de laboratorio", unique=True)
    direccion = models.CharField(max_length=300, null=True, blank=True, verbose_name="Dirección")
    responsable = models.ForeignKey(User, verbose_name="Responsable", on_delete=models.CASCADE,
                                    related_name="responsable", null=True, blank=True)

    def __str__(self):
        return self.nombre

    @staticmethod
    def get_choices_laboratory_user(user_id):
        choices = [('', '---------')]
        choices += [(o.id, o.nombre) for o in Laboratorio.objects.filter(responsable_id=user_id)]
        return choices

    class Meta:
        verbose_name = "Laboratorio"
        verbose_name_plural = "Laboratorios"
        db_table = "laboratorio"
        ordering = ["id"]
