from django.contrib.auth.models import AbstractUser, Group
from django.db import models
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

    # Obtenemos los perfiles de cada usuario acorde a su tipo
    def get_representative_profile(self):
        representative_profile = None
        if hasattr(self, 'representativeprofile'):
            representative_profile = self.representativeprofile
        return representative_profile

    def get_laboratory_worker_profile(self):
        laboratory_worker_profile = None
        if hasattr(self, 'laboratoryworkerprofile'):
            laboratory_worker_profile = self.laboratoryworkerprofile
        return laboratory_worker_profile

    def get_grocer_profile(self):
        grocer_profile = None
        if hasattr(self, 'grocerprofile'):
            grocer_profile = self.grocerprofile
        return grocer_profile

    def get_imagen(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        else:
            return '{}{}'.format(STATIC_URL, 'img/user.png')

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "auth_user"
        ordering = ["id"]


class RepresentativeProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name_profile = models.CharField(max_length=64, default="representante tecnico")

    def __str__(self):
        return self.name_profile

    class Meta:
        verbose_name = "Represente tecnico Perfil"
        verbose_name_plural = "Represente tecnico Perfiles"
        db_table = "representative_technical_profile"
        ordering = ["id"]


class LaboratoryWorkerProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name_profile = models.CharField(max_length=64, default="tecnico laboratorista")

    def __str__(self):
        return self.name_profile

    class Meta:
        verbose_name = "Tecnico laboratorista Perfil"
        verbose_name_plural = "Tecnico laboratorista Perfiles"
        db_table = "laboratory_worker_profile"
        ordering = ["id"]


class GrocerProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    name_profile = models.CharField(max_length=64, default="bodeguero")

    def __str__(self):
        return self.name_profile

    class Meta:
        verbose_name = "Bodeguero Perfil"
        verbose_name_plural = "Bodeguero Perfiles"
        db_table = "grocer_profile"
        ordering = ["id"]
