from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse  # ← Agregar esta importación
from examenes.models import Examen

# Opciones de Estado (mismas que el resto de la arquitectura)
ESTADO_CHOICES = [('Activo', 'Activo'), ('Inactivo', 'Inactivo')]

class Paquete(models.Model):
    """ Modelo principal para paquetes/perfiles de exámenes. """
    paquete_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, blank=False)
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    precio = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=False,
        validators=[MinValueValidator(0.01)]
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)
    
    # Relación muchos a muchos con Examen
    examenes = models.ManyToManyField(
        Examen,
        through='PaqueteExamen',
        related_name='paquetes'
    )

    def __str__(self): 
        return f"{self.nombre} - ${self.precio}"

    def get_absolute_url(self):
        """ URL para redireccionar después de crear/editar """
        return reverse('paquetes:paquete_detail', kwargs={'pk': self.paquete_id})

    def puede_eliminarse(self):
        # (Lógica futura: no borrar si tiene ventas/resultados)
        return (True, None)

    def delete(self, *args, **kwargs):
        se_puede, razon = self.puede_eliminarse()
        if not se_puede: 
            raise ValidationError(razon)
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'Paquetes'
        verbose_name = "Paquete"
        verbose_name_plural = "Paquetes"
        ordering = ['nombre']

class PaqueteExamen(models.Model):
    """ Modelo intermedio para la relación Paquete-Examen """
    paquete_examen_id = models.AutoField(primary_key=True)
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    
    # Campos adicionales
    orden = models.PositiveIntegerField(default=0, help_text="Orden de aparición en el paquete")
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='Activo', 
        blank=False,
        help_text="Estado de este examen dentro del paquete"
    )
    
    class Meta:
        db_table = 'Paquetes_Examenes'
        verbose_name = "Examen en Paquete"
        verbose_name_plural = "Exámenes en Paquetes"
        unique_together = ['paquete', 'examen']
        ordering = ['paquete', 'orden']

    def __str__(self):
        return f"{self.examen.nombre} en {self.paquete.nombre} ({self.estado})"

    def get_absolute_url(self):
        """ URL para redireccionar después de crear/editar """
        return reverse('paquetes:paquete_update', kwargs={'pk': self.paquete.pk})

    def clean(self):
        """ Validación para prevenir duplicados """
        if PaqueteExamen.objects.filter(
            paquete=self.paquete, 
            examen=self.examen
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                f"El examen {self.examen.nombre} ya está en este paquete."
            )
