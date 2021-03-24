from django.utils.translation import gettext, gettext_lazy as _

from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import *

from core.representantetecnico.models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User