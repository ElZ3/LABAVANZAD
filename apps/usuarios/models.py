from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator    
# Importación clave: Apuntamos al modelo Rol en la nueva app
from roles.models import Rol 

class Usuario(AbstractUser):
        """
        Modelo de usuario que ahora se relaciona con un modelo en otra app.
        """
        # ... (dui_validator, campos personalizados, etc. se mantienen igual) ...
        dui_validator = RegexValidator(
            regex=r'^\d{8}-\d{1}$',
            message="El DUI debe tener el formato 12345678-9."
        )
        first_name = None
        last_name = None
        email = models.EmailField(unique=True, blank=False, verbose_name="Correo Electrónico")
        nombre = models.CharField(max_length=100, blank=False)
        apellido = models.CharField(max_length=100, blank=False)
        dui = models.CharField(
            max_length=10, 
            unique=True, 
            blank=False, 
            validators=[dui_validator],
            verbose_name="DUI"
        )
        estado = models.CharField(
            max_length=20, 
            default='Activo', 
            choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')],
            blank=False
        )
        
        # La relación ahora apunta explícitamente a 'roles.Rol'
        rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True)

        USERNAME_FIELD = 'username'
        REQUIRED_FIELDS = ['email', 'nombre', 'apellido', 'dui']

        def __str__(self):
            return f"{self.nombre} {self.apellido} ({self.username})"

        def clean(self):
            if self.is_superuser:
                self.is_staff = True
                self.estado = 'Activo'
                try:
                    # La lógica para asignar el rol de Admin se mantiene
                    admin_rol = Rol.objects.get(nombre='Administrador')
                    self.rol = admin_rol
                except Rol.DoesNotExist:
                    pass
            super().clean()

        def save(self, *args, **kwargs):
            self.full_clean()
            super().save(*args, **kwargs)
    

