from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .models import Usuario
from .forms import CustomAuthenticationForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# --- Autenticación ---

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Intentamos autenticar con username o email
            user = authenticate(request, username=username_or_email, password=password)
            if not user:
                 try:
                    user_by_email = Usuario.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_by_email.username, password=password)
                 except Usuario.DoesNotExist:
                    user = None

            if user is not None:
                if user.estado != 'Activo':
                    messages.error(request, "Tu cuenta se encuentra inactiva. Contacta al administrador.")
                    return render(request, 'usuarios/login.html', {'form': form})
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Username, correo o contraseña incorrectos.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect('login')

# --- Mixin de Seguridad para el CRUD de Administradores ---

class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol.nombre == 'Administrador'

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
        # Obtener todos los roles únicos para los filtros
        from django.contrib.auth.models import Group  # o tu modelo de Rol
        context['roles'] = Group.objects.all()  # Ajusta según tu modelo de roles
        return context

class UserCreateView(AdminRequiredMixin, CreateView):
    model = Usuario
    form_class = UserRegisterForm
    template_name = 'usuarios/usuario_registrar.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        messages.success(self.request, "Empleado creado exitosamente.")
        return super().form_valid(form)

class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = Usuario
    form_class = UserUpdateForm
    template_name = 'usuarios/usuario_editar.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        messages.success(self.request, "Empleado actualizado exitosamente.")
        return super().form_valid(form)

class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuarios/usuario_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Regla de negocio: No se puede eliminar si ya tiene un rol
        # (que siempre será cierto porque el campo es requerido)
        # Esto previene la eliminación desde el CRUD.
        messages.error(request, f"No se puede eliminar al usuario '{self.object.username}' porque tiene un rol asignado.")
        return redirect(self.success_url)

# --- Vistas de Perfil de Usuario (para todos los usuarios logueados) ---

class ProfileView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'usuarios/perfil.html'
    context_object_name = 'perfil'

    def get_object(self, queryset=None):
        return self.request.user # Devuelve el perfil del usuario logueado

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = ProfileUpdateForm
    template_name = 'usuarios/editar_perfil.html' # Asegúrate de que sea 'usuarios/editar_perfil.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        # Si se cambió la contraseña, loguear al usuario de nuevo para actualizar la sesión
        # Solo si se está usando una forma de autenticación basada en sesión y la contraseña fue modificada
        if form.cleaned_data.get('new_password1'):
             messages.success(self.request, "Tu perfil y contraseña han sido actualizados exitosamente.")
             response = super().form_valid(form)
             # Re-autenticar al usuario para evitar invalidación de la sesión
             from django.contrib.auth import update_session_auth_hash
             update_session_auth_hash(self.request, self.object)
             return response
        else:
             messages.success(self.request, "Tu perfil ha sido actualizado exitosamente.")
             return super().form_valid(form)
