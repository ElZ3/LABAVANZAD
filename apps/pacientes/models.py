from django.db import models
from django.core.validators import RegexValidator

class Paciente(models.Model):
    """
    Representa a un paciente en el sistema.
    Todos los campos son obligatorios.
    """
    # Validador para el formato DUI 12345678-9 (reutilizado de la app usuarios)
    dui_validator = RegexValidator(
        regex=r'^\d{8}-\d{1}$',
        message="El DUI debe tener el formato 12345678-9."
    )
    
    # Opciones para el campo 'sexo'
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    paciente_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=False)
    apellido = models.CharField(max_length=100, blank=False)
    fecha_nacimiento = models.DateField(blank=False)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=False)
    dui = models.CharField(
        max_length=10, 
        unique=True, 
        blank=False, 
        validators=[dui_validator]
    )
    telefono = models.CharField(max_length=20, blank=False)
    correo = models.EmailField(max_length=100, blank=False, verbose_name="Correo Electrónico")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['apellido', 'nombre'] # Ordenar por defecto por apellido y nombre
