# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from cssf.models import *

admin.site.register(Categoria)
admin.site.register(Laboratorio)
admin.site.register(TipoPersona)
admin.site.register(User, UserAdmin)