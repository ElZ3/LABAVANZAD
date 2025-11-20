from django import forms
from .models import Resultado

class ResultadoHeaderForm(forms.ModelForm):
    """
    Formulario para las observaciones generales y el estado.
    Usado en la vista de ingreso de resultados.
    """
    class Meta:
        model = Resultado
        fields = ['observaciones_generales', 'estado']
        widgets = {
            'observaciones_generales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.HiddenInput(), # El estado se maneja con el botón "Validar"
        }