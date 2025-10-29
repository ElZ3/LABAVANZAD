from django.contrib import admin
from .models import CategoriaExamen
    
@admin.register(CategoriaExamen)
class CategoriaExamenAdmin(admin.ModelAdmin):
        list_display = ('nombre', 'estado')
        list_filter = ('estado',)
        search_fields = ('nombre',)
    
