from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Paciente
from .forms import PacienteForm

# --- Mixin de Seguridad para Administradores y Recepcionistas ---

class AdminRecepcionistaRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Asegura que el usuario logueado tenga el rol 'Administrador' o 'Recepcionista'.
    """
    def test_func(self):
        # El superusuario siempre tiene acceso
        if self.request.user.is_superuser:
            return True
        # Verifica si el rol del usuario es uno de los permitidos
        return self.request.user.rol.nombre in ['Administrador', 'Recepcionista']

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a esta página.")
        return redirect('dashboard')

# --- Vistas del CRUD de Pacientes ---

class PacienteListView(AdminRecepcionistaRequiredMixin, ListView):
    model = Paciente
    template_name = 'pacientes/paciente_lista.html'
    context_object_name = 'pacientes'

class PacienteCreateView(AdminRecepcionistaRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/paciente_registrar.html'
    success_url = reverse_lazy('paciente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Nuevo Paciente"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Paciente registrado exitosamente.")
        return super().form_valid(form)

class PacienteUpdateView(AdminRecepcionistaRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pacientes/paciente_editar.html'
    success_url = reverse_lazy('paciente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Paciente"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Paciente actualizado exitosamente.")
        return super().form_valid(form)

class PacienteDeleteView(AdminRecepcionistaRequiredMixin, DeleteView):
    model = Paciente
    template_name = 'pacientes/paciente_confirm_delete.html'
    success_url = reverse_lazy('paciente_list')

    def form_valid(self, form):
        # Sobrescribimos para añadir un mensaje de éxito
        messages.success(self.request, f"Paciente '{self.object}' eliminado exitosamente.")
        return super().form_valid(form)
