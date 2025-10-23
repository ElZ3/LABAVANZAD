from django.db import models

class Rol(models.Model):
        """
        Define los roles del sistema. Ahora vive en su propia app.
        """
        ESTADO_CHOICES = [
            ('Activo', 'Activo'),
            ('Inactivo', 'Inactivo'),
        ]

        nombre = models.CharField(max_length=50, unique=True, blank=False)
        descripcion = models.TextField(blank=False)
        estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)

        def __str__(self):
            return self.nombre

        class Meta:
            verbose_name = "Rol"
            verbose_name_plural = "Roles"
            ordering = ['nombre']
    
