from django.db import models
from django.core.exceptions import ValidationError

class Rol(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    rol_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True, blank=False)
    descripcion = models.TextField(blank=False)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)

    def __str__(self):
        return self.nombre

    # REGLAS DE NEGOCIO
    def puede_eliminarse(self):
        """Verifica si el rol puede ser eliminado"""
        return not hasattr(self, 'usuario_set') or not self.usuario_set.exists()

    def delete(self, *args, **kwargs):
        """Sobrescribir eliminación para aplicar reglas de negocio"""
        if not self.puede_eliminarse():
            raise ValidationError(
                f"No se puede eliminar el rol '{self.nombre}' porque está asignado a uno o más usuarios."
            )
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'Roles'
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ['rol_id']