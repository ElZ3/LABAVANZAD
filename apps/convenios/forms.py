<<<<<<< HEAD
from django import forms
from .models import Convenio

class ConvenioForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Convenios.
    """
    class Meta:
        model = Convenio
        fields = [
            'nombre',
            'tipo',
            'contacto',
            'condiciones_pago',
            'estado'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del convenio'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Dr. Juan Pérez'}),
            'condiciones_pago': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

=======
import re
from django import forms
from django.forms import inlineformset_factory
from .models import Convenio, DescuentoEspecifico
from examenes.models import Examen

class ConvenioForm(forms.ModelForm):
    class Meta:
        model = Convenio
        fields = [
            'nombre', 'tipo', 'estado',
            'persona_contacto', 'telefono_contacto', 'correo_contacto',
            'tipo_facturacion', 'descuento_general', 'condiciones_pago'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'persona_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'correo_contacto': forms.EmailInput(attrs={'class': 'form-control'}),
            'tipo_facturacion': forms.Select(attrs={'class': 'form-select'}),
            'descuento_general': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'condiciones_pago': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    # Sobreescribir mensajes de error por defecto (ej. campos requeridos)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer mensajes de error para campos obligatorios (None o empty string)
        required_fields = ['nombre', 'tipo', 'estado', 'persona_contacto', 'telefono_contacto', 
                           'correo_contacto', 'tipo_facturacion', 'condiciones_pago']
        for field in required_fields:
            if self.fields.get(field):
                self.fields[field].error_messages['required'] = "Este campo es obligatorio y no puede estar vacío. ⚠️"

    # --- VALIDACIÓN 1: Nombre no acepta números y no vacío ---
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or not nombre.strip():
            # Esto ya está cubierto por el __init__ pero se mantiene el chequeo de strip
            raise forms.ValidationError("El campo Nombre no puede estar vacío.")

        # Verificar si contiene números (dígitos)
        if re.search(r'\d', nombre):
            raise forms.ValidationError(
                "El Nombre no debe contener números (dígitos). 🚫"
            )
        return nombre

    # --- VALIDACIÓN 2: Persona de Contacto no acepta números y no vacío ---
    def clean_persona_contacto(self):
        persona_contacto = self.cleaned_data.get('persona_contacto')
        
        if not persona_contacto or not persona_contacto.strip():
            raise forms.ValidationError("El campo Persona de Contacto no puede estar vacío.")

        # Verificar si contiene números (dígitos)
        if re.search(r'\d', persona_contacto):
            raise forms.ValidationError(
                "El nombre de la Persona de Contacto no debe contener números (dígitos). 🚫"
            )
        return persona_contacto

    # --- VALIDACIÓN 3: Teléfono debe contener exactamente 8 dígitos y no vacío ---
    def clean_telefono_contacto(self):
        telefono = self.cleaned_data.get('telefono_contacto')
        
        if not telefono or not telefono.strip():
            raise forms.ValidationError("El campo Teléfono no puede estar vacío.")

        # Eliminar cualquier espacio o guion para validar solo los dígitos
        telefono_limpio = re.sub(r'[^\d]', '', telefono) 

        # Verificar si contiene exactamente 8 dígitos
        if not re.fullmatch(r'\d{8}', telefono_limpio):
            raise forms.ValidationError(
                "El Teléfono debe contener exactamente 8 dígitos. 📱"
            )
        return telefono_limpio # Devolvemos el valor limpio para asegurar que se guarde correctamente

    # --- VALIDACIÓN 4: Correo debe ser un formato válido y no vacío ---
    def clean_correo_contacto(self):
        correo = self.cleaned_data.get('correo_contacto')
        if not correo or not correo.strip():
             raise forms.ValidationError("El campo Correo no puede estar vacío.")

        # La validación de formato de correo ya la proporciona el widget forms.EmailInput/EmailField.
        # Solo verificamos que no esté vacío. El error de formato será en español por defecto si tiene
        # la configuración de idioma correcta en settings.py.
        return correo

    # --- VALIDACIÓN 5: Condiciones de Pago no puede estar vacío (acepta números) ---
    def clean_condiciones_pago(self):
        condiciones_pago = self.cleaned_data.get('condiciones_pago')
        if not condiciones_pago or not condiciones_pago.strip():
            raise forms.ValidationError(
                "Las Condiciones de Pago no pueden estar vacías. 📝"
            )
        # Acepta números, por lo que no necesita chequeo adicional de dígitos.
        return condiciones_pago


class DescuentoEspecificoForm(forms.ModelForm):
    """Formulario para el formset de descuentos"""
    # ... (El resto de esta clase se mantiene igual)
    class Meta:
        model = DescuentoEspecifico
        fields = ['examen', 'porcentaje_descuento']
        widgets = {
            'examen': forms.Select(attrs={'class': 'form-select'}),
            'porcentaje_descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        
        # Sobreescribir mensajes de error del formset
        error_messages = {
            'examen': {
                'required': "Debe seleccionar un examen. ⚠️"
            },
            'porcentaje_descuento': {
                'required': "El porcentaje de descuento es obligatorio. ⚠️"
            }
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['examen'].queryset = Examen.objects.all().order_by('nombre')


# FormSet (se mantiene igual)
DescuentoFormSet = inlineformset_factory(
    Convenio,
    DescuentoEspecifico,
    form=DescuentoEspecificoForm,
    extra=1,
    can_delete=True,
    fk_name='convenio'
)
>>>>>>> backup-local
