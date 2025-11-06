from django import forms
from .models import Paciente
import re # Para las validaciones de formato

class PacienteForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Pacientes.
    Valida formato de campos y obligatoriedad.
    Pasa patrones y mensajes al frontend.
    """

    # --- PATRONES Y MENSAJES CENTRALIZADOS (Para Backend y Frontend) ---
    
    # REQUISITOS: nombre/apellido (letras), correo (email), telefono (8 dígitos)
    REGEX_PATTERNS = {
        'nombre': r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$",
        'apellido': r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$",
        'dui': r'^\d{8}-\d{1}$',
        'telefono': r'^\d{8}$',
        'correo': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    }

    ERROR_MESSAGES = {
        'nombre': "El nombre solo puede contener letras y espacios.",
        'apellido': "El apellido solo puede contener letras y espacios.",
        'dui': "El DUI debe tener el formato 12345678-9.",
        'telefono': "El teléfono debe contener 8 dígitos numéricos (ej: 77123456).",
        'correo': "Introduce una dirección de correo electrónico válida.",
        'campo_vacio': "Este campo es requerido.",
        'seleccion_vacia': "Debes seleccionar una opción.",
    }

    class Meta:
        model = Paciente
        fields = [
            'nombre', 'apellido', 'fecha_nacimiento', 'sexo',
            'dui', 'telefono', 'correo',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombres del paciente'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos del paciente'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'dui': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '77123456'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
        }

    def clean(self):
        """
        Validación de campos vacíos y formato, siguiendo el patrón de RolForm.
        """
        cleaned_data = super().clean()
        
        # Lista de campos a validar (nombre_campo, clave_regex, es_requerido)
        campos_a_validar = [
            ('nombre', 'nombre', True),
            ('apellido', 'apellido', True),
            ('dui', 'dui', True),
            ('telefono', 'telefono', True),
            ('correo', 'correo', True),
            ('fecha_nacimiento', None, True), # Solo requerido, sin regex de formato
            ('sexo', None, True),             # Solo requerido
        ]

        for campo, clave_regex, requerido in campos_a_validar:
            dato = cleaned_data.get(campo)
            
            # 1. Limpiar (si es string)
            valor_limpio = ""
            if isinstance(dato, str):
                # Caso especial: teléfono (quitar guiones antes de validar)
                if campo == 'telefono':
                    valor_limpio = re.sub(r"[\s\-]", "", dato)
                    cleaned_data[campo] = valor_limpio # Guardar valor limpio
                else:
                    valor_limpio = dato.strip()
            elif dato: # Para fecha_nacimiento o sexo
                valor_limpio = dato
            
            # 2. Validar si está vacío
            if requerido and not valor_limpio:
                if campo in ['sexo']:
                    self.add_error(campo, self.ERROR_MESSAGES['seleccion_vacia'])
                else:
                    self.add_error(campo, self.ERROR_MESSAGES['campo_vacio'])
                continue # No seguir validando formato si está vacío

            # 3. Validar formato (si aplica)
            if valor_limpio and clave_regex:
                if not re.fullmatch(self.REGEX_PATTERNS[clave_regex], valor_limpio):
                    self.add_error(campo, self.ERROR_MESSAGES[clave_regex])

        return cleaned_data

    # --- Métodos para pasar datos al Frontend ---
    
    def get_regex_patterns(self):
        return self.REGEX_PATTERNS

    def get_error_messages(self):
        return self.ERROR_MESSAGES