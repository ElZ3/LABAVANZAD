from django.db import models
from django.core.exceptions import ValidationError # Importante

class CategoriaExamen(models.Model):
    
    categoria_id = models.AutoField(primary_key=True) 

    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True, blank=False)
    
    # REQUISITO: "ningun campo puede quedar vacio"
    # Se elimina blank=True, null=True
    descripcion = models.TextField(blank=False) 
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)

    def __str__(self):
        return self.nombre

    # --- REGLAS DE NEGOCIO (Movidas de la Vista al Modelo) ---
    
    def puede_eliminarse(self):
        """
        Verifica si la categoría puede ser eliminada.
        Devuelve (True, None) o (False, "Mensaje de error").
        """
        # Asumimos que el modelo 'Examen' tendrá un related_name='examen_set'
        # o un related_name por defecto 'examen_set'.
        try:
            if self.examen_set.exists():
                return (False, f"No se puede eliminar la categoría '{self.nombre}' porque está asignada a uno o más exámenes.")
        except AttributeError:
            # Maneja el caso donde el modelo Examen aún no existe o 
            # el related_name es diferente.
            # (Puedes ajustar 'examen_set' al related_name correcto)
            pass
            
        return (True, None)

    def delete(self, *args, **kwargs):
        """
        Sobrescribe el método de eliminación para aplicar reglas de negocio.
        """
        se_puede, razon = self.puede_eliminarse()
        if not se_puede:
            raise ValidationError(razon)
            
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'Categorias'
        verbose_name = "Categoría de Examen"
        verbose_name_plural = "Categorías de Exámenes"
        ordering = ['categoria_id']