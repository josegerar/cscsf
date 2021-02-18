from django.contrib import admin

from core.login.models import GrocerProfile, LaboratoryWorkerProfile, RepresentativeProfile, User
from core.login.views.customUserAdmin import CustomUserAdmin


@admin.register(User)
class UserAdmin(CustomUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')


@admin.register(RepresentativeProfile)
class GrocerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name_profile',
        'active',
        'user_id'
    )


@admin.register(LaboratoryWorkerProfile)
class GrocerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name_profile',
        'active',
        'user_id'
    )


@admin.register(GrocerProfile)
class GrocerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name_profile',
        'active',
        'user_id'
    )
