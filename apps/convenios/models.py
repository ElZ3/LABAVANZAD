from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from examenes.models import Examen
from paquetes.models import Paquete

class Convenio(models.Model):
    """
    Convenio con una entidad. Define descuentos generales y sirve de
    padre para descuentos específicos.
    """
    convenio_id = models.AutoField(primary_key=True)
    
    # --- Datos Generales ---
    nombre = models.CharField(max_length=100, unique=True, blank=False, help_text="Nombre oficial de la entidad")
    
    TIPO_CHOICES = [
        ('Clínica', 'Clínica'), ('Hospital', 'Hospital'),
        ('Empresa', 'Empresa'), ('Doctor', 'Doctor'), ('Seguro', 'Aseguradora')
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, blank=False)
    
    # --- Contacto ---
    persona_contacto = models.CharField(max_length=100, blank=False)
    telefono_contacto = models.CharField(max_length=20, blank=False)
    correo_contacto = models.EmailField(max_length=100, blank=False)

    # --- Facturación ---
    TIPO_FACTURACION_CHOICES = [
        ('Convenio', 'Facturar al Convenio'),
        ('Paciente', 'Facturar al Paciente'),
    ]
    tipo_facturacion = models.CharField(
        max_length=20, choices=TIPO_FACTURACION_CHOICES, default='Paciente',
        help_text="A quién se le emite la factura."
    )
    condiciones_pago = models.TextField(blank=False, help_text="Ej: Crédito 30 días, Contra entrega")
    
    ESTADO_CHOICES = [('Activo', 'Activo'), ('Inactivo', 'Inactivo')]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)

    # --- DESCUENTOS GENERALES (Nivel 2 de la Jerarquía) ---
    descuento_general_examenes = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Desc. General Exámenes (%)"
    )
    descuento_general_paquetes = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Desc. General Paquetes (%)"
    )

    def __str__(self):
        return self.nombre

    def puede_eliminarse(self):
        if self.ordenes.exists():
            return (False, f"No se puede eliminar '{self.nombre}' porque tiene órdenes asociadas.")
        return (True, None)

    def delete(self, *args, **kwargs):
        se_puede, razon = self.puede_eliminarse()
        if not se_puede: raise ValidationError(razon)
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'Convenios'
        verbose_name = "Convenio"
        verbose_name_plural = "Convenios"
        ordering = ['nombre']

# --- MODELOS HIJOS (Excepciones / Nivel 1 de la Jerarquía) ---

class ConvenioExamen(models.Model):
    """Descuento específico para un examen en este convenio."""
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE, related_name='descuentos_examenes')
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE)
    porcentaje_descuento = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    class Meta:
        db_table = 'Convenios_Examenes'
        unique_together = ('convenio', 'examen')

class ConvenioPaquete(models.Model):
    """Descuento específico para un paquete en este convenio."""
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE, related_name='descuentos_paquetes')
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE)
    porcentaje_descuento = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    class Meta:
        db_table = 'Convenios_Paquetes'
        unique_together = ('convenio', 'paquete')