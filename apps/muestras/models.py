from django.db import models
from django.utils import timezone
from ordenes.models import Orden
from tipos_muestras.models import TipoMuestra # El 'tipo' de muestra (Suero, Orina)
from usuarios.models import Usuario # El 'responsable' (Usuario del sistema)

class Muestra(models.Model):
    """
    Representa la muestra FÍSICA tomada del paciente para una orden específica.
    Permite la trazabilidad de la muestra dentro del laboratorio.
    """
    muestra_id = models.AutoField(primary_key=True)
    
    # --- VÍNCULOS ---
    orden = models.ForeignKey(
        Orden,
        on_delete=models.CASCADE, # Si se anula la orden, se anulan sus muestras
        related_name='muestras_registradas'
    )
    tipo_muestra = models.ForeignKey(
        TipoMuestra,
        on_delete=models.PROTECT, # No borrar "Suero" si hay muestras de suero
        verbose_name="Tipo de Muestra"
    )
    responsable_toma = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        verbose_name="Responsable de la Toma"
    )

    # --- DATOS DE LA MUESTRA ---
    # Un código único (sticker) para el tubo/contenedor
    codigo_barras = models.CharField(max_length=50, unique=True, blank=True, null=True,
                                     help_text="Código único de la etiqueta de la muestra")
    
    fecha_toma = models.DateTimeField(default=timezone.now, blank=False)
    
    ESTADO_CHOICES = [
        ('Recepcionada', 'Recepcionada'),   # Recibida en el laboratorio
        ('En Análisis', 'En Análisis'),     # En el equipo
        ('Validación', 'En Validación'),   # Resultados listos para revisar
        ('Finalizado', 'Finalizado'),     # Almacenada
        ('Rechazada', 'Rechazada'),       # Muestra coagulada, hemolizada, etc.
    ]
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES, 
        default='Recepcionada', 
        blank=False
    )
    
    observaciones = models.TextField(blank=True, help_text="Ej: Muestra hemolizada, cantidad insuficiente...")

    def __str__(self):
        return f"{self.tipo_muestra.nombre} (Orden #{self.orden.orden_id})"

    class Meta:
        db_table = 'Muestras'
        verbose_name = "Muestra de Paciente"
        verbose_name_plural = "Muestras de Pacientes"
        ordering = ['-fecha_toma']