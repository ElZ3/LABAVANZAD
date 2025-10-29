from django import forms
from .models import Examen
from categorias.models import CategoriaExamen
from django.core.exceptions import ValidationError

class ExamenForm(forms.ModelForm):
    """Formulario para el CRUD de Exámenes con validación de campos obligatorios."""
    
    class Meta:
        model = Examen
        fields = [
            'nombre', 'codigo', 'categoria', 'tipo_muestra', 
            'valor_referencia', 'metodo', 'precio', 'estado'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'tipo_muestra': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Sangre, Orina, Heces'}),
            'valor_referencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'metodo': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra el queryset para mostrar solo categorías activas en el dropdown
        self.fields['categoria'].queryset = CategoriaExamen.objects.filter(estado='Activo').order_by('nombre')

    def clean(self):
        """
        Garantiza que ningún campo se deje vacío. 
        Todos los campos de texto/numéricos/select se validan para no estar vacíos.
        """
        cleaned_data = super().clean()
        
        # Lista de campos que deben ser obligatorios (todos los definidos en Meta.fields)
        required_fields = self.Meta.fields

        for field_name in required_fields:
            field_value = cleaned_data.get(field_name)
            
            # Comprobamos si el campo está vacío. 
            # Esto funciona para cadenas vacías (''), None, 0, o campos de selección no seleccionados.
            if not field_value and field_value != 0: 
                # Obtenemos el nombre legible del campo para el mensaje de error
                field_label = self.fields[field_name].label or field_name.replace('_', ' ').capitalize()
                
                # Añade el error al campo específico
                self.add_error(field_name, f"El campo '{field_label}' no puede estar vacío.")

        # Dado que todos los campos aceptan letras y números (por ser TextInput o Textarea),
        # no se necesita validación de formato adicional, solo la de "no-vacío".
        return cleaned_data
