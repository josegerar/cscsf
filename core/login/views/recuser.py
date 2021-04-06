from django.conf import settings
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import TemplateView


class recuperaruser(TemplateView):
    template_name = "recuperarusuario.html"