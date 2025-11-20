from django.db import models
from django.utils import timezone
from ordenes.models import Orden
from usuarios.models import Usuario

class Pago(models.Model):
    """
    Representa una transacción de pago única (completa o parcial)
    asociada a una Orden.
    """
    pago_id = models.AutoField(primary_key=True)
    
    orden = models.ForeignKey(
        Orden,
        on_delete=models.CASCADE,
        related_name='pagos' # orden.pagos.all()
    )
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    
    METODO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia', 'Transferencia'),
    ]
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES, default='Efectivo')
    fecha_pago = models.DateTimeField(default=timezone.now)
    
    registrado_por = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT
    )
    observaciones = models.CharField(max_length=200, blank=True,
                                    help_text="Ej: N° de referencia, abono inicial")

    def __str__(self):
        return f"Pago de ${self.monto} para Orden #{self.orden.pk}"

    class Meta:
        db_table = 'Pagos'
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha_pago']