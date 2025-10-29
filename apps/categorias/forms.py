import re
from django import forms
from .models import CategoriaExamen
    
class CategoriaExamenForm(forms.ModelForm):
    
    class Meta:
        model = CategoriaExamen
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Biología, Historia'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe brevemente la categoría...'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }
    
    # Validaciones para el campo 'nombre' 
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        
        # 1. Validación de campo vacío
        if not nombre or not nombre.strip():
            raise forms.ValidationError(
                "El campo Nombre no puede estar vacío."
            )
        
        # Validación: No debe contener números
        if re.search(r'\d', nombre):
            raise forms.ValidationError(
                "El nombre no debe contener números (dígitos)."
            )
            
        return nombre

    # Validaciones para el campo 'descripcion'
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        
        # Validación de campo vacío
        if not descripcion or not descripcion.strip():
            raise forms.ValidationError(
                "El campo Descripción no puede estar vacío."
            )
        
        # Validación: No debe contener números (dígitos)
        if re.search(r'\d', descripcion):
            raise forms.ValidationError(
                "La descripción no debe contener números (dígitos)."
            )
            
        return descripcion