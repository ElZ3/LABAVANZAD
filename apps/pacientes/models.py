from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date
import re

class Paciente(models.Model):
    """
    Representa a un paciente en el sistema.
    Todos los campos son obligatorios.
    Contiene reglas de negocio para borrado y validadores de BBDD.
    """
    
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]

    # --- CAMPOS ---
    
    paciente_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=False)
    apellido = models.CharField(max_length=100, blank=False)
    fecha_nacimiento = models.DateField(blank=False)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=False)
    dui = models.CharField(max_length=10, unique=True, blank=False)
    telefono = models.CharField(max_length=8, blank=False)
    correo = models.EmailField(max_length=100, blank=False, verbose_name="Correo Electrónico")
    edad_al_registro = models.PositiveIntegerField(null=True, blank=True, verbose_name="Edad al Registro"
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    # --- REGLAS DE NEGOCIO Y LIMPIEZA ---

    @property
    def edad(self):
        """Calcula la edad precisa en el momento actual."""
        if not self.fecha_nacimiento: return None
        today = date.today()
        return today.year - self.fecha_nacimiento.year - (
            (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
        )

    def clean(self):
        """
        Normaliza los datos antes de guardarlos.
        """
        super().clean()
        # Limpiar teléfono de espacios o guiones (común en la entrada)
        if self.telefono:
            self.telefono = re.sub(r"[\s\-]", "", self.telefono)

    def puede_eliminarse(self):
        """
        Regla de negocio: Verifica si el paciente puede ser eliminado.
        Un paciente no puede eliminarse si tiene citas, exámenes o historial.
        """
        # A futuro, esto se conectará con otros modelos:
        # if self.cita_set.exists() or self.examen_set.exists():
        #     return (False, f"No se puede eliminar al paciente '{self}' porque tiene citas o exámenes registrados.")
        
        # Simulación (descomentar y adaptar cuando existan los modelos):
        # try:
        #     if self.citas.exists(): # Asumiendo un related_name='citas'
        #         return (False, f"No se puede eliminar al paciente '{self}' porque tiene citas registradas.")
        # except AttributeError:
        #     pass # El modelo Cita aún no existe
            
        return (True, None)

    def delete(self, *args, **kwargs):
        """
        Sobrescribe el método de eliminación para aplicar reglas de negocio.
        """
        se_puede, razon = self.puede_eliminarse()
        if not se_puede:
            raise ValidationError(razon)
            
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean() # Llama a clean() (y validadores) antes de guardar
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'Pacientes'
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['paciente_id']