from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# Importamos el modelo de esta misma app
from .models import Rol
# Importamos el formulario de esta misma app
from .forms import RolForm    
# Importamos el Mixin de seguridad desde la app de usuarios
from usuarios.views import AdminRequiredMixin

# --- CRUD de Roles (para Administradores) ---

class RolListView(AdminRequiredMixin, ListView):
    model = Rol
    template_name = 'roles/rol_lista.html' # Usaremos una nueva carpeta de plantillas
    context_object_name = 'roles'

class RolCreateView(AdminRequiredMixin, CreateView):
    model = Rol
    form_class = RolForm
    template_name = 'roles/rol_registrar.html'
    success_url = reverse_lazy('rol_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Nuevo Rol"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Rol creado exitosamente.")
        return super().form_valid(form)

class RolUpdateView(AdminRequiredMixin, UpdateView):
    model = Rol
    form_class = RolForm
    template_name = 'roles/rol_editar.html'
    success_url = reverse_lazy('rol_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Rol"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Rol actualizado exitosamente.")
        return super().form_valid(form)

class RolDeleteView(AdminRequiredMixin, DeleteView):
    model = Rol
    template_name = 'roles/rol_confirm_delete.html'
    success_url = reverse_lazy('rol_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Regla de negocio: Verificar si el rol está en uso antes de intentar eliminar
        if self.object.usuario_set.exists():
            messages.error(request, f"No se puede eliminar el rol '{self.object.nombre}' porque está asignado a uno o más usuarios.")
            return redirect(self.success_url)
        
        # Si no está en uso, procede con la eliminación
        messages.success(request, f"Rol '{self.object.nombre}' eliminado exitosamente.")
        return super().post(request, *args, **kwargs)

