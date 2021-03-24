from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _

from app.settings import MEDIA_URL, STATIC_URL
from core.base.models import BaseModel


class Persona(BaseModel):
    nombre = models.CharField(max_length=100, verbose_name="Nombres", default="")
    apellido = models.CharField(max_length=100, verbose_name="Apellidos")
    cedula = models.CharField(max_length=10, verbose_name="Cedula", unique=True)
    telefono = models.CharField(max_length=10, verbose_name="Telefono", null=True, blank=True)
    imagen = models.ImageField(upload_to="users/%Y/%m/%d", null=True, blank=True)
    is_active = models.BooleanField(default=True, editable=False)

    def __str__(self):
        return self.nombre + " " + self.apellido

    def toJSON(self):
        item = model_to_dict(self, exclude=['imagen'])
        item['imagen'] = self.get_imagen()
        return item

    def get_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        else:
            return '{}{}'.format(STATIC_URL, 'img/user.png')

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        db_table = "persona"
        ordering = ["id"]


class User(AbstractUser, BaseModel):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name="Persona", null=True)
    is_representative = models.BooleanField(
        _('Es representante técnico'),
        default=False,
        help_text=_('Indica si el usuario es Representante tecnico')
    )
    is_laboratory_worker = models.BooleanField(
        _('Es tecnico de laboratorio'),
        default=False,
        help_text=_('Indica si el usuario es Técnico de laboratorio')
    )
    is_grocer = models.BooleanField(
        _('Es bodegero'),
        default=False,
        help_text=_('Indica si el usuario es Bodeguero')
    )

    def __str__(self):
        return self.username

    def toJSON(self):
        return model_to_dict(self, exclude=['imagen', 'groups'])

    @staticmethod
    def get_choices_user():
        choices = [('', '---------')]
        choices += [(o.id, o.get_user_info()) for o in User.objects.all()]
        return choices

    @staticmethod
    def get_choices_laboratory_worker():
        choices = [('', '---------')]
        choices += [(o.id, o.get_user_info()) for o in User.objects.filter(is_laboratory_worker=True)]
        return choices

    @staticmethod
    def get_choices_grocer():
        choices = [('', '---------')]
        choices += [(o.id, o.get_user_info()) for o in User.objects.filter(is_grocer=True)]
        return choices

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        group = None
        if self.is_grocer is True:
            group = Group.objects.get(name__iexact='bodega')
        elif self.is_laboratory_worker is True:
            group = Group.objects.get(name__iexact='laboratorio')
        elif self.is_representative is True:
            group = Group.objects.get(name__iexact='representante')
        if group is not None:
            self.groups.add(group)

    def get_user_info(self):
        if self.persona is not None:
            return self.persona.__str__()
        else:
            return self.username

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "auth_user"
        ordering = ["id"]
