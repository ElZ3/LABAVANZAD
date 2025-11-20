from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Rol
from .forms import RolForm    
from usuarios.views import AdminRequiredMixin
from django.core.exceptions import ValidationError 

# --- CRUD de Roles (para Administradores) ---

class RolListView(AdminRequiredMixin, ListView):
    model = Rol
    template_name = 'roles/rol_lista.html' # Usaremos una nueva carpeta de plantillas
    context_object_name = 'roles'

class RolCreateView(AdminRequiredMixin, CreateView):
    model = Rol
    form_class = RolForm
    template_name = 'roles/rol_form.html'
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
    template_name = 'roles/rol_form.html'
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
        try:
            # ✅ DELEGAR AL MODELO - MODIFICADO
            self.object.delete()
            messages.success(request, f"Rol '{self.object.nombre}' eliminado exitosamente.")
        except ValidationError as e:
            # ✅ CAPTURAR ERROR DEL MODELO - NUEVO
            messages.error(request, str(e))
            return redirect(self.success_url)
        
        return redirect(self.success_url)
