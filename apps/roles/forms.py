from django import forms
from .models import Rol 
import re

class RolForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Roles.
    Asegura que los campos 'nombre' y 'descripcion' no estén vacíos y
    solo contengan caracteres válidos.
    """

    # PATRONES CENTRALIZADOS
    REGEX_PATTERNS = {
        'nombre': r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$",
        'descripcion': r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\.\,\-\n\r]+$",
    }

    # MENSAJES CENTRALIZADOS
    ERROR_MESSAGES = {
        'nombre': "El nombre del rol solo puede contener letras y espacios.",
        'descripcion': "La descripción no puede contener números, solo letras, espacios y puntuación (.,-).",
        'campo_vacio': "Este campo es requerido.",
    }

    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        nombre = cleaned_data.get('nombre', '').strip()
        descripcion = cleaned_data.get('descripcion', '').strip()

        # --- Validación de campos vacíos ---
        if not nombre:
            self.add_error('nombre', self.ERROR_MESSAGES['campo_vacio'])
        elif not re.fullmatch(self.REGEX_PATTERNS['nombre'], nombre):
            self.add_error('nombre', self.ERROR_MESSAGES['nombre'])

        if not descripcion:
            self.add_error('descripcion', self.ERROR_MESSAGES['campo_vacio'])
        elif not re.fullmatch(self.REGEX_PATTERNS['descripcion'], descripcion):
            self.add_error('descripcion', self.ERROR_MESSAGES['descripcion'])

        return cleaned_data

    # Métodos para pasar patrones y mensajes al frontend
    def get_regex_patterns(self):
        return self.REGEX_PATTERNS

    def get_error_messages(self):
        return self.ERROR_MESSAGES
