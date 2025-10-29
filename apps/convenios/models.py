from django.db import models
<<<<<<< HEAD

class Convenio(models.Model):
    """
    Representa un convenio con una clínica, hospital o empresa.
    Todos los campos son obligatorios.
=======
from examenes.models import Examen  # <-- Importamos el modelo Examen

class Convenio(models.Model):
    """
    Convenio con una entidad, ahora incluye campos de contacto detallados,
    facturación y un sistema de descuentos.
>>>>>>> backup-local
    """
    TIPO_CHOICES = [
        ('Clínica', 'Clínica'),
        ('Hospital', 'Hospital'),
        ('Empresa', 'Empresa'),
        ('Doctor', 'Doctor')
    ]
<<<<<<< HEAD

=======
>>>>>>> backup-local
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
<<<<<<< HEAD
=======
    TIPO_FACTURACION_CHOICES = [
        ('Convenio', 'Facturar al Convenio'),
        ('Paciente', 'Facturar al Paciente'),
    ]
>>>>>>> backup-local

    convenio_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, blank=False, help_text="Nombre oficial de la entidad")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, blank=False)
<<<<<<< HEAD
    contacto = models.CharField(max_length=100, blank=False, help_text="Nombre de la persona de contacto")
=======
    
    # 1. CAMPOS DE CONTACTO (DIVIDIDOS)
    persona_contacto = models.CharField(max_length=100, blank=False)
    telefono_contacto = models.CharField(max_length=20, blank=False)
    correo_contacto = models.EmailField(max_length=100, blank=False)

    # 2. CAMPO DE FACTURACIÓN
    tipo_facturacion = models.CharField(
        max_length=20,
        choices=TIPO_FACTURACION_CHOICES,
        default='Paciente',
        blank=False,
        help_text="Indica a quién se le emitirá la factura por defecto."
    )

    # 3. SISTEMA DE DESCUENTOS (GENERAL)
    descuento_general = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        blank=False,
        help_text="Porcentaje de descuento general (ej: 10.5 para 10.5%). Se aplica si no hay un descuento específico."
    )
    
>>>>>>> backup-local
    condiciones_pago = models.TextField(blank=False, help_text="Detalles del acuerdo de pago")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Convenio"
        verbose_name_plural = "Convenios"
        ordering = ['nombre']

<<<<<<< HEAD
=======
class DescuentoEspecifico(models.Model):
    """
    Modelo 'through' para manejar descuentos específicos por examen.
    Esto permite anular el descuento general.
    """
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE, related_name="descuentos_especificos")
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name="convenios_con_descuento")
    porcentaje_descuento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        help_text="Porcentaje de descuento SOLO para este examen (ej: 25.0)."
    )

    def __str__(self):
        return f"{self.convenio.nombre} - {self.examen.nombre}: {self.porcentaje_descuento}%"

    class Meta:
        unique_together = ('convenio', 'examen') # Solo una regla por convenio/examen
        verbose_name = "Descuento Específico"
        verbose_name_plural = "Descuentos Específicos"

>>>>>>> backup-local
