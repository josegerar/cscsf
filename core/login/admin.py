from django.contrib import admin

from core.login.models import User
from core.login.views.customUserAdmin import CustomUserAdmin


@admin.register(User)
class UserAdmin(CustomUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
