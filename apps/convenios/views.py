from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Convenio
from .forms import ConvenioForm

# --- Mixin de Seguridad para Administradores ---
# NOTA: Este Mixin es idéntico al de la app 'usuarios'.
# En un proyecto más grande, podrías moverlo a un lugar central (ej. una app 'core').
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Asegura que el usuario logueado tenga el rol 'Administrador'.
    """
    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return self.request.user.rol.nombre == 'Administrador'

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a esta página.")
        return redirect('dashboard')

# --- Vistas del CRUD de Convenios ---

class ConvenioListView(AdminRequiredMixin, ListView):
    model = Convenio
    template_name = 'convenios/convenio_lista.html'
    context_object_name = 'convenios'

class ConvenioCreateView(AdminRequiredMixin, CreateView):
    model = Convenio
    form_class = ConvenioForm
    template_name = 'convenios/convenio_registrar.html'
    success_url = reverse_lazy('convenio_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Nuevo Convenio"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Convenio registrado exitosamente.")
        return super().form_valid(form)

class ConvenioUpdateView(AdminRequiredMixin, UpdateView):
    model = Convenio
    form_class = ConvenioForm
    template_name = 'convenios/convenio_editar.html'
    success_url = reverse_lazy('convenio_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Convenio"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Convenio actualizado exitosamente.")
        return super().form_valid(form)

class ConvenioDeleteView(AdminRequiredMixin, DeleteView):
    model = Convenio
    template_name = 'convenios/convenio_confirm_delete.html'
    success_url = reverse_lazy('convenio_list')

    def form_valid(self, form):
        messages.success(self.request, f"Convenio '{self.object}' eliminado exitosamente.")
        return super().form_valid(form)
