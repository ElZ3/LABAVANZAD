from django import forms
from django.contrib.auth import get_user_model
<<<<<<< HEAD
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

Usuario = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulario de login personalizado.
    El campo 'username' puede recibir el username o el correo.
=======
from django.contrib.auth.forms import AuthenticationForm
import re 

Usuario = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulario de login personalizado.
>>>>>>> backup-local
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
<<<<<<< HEAD
            {'class': 'form-control', 'placeholder': 'Username o Correo'}
=======
            {'class': 'form-control', 'placeholder': 'Username'}
>>>>>>> backup-local
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Contraseña'}
        )
<<<<<<< HEAD

class UserRegisterForm(forms.ModelForm):
    """Formulario para que los administradores registren nuevos usuarios."""
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
=======
\
## Formulario de Registro (Admin)

class UserRegisterForm(forms.ModelForm):
    """Formulario para que los administradores registren nuevos usuarios."""
    
    # Añadimos form-control a las contraseñas
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Confirmar Contraseña"
    )
>>>>>>> backup-local

    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellido', 'email', 'dui', 'rol', 'estado']
<<<<<<< HEAD

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
        
=======
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'dui': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # --- Validación de Nombre y Apellido (Solo letras y espacios) ---
        nombre = cleaned_data.get('nombre', '')
        apellido = cleaned_data.get('apellido', '')

        regex = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
        
        if nombre and not re.fullmatch(regex, nombre):
            self.add_error('nombre', "El nombre solo puede contener letras y espacios.")

        if apellido and not re.fullmatch(regex, apellido):
            self.add_error('apellido', "El apellido solo puede contener letras y espacios.")
        # ---------------------------------------------------------------
        
        # --- Validación de Contraseñas (Específica del registro) ---
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if not self.instance.pk:
            if password and password2 and password != password2:
                self.add_error("password2", "Las contraseñas no coinciden.")
            if not password:
                self.add_error("password", "La contraseña es obligatoria para el registro.")
            if not password2:
                self.add_error("password2", "La confirmación de contraseña es obligatoria.")

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        
        if not self.instance.pk and password:
            user.set_password(password)
        
        if commit:
            user.save()
        return user


# ----------------------------------------------------------------------
## Formulario de Edición de Usuario (Admin)

>>>>>>> backup-local
class UserUpdateForm(forms.ModelForm):
    """Formulario para que los administradores editen usuarios."""
    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellido', 'email', 'dui', 'rol', 'estado']
<<<<<<< HEAD

class ProfileUpdateForm(forms.ModelForm):
    """Formulario para que los usuarios editen su propio perfil."""
    class Meta:
        model = Usuario
        # El usuario solo puede editar estos campos de su propio perfil
        fields = ['username', 'nombre', 'apellido', 'email', 'dui']
=======
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'dui': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # --- Validación de Nombre y Apellido (Solo letras y espacios) ---
        nombre = cleaned_data.get('nombre', '')
        apellido = cleaned_data.get('apellido', '')
        
        # Expresión regular que solo acepta letras (mayúsculas/minúsculas) y espacios.
        regex = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
        
        if nombre and not re.fullmatch(regex, nombre):
            self.add_error('nombre', "El nombre solo puede contener letras y espacios.")

        if apellido and not re.fullmatch(regex, apellido):
            self.add_error('apellido', "El apellido solo puede contener letras y espacios.")
        # ---------------------------------------------------------------

        return cleaned_data
    
# ----------------------------------------------------------------------
## Formulario de Perfil (Usuario)

class ProfileUpdateForm(forms.ModelForm):
    """Formulario para que los usuarios editen su propio perfil. Incluye campos de contraseña opcionales."""

    # Campos de contraseña opcionales para cambiar la contraseña
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Nueva Contraseña",
        required=False,
        help_text="Déjalo en blanco si no deseas cambiarla."
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}), 
        label="Confirmar Nueva Contraseña",
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellido', 'email', 'dui', 'new_password1', 'new_password2']
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'dui': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        
        # --- Validación de Nombre y Apellido (Solo letras y espacios) ---
        nombre = cleaned_data.get('nombre', '')
        apellido = cleaned_data.get('apellido', '')
        
        # Expresión regular que solo acepta letras (mayúsculas/minúsculas) y espacios.
        regex = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
        
        if nombre and not re.fullmatch(regex, nombre):
            self.add_error('nombre', "El nombre solo puede contener letras y espacios.")

        if apellido and not re.fullmatch(regex, apellido):
            self.add_error('apellido', "El apellido solo puede contener letras y espacios.")
        # ---------------------------------------------------------------
        
        # --- Validación de Contraseñas (Específica del perfil) ---
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 or new_password2:
            if not new_password1 or not new_password2:
                # Usa add_error(None, ...) para un error no asociado a un campo específico
                self.add_error(None, "Debes ingresar y confirmar la nueva contraseña.")
            if new_password1 and new_password2 and new_password1 != new_password2:
                self.add_error("new_password2", "Las contraseñas no coinciden.")
        
        return cleaned_data
        
    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password1")
        
        if new_password:
            user.set_password(new_password)
            
        if commit:
            user.save()
        return user
>>>>>>> backup-local
