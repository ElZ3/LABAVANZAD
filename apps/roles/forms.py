from django import forms
from .models import Rol # Importamos Rol

# ... (CustomAuthenticationForm, UserRegisterForm, etc. se mantienen igual) ...

class RolForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Roles.
    """
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

