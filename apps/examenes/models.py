from django.db import models
# Importamos el modelo desde la nueva app 'categorias'
from categorias.models import CategoriaExamen

class Examen(models.Model):
    """
    Define un examen de laboratorio individual con todos sus detalles.
    """
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]

    examen_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=False)
    codigo = models.CharField(max_length=20, unique=True, blank=False)
    
    # Relación con la tabla separada CategoriaExamen
    categoria = models.ForeignKey(
        CategoriaExamen, 
        on_delete=models.PROTECT, # Previene borrar categorías en uso
        blank=False, 
        null=False
    )
    
    tipo_muestra = models.CharField(max_length=50, blank=False)
    valor_referencia = models.TextField(blank=False, help_text="Valores normales o de referencia para este examen")
    metodo = models.CharField(max_length=50, blank=False, help_text="Metodología usada para el análisis")
    precio = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Examen"
        verbose_name_plural = "Exámenes"
        ordering = ['categoria', 'nombre']

