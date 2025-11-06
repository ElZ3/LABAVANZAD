import re
from django import forms
from .models import Paquete, PaqueteExamen
from examenes.models import Examen

class PaqueteForm(forms.ModelForm):
    """ Formulario para el modelo Paquete. """
    
    # --- PATRONES Y MENSAJES (Arquitectura) ---
    REGEX_PATTERNS = {
        'nombre': r"^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\.,\-\(\)]+$",
    }
    ERROR_MESSAGES = {
        'nombre': "El nombre solo puede contener letras, números, espacios y (.,-).",
        'precio': "El precio debe ser un número positivo.",
        'campo_vacio': "Este campo es requerido.",
    }

    # Campo para seleccionar exámenes (ManyToMany)
    examenes = forms.ModelMultipleChoiceField(
        queryset=Examen.objects.filter(estado='Activo'),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': '8'}),
        required=True,
        help_text="Mantén presionada la tecla Ctrl (Cmd en Mac) para seleccionar múltiples exámenes."
    )

    class Meta:
        model = Paquete
        fields = ['nombre', 'descripcion', 'precio', 'estado', 'examenes']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando, mostrar los exámenes ya seleccionados
        if self.instance and self.instance.pk:
            self.fields['examenes'].initial = self.instance.examenes.filter(
                paqueteexamen__estado='Activo'
            )

    def clean(self):
        cleaned_data = super().clean()
        
        # Validación de nombre
        nombre = cleaned_data.get('nombre', '').strip()
        if not nombre:
            self.add_error('nombre', self.ERROR_MESSAGES['campo_vacio'])
        elif not re.fullmatch(self.REGEX_PATTERNS['nombre'], nombre):
            self.add_error('nombre', self.ERROR_MESSAGES['nombre'])
        
        # Validación de precio
        precio = cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            self.add_error('precio', self.ERROR_MESSAGES['precio'])
        
        # Validación de exámenes
        examenes = cleaned_data.get('examenes')
        if not examenes:
            self.add_error('examenes', "Debe seleccionar al menos un examen.")
        
        return cleaned_data

    # --- Métodos para el Frontend (Arquitectura) ---
    def get_regex_patterns(self): 
        return self.REGEX_PATTERNS
    
    def get_error_messages(self): 
        return self.ERROR_MESSAGES


class PaqueteExamenForm(forms.ModelForm):
    """ Formulario para editar un examen individual dentro de un paquete """
    class Meta:
        model = PaqueteExamen
        fields = ['orden', 'estado']
        widgets = {
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'orden': 'Orden de aparición',
            'estado': 'Estado en el paquete',
        }