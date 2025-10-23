from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

Usuario = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulario de login personalizado.
    El campo 'username' puede recibir el username o el correo.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Username o Correo'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Contraseña'}
        )

class UserRegisterForm(forms.ModelForm):
    """Formulario para que los administradores registren nuevos usuarios."""
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellido', 'email', 'dui', 'rol', 'estado']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
        
class UserUpdateForm(forms.ModelForm):
    """Formulario para que los administradores editen usuarios."""
    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellido', 'email', 'dui', 'rol', 'estado']

class ProfileUpdateForm(forms.ModelForm):
    """Formulario para que los usuarios editen su propio perfil."""
    class Meta:
        model = Usuario
        # El usuario solo puede editar estos campos de su propio perfil
        fields = ['username', 'nombre', 'apellido', 'email', 'dui']
