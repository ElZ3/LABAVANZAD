import re
from django import forms
from .models import TipoMuestra

class TipoMuestraForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Tipos de Muestra.
    Valida formato de campos y obligatoriedad.
    Pasa patrones y mensajes al frontend.
    """

    # --- PATRONES Y MENSAJES CENTRALIZADOS (Para Backend y Frontend) ---

    REGEX_PATTERNS = {
        # REQUISITO: "nombre solo letra y espacio"
        'nombre': r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$",
        
        # REQUISITO: "descripcion y condiciones... aceptan letras, numeros, espacio y caracteres"
        'general': r"^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\.,;:_\-¡!¿?()\[\]{}#*\/\\@%$&+=°]+$",
    }

    ERROR_MESSAGES = {
        'nombre': "El nombre solo puede contener letras y espacios.",
        'descripcion': "La descripción solo puede contener letras, números, espacios y puntuación.",
        'condiciones': "Este campo solo puede contener letras, números, espacios y puntuación.",
        'campo_vacio': "Este campo es requerido.",
    }

    class Meta:
        model = TipoMuestra
        fields = ['nombre', 'descripcion', 'condiciones_almacenamiento', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Suero, Orina, Sangre total'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción de la muestra...'}),
            'condiciones_almacenamiento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Refrigerado (2-8°C), Congelado (-20°C)'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        """
        Validación de campos vacíos y formato, siguiendo el patrón de RolForm.
        """
        cleaned_data = super().clean()
        
        nombre = cleaned_data.get('nombre', '').strip()
        descripcion = cleaned_data.get('descripcion', '').strip()
        condiciones = cleaned_data.get('condiciones_almacenamiento', '').strip()
        
        regex_nombre = self.REGEX_PATTERNS['nombre']
        regex_general = self.REGEX_PATTERNS['general']

        # --- Validación de Nombre ---
        if not nombre:
            self.add_error('nombre', self.ERROR_MESSAGES['campo_vacio'])
        elif not re.fullmatch(regex_nombre, nombre):
            self.add_error('nombre', self.ERROR_MESSAGES['nombre'])

        # --- Validación de Descripción ---
        if not descripcion:
            self.add_error('descripcion', self.ERROR_MESSAGES['campo_vacio'])
        elif not re.fullmatch(regex_general, descripcion):
            self.add_error('descripcion', self.ERROR_MESSAGES['descripcion'])

        # --- Validación de Condiciones ---
        if not condiciones:
            self.add_error('condiciones_almacenamiento', self.ERROR_MESSAGES['campo_vacio'])
        elif not re.fullmatch(regex_general, condiciones):
            self.add_error('condiciones_almacenamiento', self.ERROR_MESSAGES['condiciones'])

        return cleaned_data

    # --- Métodos para pasar datos al Frontend ---

    def get_regex_patterns(self):
        return self.REGEX_PATTERNS

    def get_error_messages(self):
        return self.ERROR_MESSAGES