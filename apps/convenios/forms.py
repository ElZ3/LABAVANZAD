from django import forms
from .models import Convenio, ConvenioExamen, ConvenioPaquete

class ConvenioForm(forms.ModelForm):
    """Formulario para los datos generales del Convenio."""
    class Meta:
        model = Convenio
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'persona_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_contacto': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo_facturacion': forms.Select(attrs={'class': 'form-select'}),
            'condiciones_pago': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'descuento_general_examenes': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descuento_general_paquetes': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class ConvenioExamenForm(forms.ModelForm):
    """Formulario para agregar una excepción de Examen."""
    class Meta:
        model = ConvenioExamen
        fields = ['examen', 'porcentaje_descuento']
        widgets = {
            'examen': forms.Select(attrs={'class': 'form-select'}), # Idealmente con Select2
            'porcentaje_descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0-100'}),
        }

class ConvenioPaqueteForm(forms.ModelForm):
    """Formulario para agregar una excepción de Paquete."""
    class Meta:
        model = ConvenioPaquete
        fields = ['paquete', 'porcentaje_descuento']
        widgets = {
            'paquete': forms.Select(attrs={'class': 'form-select'}),
            'porcentaje_descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0-100'}),
        }