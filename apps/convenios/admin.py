from django.contrib import admin
from .models import Convenio

@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'contacto', 'estado')
    list_filter = ('tipo', 'estado')
    search_fields = ('nombre', 'contacto')

