from django import forms
from .models import Rol 
import re
# Asegúrate de que .models.Rol sea accesible desde donde se encuentra este forms.py
# (Se asume que la línea 'from .models import Rol' está en la parte superior de tu archivo)

# ... (Tus otros formularios como CustomAuthenticationForm, UserRegisterForm, etc.) ...
# from .models import Rol # Asumiendo que esta importación está en la parte superior

# ... (Tus otros formularios como CustomAuthenticationForm, UserRegisterForm, etc.) ...

# ----------------------------------------------------------------------
## Formulario para Roles

class RolForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Roles.
    Asegura que los campos 'nombre' y 'descripcion' solo contengan letras y espacios.
    """
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
        
        # Expresión regular para **NOMBRE**: Solo letras y espacios.
        # Incluye letras acentuadas (áéíóúÁÉÍÓÚ) y la ñ/Ñ.
        regex_solo_letras = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
        
        # Expresión regular para **DESCRIPCIÓN**: Más permisiva.
        # Permite letras, espacios, puntos, comas, guiones, saltos de línea (\n\r)
        # pero **prohíbe los dígitos** (0-9).
        # Nota: La coma (,) y el punto (.) son comunes en descripciones.
        regex_solo_letras_desc = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\.\,\-\n\r]+$"

        # --- Validación de Nombre (Solo letras y espacios) ---
        nombre = cleaned_data.get('nombre', '')
        if nombre and not re.fullmatch(regex_solo_letras, nombre):
            self.add_error(
                'nombre', 
                "El nombre del rol solo puede contener letras y espacios."
            )

        # --- Validación de Descripción (Solo letras, espacios y puntuación básica) ---
        descripcion = cleaned_data.get('descripcion', '')
        if descripcion and not re.fullmatch(regex_solo_letras_desc, descripcion):
            self.add_error(
                'descripcion', 
                "La descripción no puede contener números, solo letras, espacios y puntuación (.,-)."
            )
        # -------------------------------------------------------

        return cleaned_data