from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from roles.models import Rol # Importar Rol para filtrar el queryset
import re

Usuario = get_user_model()

# ======================================================================
# FORMULARIO BASE (PARA SEGUIR EL PATRÓN DE ROLES Y EVITAR REPETIR CÓDIGO)
# ======================================================================

class UserBaseForm(forms.ModelForm):
    """
    Formulario base que centraliza la validación de formato
    para todos los formularios de usuario, siguiendo el patrón de RolForm.
    """

    # PATRONES CENTRALIZADOS (REQUISITOS)
    REGEX_PATTERNS = {
        'username': r"^[a-zA-Z0-9\.\@\+\-_]+$", # Default de Django
        'nombre': r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$",
        'apellido': r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$",
        'dui': r'^\d{8}-\d{1}$', # para JS
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    }

    # MENSAJES CENTRALIZADOS
    ERROR_MESSAGES = {
        'username': "Username solo puede contener letras, números y @/./+/-/_.",
        'nombre': "El nombre solo puede contener letras y espacios.",
        'apellido': "El apellido solo puede contener letras y espacios.",
        'dui': "El DUI debe tener el formato 12345678-9.",
        'campo_vacio': "Este campo es requerido.",
        'email_invalido': "Por favor, introduce una dirección de correo válida.",
    }

    class Meta:
        model = Usuario
        fields = ['username', 'nombre', 'apellido', 'email', 'dui', 'rol', 'estado']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'dui': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar el queryset de 'rol' para mostrar solo roles 'Activos'
        if 'rol' in self.fields:
            self.fields['rol'].queryset = Rol.objects.filter(estado='Activo')
            # Opcional: añadir un 'empty_label' si el rol es opcional
            self.fields['rol'].empty_label = "Sin rol asignado"


    def clean(self):
        """
        Validación de formato y campos vacíos, siguiendo el patrón de RolForm.
        """
        cleaned_data = super().clean()
        
        campos_a_validar = {
            'username': 'username',
            'nombre': 'nombre',
            'apellido': 'apellido',
            'dui': 'dui',
            'email': 'email',
        }

        for campo, nombre_regex in campos_a_validar.items():
            dato = cleaned_data.get(campo, '').strip()
            if not dato:
                # El modelo ya exige 'blank=False', pero esto es para JS y errores
                if campo in ['username', 'nombre', 'apellido', 'dui','email']: # Rol es opcional
                    self.add_error(campo, self.ERROR_MESSAGES['campo_vacio'])
            elif not re.fullmatch(self.REGEX_PATTERNS[nombre_regex], dato):
                self.add_error(campo, self.ERROR_MESSAGES[nombre_regex])
        
        return cleaned_data

    # Métodos para pasar patrones y mensajes al frontend
    def get_regex_patterns(self):
        return self.REGEX_PATTERNS

    def get_error_messages(self):
        return self.ERROR_MESSAGES

# ======================================================================
# FORMULARIOS ESPECÍFICOS
# ======================================================================

class UserRegisterForm(UserBaseForm):
    """Formulario para que los administradores registren nuevos usuarios."""
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_password1'}),
        label="Contraseña"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_password2'}),
        label="Confirmar Contraseña"
    )

    class Meta(UserBaseForm.Meta):
        # Hereda fields y widgets de la base, solo añadimos los de password
        fields = UserBaseForm.Meta.fields + ['password', 'password2']


    def clean(self):
        # 1. Ejecutar validación de la clase base (nombre, apellido, etc.)
        cleaned_data = super().clean()
        
        # 2. Añadir validación específica de contraseñas
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if not password:
            self.add_error("password", "La contraseña es obligatoria para el registro.")
        if not password2:
            self.add_error("password2", "La confirmación de contraseña es obligatoria.")
        
        if password and password2 and password != password2:
            self.add_error("password2", "Las contraseñas no coinciden.")

        return cleaned_data
    
    def save(self, commit=True):
        # Usamos el save del UserBaseForm (que es ModelForm.save)
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserUpdateForm(UserBaseForm):
    """Formulario para que los administradores editen usuarios. No incluye contraseña."""
    
    class Meta(UserBaseForm.Meta):
        # Usa exactamente los mismos fields y widgets de la base
        pass
    
    # No necesita 'clean()' propio porque toda la validación
    # de formato ya está en UserBaseForm.
    
    # No necesita 'save()' propio, el de ModelForm es suficiente.


class ProfileUpdateForm(UserBaseForm):
    """Formulario para que los usuarios editen su propio perfil. Incluye cambio de contraseña opcional."""

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_new_password1'}),
        label="Nueva Contraseña",
        required=False,
        help_text="Déjalo en blanco si no deseas cambiarla."
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'id_new_password2'}),
        label="Confirmar Nueva Contraseña",
        required=False
    )

    class Meta(UserBaseForm.Meta):
        # El perfil no permite cambiar rol ni estado
        fields = ['username', 'nombre', 'apellido', 'email', 'dui']
        # Los campos de contraseña se añaden manualmente
        
    def __init__(self, *args, **kwargs):
        super(UserBaseForm, self).__init__(*args, **kwargs) # Llamar al init de ModelForm
        # No filtramos roles aquí porque no se usan.

    def clean(self):
        # 1. Ejecutar validación de la clase base
        cleaned_data = super().clean()

        # 2. Añadir validación específica de cambio de contraseña
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        if new_password1 or new_password2:
            if not new_password1 or not new_password2:
                self.add_error(None, "Para cambiar la contraseña, debes ingresar y confirmar la nueva.")
            elif new_password1 != new_password2:
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

# ======================================================================
# FORMULARIO DE LOGIN (Personalizado)
# ======================================================================

class CustomAuthenticationForm(AuthenticationForm):
    """
    Formulario de login personalizado para login con email/username
    y para añadir clases de Bootstrap.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Username o Correo'}
        )
        self.fields['username'].label = "Username o Correo"
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Contraseña', 'id': 'id_login_password'}
        )

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            # Autenticación con email
            if '@' in username_or_email:
                try:
                    user_by_email = Usuario.objects.get(email=username_or_email)
                    # Usamos el username real para el backend de autenticación
                    self.cleaned_data['username'] = user_by_email.username
                except Usuario.DoesNotExist:
                    pass # Dejamos que AuthenticationForm falle normalmente
            
            # Comprobar estado 'Activo'
            try:
                # Buscamos por username o por email
                user = Usuario.objects.get(
                    Q(username=username_or_email) | Q(email=username_or_email)
                )
                if user.estado != 'Activo':
                    raise forms.ValidationError(
                        "Tu cuenta se encuentra inactiva. Contacta al administrador."
                    )
            except Usuario.DoesNotExist:
                pass # Dejamos que AuthenticationForm maneje el error de "no existe"

        return super().clean()