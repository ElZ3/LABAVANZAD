from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Pacientes.
    """
    class Meta:
        model = Paciente
        fields = [
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'sexo',
            'dui',
            'telefono',
            'correo',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres del paciente'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos del paciente'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'dui': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
        }
