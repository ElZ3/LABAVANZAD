from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from .models import Usuario
from roles.models import Rol # Importar Rol para el filtro de lista
from .forms import (
    CustomAuthenticationForm, 
    UserRegisterForm, 
    UserUpdateForm, 
    ProfileUpdateForm
)

# --- Autenticación ---

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard') # Asumiendo que 'dashboard' es tu vista principal

    if request.method == 'POST':
        # La lógica de email/username y estado inactivo ahora está en el form
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
        # Si no es válido, los errores (incluyendo "inactivo") ya vienen en el form
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'usuarios/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login') # Asumiendo que 'login' es el nombre de tu login_view

# --- Mixin de Seguridad ---

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Verifica que el usuario esté logueado Y que su rol sea 'Administrador'.
    """
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        # Comprueba que el usuario tenga un rol asignado antes de leer .nombre
        if self.request.user.rol:
            return self.request.user.rol.nombre == 'Administrador'
        return False

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a esta página.")
        return redirect('dashboard')

# --- CRUD de Usuarios (para Administradores) ---

class UserListView(AdminRequiredMixin, ListView):
    model = Usuario
    template_name = 'usuarios/usuario_lista.html'
    context_object_name = 'usuarios'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # CORREGIDO: Usar el modelo Rol, no Group
        context['roles'] = Rol.objects.all() 
        return context

class UserCreateView(AdminRequiredMixin, CreateView):
    model = Usuario
    form_class = UserRegisterForm
    template_name = 'usuarios/usuario_registrar.html' # Usamos el template unificado
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Nuevo Usuario"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Usuario creado exitosamente.")
        return super().form_valid(form)

class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = Usuario
    form_class = UserUpdateForm
    template_name = 'usuarios/usuario_editar.html' # Usamos el template unificado
    success_url = reverse_lazy('user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Usuario"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Usuario actualizado exitosamente.")
        return super().form_valid(form)

class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # REGLA DE VISTA: Un usuario no puede eliminarse a sí mismo.
        if self.object == request.user:
            messages.error(request, "No puedes eliminar tu propia cuenta de usuario.")
            return redirect(self.success_url)

        try:
            # ✅ DELEGAR AL MODELO - Siguiendo el patrón de Rol
            self.object.delete()
            messages.success(request, f"Usuario '{self.object.username}' eliminado exitosamente.")
        
        except (ValidationError, ProtectedError) as e:
            # ✅ CAPTURAR ERROR DEL MODELO O BBDD
            # 'e' puede ser una lista de errores de ValidationError, así que lo manejamos
            error_message = str(e)
            if isinstance(e, ValidationError):
                error_message = e.message
            elif isinstance(e, ProtectedError):
                error_message = f"No se puede eliminar a '{self.object.username}' porque tiene objetos relacionados que lo protegen."
                
            messages.error(request, error_message)
        
        return redirect(self.success_url)

# --- Vistas de Perfil de Usuario ---

class ProfileView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'usuarios/perfil.html'
    context_object_name = 'perfil'

    def get_object(self, queryset=None):
        return self.request.user # Siempre muestra el perfil del usuario logueado

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = ProfileUpdateForm
    template_name = 'usuarios/editar_perfil.html'
    success_url = reverse_lazy('profile') # Asumiendo que 'profile' es el nombre de ProfileView

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        password_changed = bool(form.cleaned_data.get('new_password1'))
        response = super().form_valid(form)
        
        if password_changed:
            messages.success(self.request, "Tu perfil y contraseña han sido actualizados exitosamente.")
            # Re-autenticar al usuario para evitar invalidación de la sesión
            update_session_auth_hash(self.request, self.object)
        else:
            messages.success(self.request, "Tu perfil ha sido actualizado exitosamente.")
            
        return response