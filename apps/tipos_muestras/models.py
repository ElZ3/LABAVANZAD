from django.db import models
from django.core.exceptions import ValidationError

class TipoMuestra(models.Model):
    """
    Define los tipos de muestras (Ej: Suero, Orina) y sus condiciones.
    Contiene reglas de negocio para la eliminación.
    """
    
    # --- CAMPOS (Basados en la definición) ---
    tipo_muestra_id = models.AutoField(primary_key=True)
    
    # REQUISITO: "nombre solo letra y espacio"
    nombre = models.CharField(max_length=50, unique=True, blank=False) 
    
    # REQUISITO: "descripcion ... aceptan letras, numeros, espacio y caracteres"
    # REQUISITO: "ningun campo vacio"
    descripcion = models.CharField(max_length=200, blank=False)
    
    # REQUISITO: "condiciones... aceptan letras, numeros, espacio y caracteres"
    # REQUISITO: "ningun campo vacio"
    condiciones_almacenamiento = models.CharField(max_length=100, blank=False)

    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)

    def __str__(self):
        return self.nombre

    # --- REGLAS DE NEGOCIO (Arquitectura) ---
    
    def puede_eliminarse(self):
        """
        Verifica si el tipo de muestra puede ser eliminado.
        (Ej: No si está asignado a un Examen)
        """
        # Asumimos que un modelo 'Examen' tendrá un related_name='examen_set'
        try:
            if self.examen_set.exists():
                return (False, f"No se puede eliminar '{self.nombre}' porque está asignado a uno o más exámenes.")
        except AttributeError:
            # Aún no existe el modelo Examen, pero la lógica está lista.
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
        db_table = 'Tipos_Muestras'
        verbose_name = "Tipo de Muestra"
        verbose_name_plural = "Tipos de Muestras"
        ordering = ['tipo_muestra_id']