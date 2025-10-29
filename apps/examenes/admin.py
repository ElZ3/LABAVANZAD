from django.contrib import admin
from .models import Examen

@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'categoria', 'precio', 'estado')
    list_filter = ('categoria', 'estado')
    search_fields = ('nombre', 'codigo')

