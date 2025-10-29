from django.db import models

class Convenio(models.Model):
    """
    Representa un convenio con una clínica, hospital o empresa.
    Todos los campos son obligatorios.
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

    convenio_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, blank=False, help_text="Nombre oficial de la entidad")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, blank=False)
    contacto = models.CharField(max_length=100, blank=False, help_text="Nombre de la persona de contacto")
    condiciones_pago = models.TextField(blank=False, help_text="Detalles del acuerdo de pago")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Convenio"
        verbose_name_plural = "Convenios"
        ordering = ['nombre']

