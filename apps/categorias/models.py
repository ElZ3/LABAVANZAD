from django.db import models
    
class CategoriaExamen(models.Model):

        categoria_id = models.AutoField(primary_key=True) 

        ESTADO_CHOICES = [
            ('Activo', 'Activo'),
            ('Inactivo', 'Inactivo'),
        ]
        nombre = models.CharField(max_length=100, unique=True, blank=False)
        descripcion = models.TextField(blank=True, null=True)
        estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)
    
        def __str__(self):
            return self.nombre
    
        class Meta:
            verbose_name = "Categoría de Examen"
            verbose_name_plural = "Categorías de Exámenes"
            ordering = ['nombre']
    
