from django import forms
from .models import Convenio

class ConvenioForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Convenios.
    """
    class Meta:
        model = Convenio
        fields = [
            'nombre',
            'tipo',
            'contacto',
            'condiciones_pago',
            'estado'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del convenio'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Dr. Juan Pérez'}),
            'condiciones_pago': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

