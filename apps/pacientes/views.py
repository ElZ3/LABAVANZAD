from datetime import date
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.exceptions import ValidationError # Importar para capturar
from django.db.models.deletion import ProtectedError # Importar para capturar
from .models import Paciente
from .forms import PacienteForm

# --- Mixin de Seguridad ---

class AdminRecepcionistaRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Asegura que el usuario logueado tenga el rol 'Administrador' o 'Recepcionista'.
    """
    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.rol:
            return False
        # El superusuario siempre tiene acceso (implícito si tiene rol Admin)
        return self.request.user.rol.nombre in ['Administrador', 'Recepcionista']

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a esta página.")
        # Asumiendo que 'dashboard' es tu vista principal
        return redirect('dashboard' if self.request.user.is_authenticated else 'login')

# --- Vistas del CRUD de Pacientes ---

class PacienteListView(AdminRecepcionistaRequiredMixin, ListView):
    model = Paciente
    template_name = 'pacientes/paciente_lista.html'
    context_object_name = 'pacientes'

class PacienteCreateView(AdminRecepcionistaRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    # Usamos un template unificado
    template_name = 'pacientes/paciente_form.html' 
    success_url = reverse_lazy('paciente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Nuevo Paciente"
        return context

    # --- CÁLCULO Y ASIGNACIÓN AL GUARDAR ---
    def form_valid(self, form):
        # Calculamos la edad al momento del registro
        fecha_nacimiento = form.instance.fecha_nacimiento
        
        if fecha_nacimiento:
            today = date.today()
            
            # Lógica precisa de cálculo de edad en años
            edad = today.year - fecha_nacimiento.year - (
                (today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
            )
            # Asignamos el valor al campo de la base de datos
            form.instance.edad_al_registro = edad
            
        messages.success(self.request, "Paciente registrado exitosamente.")
        return super().form_valid(form)

class PacienteUpdateView(AdminRecepcionistaRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    # Usamos un template unificado
    template_name = 'pacientes/paciente_form.html'
    success_url = reverse_lazy('paciente_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Paciente"
        return context

    # --- CÁLCULO Y ASIGNACIÓN AL GUARDAR ---
    def form_valid(self, form):
        # Calculamos la edad al momento del registro
        fecha_nacimiento = form.instance.fecha_nacimiento
        
        if fecha_nacimiento:
            today = date.today()
            
            # Lógica precisa de cálculo de edad en años
            edad = today.year - fecha_nacimiento.year - (
                (today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
            )
            # Asignamos el valor al campo de la base de datos
            form.instance.edad_al_registro = edad
            
        messages.success(self.request, "Paciente registrado exitosamente.")
        return super().form_valid(form)

class PacienteDeleteView(AdminRecepcionistaRequiredMixin, DeleteView):
    model = Paciente
    template_name = 'pacientes/paciente_confirm_delete.html'
    success_url = reverse_lazy('paciente_list')

    def post(self, request, *args, **kwargs):
        """
        Sobrescrito para seguir el patrón de 'delegar y capturar'.
        """
        self.object = self.get_object()
        try:
            # ✅ DELEGAR AL MODELO
            self.object.delete()
            messages.success(request, f"Paciente '{self.object}' eliminado exitosamente.")
        
        except (ValidationError, ProtectedError) as e:
            # ✅ CAPTURAR ERROR DEL MODELO O BBDD
            error_message = str(e)
            if isinstance(e, ValidationError):
                error_message = e.message # Usar el mensaje limpio de la regla de negocio
            elif isinstance(e, ProtectedError):
                error_message = f"No se puede eliminar a '{self.object}' porque tiene registros relacionados."
                
            messages.error(request, error_message)
        
        return redirect(self.success_url)