from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from core.login.forms.customUserChangeForm import CustomUserChangeForm
from core.login.forms.customUserCreationForm import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'is_representative', 'is_laboratory_worker', 'is_grocer',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        (_('Roles'), {
            'fields': ('is_representative', 'is_laboratory_worker', 'is_grocer'),
        }),
    )
