from django import forms
from .models import Orden
from pacientes.models import Paciente
from convenios.models import Convenio # Importando tu modelo

class OrdenCreateForm(forms.ModelForm):
    """
    Formulario simple usado SÓLO para crear la orden (Paso 1).
    Solo pide los datos iniciales.
    """
    class Meta:
        model = Orden
        fields = ['paciente', 'convenio', 'prioridad', 'metodo_entrega']
        widgets = {
            # Usamos un Select simple. En una app real, esto usaría Select2.
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'convenio': forms.Select(attrs={'class': 'form-select'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'metodo_entrega': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtramos para mostrar solo pacientes y convenios activos
        self.fields['paciente'].queryset = Paciente.objects.all() # Asumiendo que no hay 'estado' en Paciente
        self.fields['convenio'].queryset = Convenio.objects.filter(estado='Activo')
        self.fields['convenio'].empty_label = "Ninguno (Cliente Privado)"

class OrdenUpdateForm(forms.ModelForm):
    """
    Formulario usado en el "HUB" de edición.
    Permite cambiar el estado y la prioridad.
    """
    class Meta:
        model = Orden
        # El usuario no debe cambiar paciente o convenio manualmente aquí
        fields = ['estado', 'prioridad', 'metodo_entrega']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'metodo_entrega': forms.Select(attrs={'class': 'form-select'}),
        }

# --- Formularios de Acción (para los botones "Añadir") ---

class AddExamenForm(forms.Form):
    """ Formulario simple para el botón "Añadir Examen". """
    examen_id = forms.IntegerField(widget=forms.HiddenInput())

class AddPaqueteForm(forms.Form):
    """ Formulario simple para el botón "Añadir Paquete". """
    paquete_id = forms.IntegerField(widget=forms.HiddenInput())