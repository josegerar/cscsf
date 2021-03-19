from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _

from app.settings import MEDIA_URL, STATIC_URL
from core.base.models import BaseModel


class User(AbstractUser, BaseModel):
    cedula = models.CharField(max_length=10, verbose_name="Cedula", unique=True)
    telefono = models.CharField(max_length=10, verbose_name="Telefono", null=True, blank=True)
    imagen = models.ImageField(upload_to="users/%Y/%m/%d", null=True, blank=True)
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
        choices += [(o.id, str('{} {} {}'.format(str(o.first_name), str(o.last_name), str(o.cedula)))) for o in
                    User.objects.all()]
        return choices

    @staticmethod
    def get_choices_laboratory_worker():
        choices = [('', '---------')]
        choices += [(o.id, str('{} {} {}'.format(str(o.first_name), str(o.last_name), str(o.cedula)))) for o in
                    User.objects.filter(is_laboratory_worker=True)]
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

    def get_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        else:
            return '{}{}'.format(STATIC_URL, 'img/user.png')

    def get_user_info(self):
        return '{} {} {}'.format(str(self.first_name), str(self.last_name), str(self.cedula))

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "auth_user"
        ordering = ["id"]
