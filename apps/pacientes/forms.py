from django import forms
from .models import Paciente # Se asume que este modelo existe
from django.core.exceptions import ValidationError
import re # Necesario para la validación de formato (DUI, Teléfono, Nombres)

class PacienteForm(forms.ModelForm):

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
    
    def clean(self):
        """
        Realiza validaciones de campos obligatorios, formato de nombre y formato de teléfono.
        Lanza un único ValidationError con todos los errores acumulados.
        """
        cleaned_data = super().clean()
        errors = {}
        
        # -----------------------------------------------------------
        # 1. Validación de campos vacíos (Obligatoriedad de todos los campos)
        # -----------------------------------------------------------
        required_fields = self.Meta.fields
        for field_name in required_fields:
            field_value = cleaned_data.get(field_name)
            
            # Chequea por valores None, cadena vacía, o False (para selects no seleccionados)
            if not field_value:
                # Obtenemos la etiqueta (label) del campo para el mensaje
                field_label = self.fields[field_name].label or field_name.replace('_', ' ').capitalize()
                
                # Mensaje especial para selects si está vacío
                if field_name == 'sexo':
                    errors[field_name] = f"Seleccione el {field_label} del paciente."
                else:
                    errors[field_name] = f"El campo '{field_label}' no puede estar vacío."
        
        # -----------------------------------------------------------
        # 2. Validación de Nombre y Apellido (Solo letras y espacios)
        # -----------------------------------------------------------
        nombre = cleaned_data.get('nombre')
        apellido = cleaned_data.get('apellido')
        
        # Expresión regular que solo acepta letras (mayúsculas/minúsculas) y espacios.
        # Solo se ejecuta si el campo no ha fallado la prueba de campo vacío antes
        if nombre and 'nombre' not in errors and not re.fullmatch(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            errors['nombre'] = "El nombre solo puede contener letras y espacios."

        if apellido and 'apellido' not in errors and not re.fullmatch(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", apellido):
            errors['apellido'] = "El apellido solo puede contener letras y espacios."

        # -----------------------------------------------------------
        # 3. Validación de Teléfono (8 dígitos)
        # -----------------------------------------------------------
        telefono = cleaned_data.get('telefono')

        if telefono and 'telefono' not in errors:
            # Limpiamos el teléfono (quitamos guiones, espacios) antes de validar
            telefono_limpio = str(telefono).replace('-', '').replace(' ', '')
            
            if len(telefono_limpio) != 8 or not telefono_limpio.isdigit():
                errors['telefono'] = "El teléfono debe ser de 8 dígitos numéricos (ej: 77123456)."
            else:
                # Opcional: guardamos el dato limpio en cleaned_data para usarlo en el modelo
                cleaned_data['telefono'] = telefono_limpio

        # -----------------------------------------------------------
        # 4. Lanzamiento de la Excepción
        # -----------------------------------------------------------
        if errors:
            # Lanza la excepción con el diccionario de errores, mapeando cada mensaje a su campo
            raise forms.ValidationError(errors)

        return cleaned_data
