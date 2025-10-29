from django.contrib import admin
<<<<<<< HEAD
from .models import Convenio

@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'contacto', 'estado')
    list_filter = ('tipo', 'estado')
    search_fields = ('nombre', 'contacto')

=======
from .models import Convenio, DescuentoEspecifico

class DescuentoEspecificoInline(admin.TabularInline):
        model = DescuentoEspecifico
        extra = 1

@admin.register(Convenio)
class ConvenioAdmin(admin.ModelAdmin):
        list_display = ('nombre', 'tipo', 'persona_contacto', 'telefono_contacto', 'estado')
        list_filter = ('tipo', 'estado')
        search_fields = ('nombre', 'persona_contacto')
        inlines = [DescuentoEspecificoInline] # ¡Permite editar descuentos desde el convenio!
>>>>>>> backup-local
