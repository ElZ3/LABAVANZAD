from django.db import models
from django.core.exceptions import ValidationError

class Convenio(models.Model):
    """
    Convenio con una entidad - Sin sistema de descuentos
    """
    TIPO_CHOICES = [
        ('Clínica', 'Clínica'),
        ('Hospital', 'Hospital'),
        ('Empresa', 'Empresa'),
        ('Doctor', 'Doctor')
    ]
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    TIPO_FACTURACION_CHOICES = [
        ('Convenio', 'Facturar al Convenio'),
        ('Paciente', 'Facturar al Paciente'),
    ]

    convenio_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, blank=False, help_text="Nombre oficial de la entidad")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, blank=False)
    
    # CAMPOS DE CONTACTO
    persona_contacto = models.CharField(max_length=100, blank=False)
    telefono_contacto = models.CharField(max_length=20, blank=False)
    correo_contacto = models.EmailField(max_length=100, blank=False)

    # CAMPO DE FACTURACIÓN
    tipo_facturacion = models.CharField(
        max_length=20,
        choices=TIPO_FACTURACION_CHOICES,
        default='Paciente',
        blank=False,
        help_text="Indica a quién se le emitirá la factura por defecto."
    )
    
    condiciones_pago = models.TextField(blank=False, help_text="Detalles del acuerdo de pago")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)

    def __str__(self):
        return self.nombre

    def clean(self):
        """Validaciones básicas del modelo"""
        # Puedes agregar validaciones específicas aquí si es necesario
        pass

    def puede_eliminarse(self):
        """
        Regla de negocio: Verifica si el convenio puede ser eliminado.
        """
        # Verificar si hay órdenes asociadas a este convenio
        if self.ordenes.exists():
            return (False, f"No se puede eliminar el convenio '{self.nombre}' porque tiene órdenes asociadas.")
        
        return (True, None)

    def delete(self, *args, **kwargs):
        se_puede, razon = self.puede_eliminarse()
        if not se_puede:
            raise ValidationError(razon)
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'Convenios'
        verbose_name = "Convenio"
        verbose_name_plural = "Convenios"
        ordering = ['nombre']