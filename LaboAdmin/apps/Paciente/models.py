from django.db import models

class Paciente(models.Model):
    paciente_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1)
    dui = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
