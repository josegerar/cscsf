from django.utils.translation import gettext, gettext_lazy as _

from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import *

from core.representantetecnico.models import User


class CustomUserCreationForm(UserCreationForm):
    cedula = CharField(
        label=_("Cedula"),
        strip=False,
        widget=NumberInput(attrs={'minlength': 10, 'maxlength': 10}),
        help_text="Requerido, maximo 10 caracteres, minimo 10 caracteres",
    )

    class Meta(UserCreationForm.Meta):
        model = User