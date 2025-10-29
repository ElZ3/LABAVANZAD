from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    # Campos visibles en la lista de usuarios
    list_display = ('username', 'email', 'nombre', 'apellido', 'rol', 'estado', 'is_staff')
    list_filter = ('estado', 'is_staff', 'is_superuser', 'groups', 'rol')
    search_fields = ('username', 'nombre', 'apellido', 'email')
    ordering = ('username',)

    # Campos visibles al editar un usuario existente
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Información personal'), {'fields': ('nombre', 'apellido', 'email', 'dui', 'rol', 'estado')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    # Campos visibles al crear un nuevo usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'nombre', 'apellido', 'dui', 'rol', 'estado', 'password1', 'password2'),
        }),
<<<<<<< HEAD
    )
=======
    )
>>>>>>> backup-local
