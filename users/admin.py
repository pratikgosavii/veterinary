from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import *  # Import your custom form

class CustomUserAdmin(UserAdmin):
   
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('mobile', 'email', 'is_staff', 'is_active', 'is_customer', 'is_doctor', 'is_daycare', 'is_service_provider')
    list_filter = ('is_staff', 'is_active', 'is_customer', 'is_doctor', 'is_service_provider')

    fieldsets = (
        (None, {'fields': ('mobile', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Roles', {'fields': ('is_customer', 'is_doctor', 'is_daycare', 'is_service_provider')}),
        ('Groups & Permissions', {'fields': ('groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('mobile',)
    ordering = ('mobile',)

admin.site.register(User, CustomUserAdmin)