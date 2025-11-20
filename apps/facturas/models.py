from django.db import models
from django.utils import timezone
from ordenes.models import Orden
from usuarios.models import Usuario

class Factura(models.Model):
    """
    Representa el documento legal de la Factura, vinculado 1-a-1 con una Orden.
    Copia los datos de la orden en el momento de la emisión.
    """
    factura_id = models.AutoField(primary_key=True)
    
    # Vínculo 1-a-1
    orden = models.OneToOneField(
        Orden,
        on_delete=models.PROTECT, # No borrar orden si tiene factura
        related_name='factura'  # orden.factura
    )
    
    # Datos del Paciente/Convenio (Copiados para el historial)
    cliente_nombre = models.CharField(max_length=200)
    cliente_dui = models.CharField(max_length=10, blank=True)
    
    # Datos de la Factura (de tu tabla)
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateTimeField(default=timezone.now)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    
    # Montos (Copiados de la Orden en el momento de la emisión)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente de Pago'),
        ('Pagada', 'Pagada'),
        ('Parcial', 'Pago Parcial'),
        ('Anulada', 'Anulada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    
    TIPO_CHOICES = [
        ('Particular', 'Factura Particular'),
        ('Convenio', 'Crédito Fiscal (Convenio)'),
    ]
    tipo_factura = models.CharField(max_length=20, choices=TIPO_CHOICES)
    
    observaciones = models.TextField(blank=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT)

    def __str__(self):
        return f"Factura {self.numero_factura} (Orden #{self.orden.pk})"

    class Meta:
        db_table = 'Facturas'
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['-fecha_emision']