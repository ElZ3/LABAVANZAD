from django import forms
from .models import Pago

class PagoForm(forms.ModelForm):
    """
    Formulario simple para registrar un nuevo pago.
    """
    class Meta:
        model = Pago
        fields = ['monto', 'metodo', 'observaciones']
        widgets = {
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'metodo': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control'}),
        }