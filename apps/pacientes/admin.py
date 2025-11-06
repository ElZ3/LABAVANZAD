from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
        list_display = ('apellido', 'nombre', 'dui', 'telefono', 'correo')
        search_fields = ('nombre', 'apellido', 'dui')
