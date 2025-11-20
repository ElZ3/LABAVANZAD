from django.db import models
from django.utils import timezone
from ordenes.models import Orden
from examenes.models import ValorReferencia # ¡Importante!
from usuarios.models import Usuario

class Resultado(models.Model):
    """
    El "Encabezado" del informe de resultados.
    Se vincula 1-a-1 con una Orden.
    """
    resultado_id = models.AutoField(primary_key=True)
    
    # Vínculo 1-a-1 con la Orden
    orden = models.OneToOneField(
        Orden,
        on_delete=models.CASCADE,
        related_name='resultado' # orden.resultado
    )
    
    ESTADO_CHOICES = [
        ('Pendiente', 'Ingreso de Datos'),  # Visible en Gestión de Resultados
        ('En Espera', 'En Espera de Validación'), # Visible en Validaciones
        ('Validado', 'Validado Final'), # Historial
    ]

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    
    observaciones_generales = models.TextField(blank=True, null=True,
                                        help_text="Observaciones generales del informe (ej: Muestra lipémica)")
    
    # Campos de Validación (REQUISITO)
    validado_por = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        null=True, blank=True, # Solo se llena al validar
        related_name='resultados_validados'
    )
    fecha_validacion = models.DateTimeField(null=True, blank=True)
    
    # Fecha de emisión (cuando se crea el primer borrador)
    fecha_emision = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Resultados para {self.orden}"

    class Meta:
        db_table = 'Resultados'
        verbose_name = "Resultado (Encabezado)"
        verbose_name_plural = "Resultados (Encabezados)"

class ResultadoDetalle(models.Model):
    """
    Una "Línea" o "Parámetro" individual del resultado.
    Almacena el valor obtenido.
    """
    resultado_detalle_id = models.AutoField(primary_key=True)
    
    # Vínculo al encabezado
    resultado = models.ForeignKey(
        Resultado,
        on_delete=models.CASCADE,
        related_name='detalles' # resultado.detalles
    )
    
    # Vínculo al parámetro que se está midiendo
    valor_referencia = models.ForeignKey(
        ValorReferencia,
        on_delete=models.PROTECT, # No borrar "Glucosa" si hay resultados
        related_name='resultados_obtenidos'
    )
    
    # El valor que el técnico de laboratorio ingresó
    # Se usa CharField para permitir "120.5" y "Negativo"
    valor_obtenido = models.CharField(max_length=100, blank=False)
    
    # (Opcional) Podemos añadir lógica futura aquí para marcar esto
    # fuera_de_rango = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.valor_referencia.examen.codigo}: {self.valor_obtenido}"

    class Meta:
        db_table = 'Resultados_Detalle'
        verbose_name = "Resultado (Detalle)"
        verbose_name_plural = "Resultados (Detalles)"
        # Un parámetro solo debe tener un resultado por informe
        unique_together = ('resultado', 'valor_referencia')