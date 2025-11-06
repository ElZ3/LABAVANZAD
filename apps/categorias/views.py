from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# Importaciones para el Mixin y el DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
# Importaciones de la App
from .models import CategoriaExamen
from .forms import CategoriaExamenForm

# --- REQUISITO: Mixin de Seguridad para Administradores y Técnicos ---

class AdminTecnicoRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Asegura que el usuario logueado tenga el rol 'Administrador' o 'Tecnico'.
    """
    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.rol:
            return False
        # Comprueba si el nombre del rol está en la lista de permitidos
        return self.request.user.rol.nombre in ['Administrador', 'Tecnico']

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a esta página.")
        return redirect('dashboard' if self.request.user.is_authenticated else 'login')

# --- CRUD de Categorías de Examen ---

class CategoriaExamenListView(AdminTecnicoRequiredMixin, ListView):
    model = CategoriaExamen
    template_name = 'categorias/categoria_lista.html'
    context_object_name = 'categorias'

class CategoriaExamenCreateView(AdminTecnicoRequiredMixin, CreateView):
    model = CategoriaExamen
    form_class = CategoriaExamenForm
    template_name = 'categorias/categoria_registrar.html' # Template unificado
    success_url = reverse_lazy('categoria_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Nueva Categoría"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Categoría registrada exitosamente.")
        return super().form_valid(form)

class CategoriaExamenUpdateView(AdminTecnicoRequiredMixin, UpdateView):
    model = CategoriaExamen
    form_class = CategoriaExamenForm
    template_name = 'categorias/categoria_editar.html' # Template unificado
    success_url = reverse_lazy('categoria_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Categoría"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Categoría actualizada exitosamente.")
        return super().form_valid(form)

class CategoriaExamenDeleteView(AdminTecnicoRequiredMixin, DeleteView):
    model = CategoriaExamen
    template_name = 'categorias/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria_list')

    def post(self, request, *args, **kwargs):
        """
        Sobrescrito para seguir el patrón de 'delegar y capturar'.
        La lógica de negocio AHORA ESTÁ EN EL MODELO.
        """
        self.object = self.get_object()
        try:
            # ✅ DELEGAR AL MODELO
            self.object.delete()
            messages.success(request, f"Categoría '{self.object.nombre}' eliminada exitosamente.")
        
        except (ValidationError, ProtectedError) as e:
            # ✅ CAPTURAR ERROR DEL MODELO O BBDD
            error_message = str(e)
            if isinstance(e, ValidationError):
                error_message = e.message # Mensaje limpio de la regla de negocio
            elif isinstance(e, ProtectedError):
                error_message = f"No se puede eliminar a '{self.object}' porque tiene exámenes relacionados."
                
            messages.error(request, error_message)
        
        return redirect(self.success_url)