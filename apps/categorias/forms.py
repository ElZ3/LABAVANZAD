import re
from django import forms
from .models import CategoriaExamen

class CategoriaExamenForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Categorías.
    Valida formato de campos y obligatoriedad.
    Pasa patrones y mensajes al frontend.
    """

    # --- PATRONES Y MENSAJES CENTRALIZADOS (Para Backend y Frontend) ---

    # REQUISITO: nombre y descripcion solo letras y espacio
    REGEX_PATTERNS = {
        'letras_espacios': r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$",
    }

    ERROR_MESSAGES = {
        'nombre': "El nombre solo puede contener letras y espacios.",
        'descripcion': "La descripción solo puede contener letras y espacios.",
        'campo_vacio': "Este campo es requerido.",
    }

    class Meta:
        model = CategoriaExamen
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Hematología, Química Sanguínea'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe brevemente la categoría...'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        """
        Validación de campos vacíos y formato, siguiendo el patrón de RolForm.
        """
        cleaned_data = super().clean()
        
        nombre = cleaned_data.get('nombre', '').strip()
        descripcion = cleaned_data.get('descripcion', '').strip()
        
        regex = self.REGEX_PATTERNS['letras_espacios']

        # --- Validación de Nombre ---
        if not nombre:
            self.add_error('nombre', self.ERROR_MESSAGES['campo_vacio'])
        elif not re.fullmatch(regex, nombre):
            self.add_error('nombre', self.ERROR_MESSAGES['nombre'])

        # --- Validación de Descripción ---
        # REQUISITO: ningun campo puede quedar vacio
        if not descripcion:
            self.add_error('descripcion', self.ERROR_MESSAGES['campo_vacio'])
        elif not re.fullmatch(regex, descripcion):
            self.add_error('descripcion', self.ERROR_MESSAGES['descripcion'])

        return cleaned_data

    # --- Métodos para pasar datos al Frontend ---

    def get_regex_patterns(self):
        # Pasamos solo el que necesitamos
        return {'letras_espacios': self.REGEX_PATTERNS['letras_espacios']}

    def get_error_messages(self):
        return self.ERROR_MESSAGES