import re
from django import forms
from .models import Examen, MetodoExamen, ValorReferencia
from categorias.models import CategoriaExamen
from tipos_muestras.models import TipoMuestra

# --- Formulario 1: Examen Principal ---

class ExamenForm(forms.ModelForm):
    """ Formulario para el modelo principal Examen. """
    
    # --- PATRONES Y MENSAJES (Arquitectura) ---
    REGEX_PATTERNS = {
        'nombre': r"^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s\.,\-\(\)]+$",
        'codigo': r"^[A-Z0-9_]+$",
    }
    ERROR_MESSAGES = {
        'nombre': "El nombre solo puede contener letras, números, espacios y (.,-).",
        'codigo': "El código solo puede contener letras mayúsculas, números y guión bajo (_).",
        'precio': "El precio debe ser un número positivo.",
        'campo_vacio': "Este campo es requerido.",
        'seleccion_vacia': "Debes seleccionar una opción.",
    }

    class Meta:
        model = Examen
        fields = ['nombre', 'codigo', 'categoria', 'tipo_muestra', 'precio', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform:uppercase;'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'tipo_muestra': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = CategoriaExamen.objects.filter(estado='Activo')
        self.fields['tipo_muestra'].queryset = TipoMuestra.objects.filter(estado='Activo')

    def clean_codigo(self):
        return self.cleaned_data.get('codigo', '').upper()

    def clean(self):
        cleaned_data = super().clean()
        campos_texto = {'nombre': 'nombre', 'codigo': 'codigo'}
        for campo, regex_key in campos_texto.items():
            dato = cleaned_data.get(campo, '').strip()
            if not dato: self.add_error(campo, self.ERROR_MESSAGES['campo_vacio'])
            elif not re.fullmatch(self.REGEX_PATTERNS[regex_key], dato): self.add_error(campo, self.ERROR_MESSAGES[regex_key])

        if not cleaned_data.get('categoria'): self.add_error('categoria', self.ERROR_MESSAGES['seleccion_vacia'])
        if not cleaned_data.get('tipo_muestra'): self.add_error('tipo_muestra', self.ERROR_MESSAGES['seleccion_vacia'])
        
        precio = cleaned_data.get('precio')
        if precio is not None and precio <= 0: self.add_error('precio', self.ERROR_MESSAGES['precio'])
        
        return cleaned_data

    # --- Métodos para el Frontend (Arquitectura) ---
    def get_regex_patterns(self): return self.REGEX_PATTERNS
    def get_error_messages(self): return self.ERROR_MESSAGES

# --- Formulario 2: Métodos (Hijo) ---

class MetodoExamenForm(forms.ModelForm):
    """ Formulario simple para el modelo hijo MetodoExamen. """
    class Meta:
        model = MetodoExamen
        fields = ['metodo', 'estado']
        widgets = {
            'metodo': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

# --- Formulario 3: Valores de Referencia (Hijo) ---

class ValorReferenciaForm(forms.ModelForm):
    class Meta:
        model = ValorReferencia
        # Quitamos 'poblacion', agregamos sexo y edades
        fields = ['sexo', 'edad_minima', 'edad_maxima', 'rango_referencia', 'unidad_medida', 'tipo_resultado', 'estado']
        widgets = {
            'sexo': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'edad_minima': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '0'}),
            'edad_maxima': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': '120'}),
            'rango_referencia': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Ej: 70-110'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Ej: mg/dL'}),
            'tipo_resultado': forms.Select(attrs={'class': 'form-select form-select-sm'}),
            'estado': forms.Select(attrs={'class': 'form-select form-select-sm'}),
        }