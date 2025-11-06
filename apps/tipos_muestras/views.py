from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from .models import TipoMuestra
from .forms import TipoMuestraForm

# --- REQUISITO: Mixin de Seguridad para Administradores y Técnicos ---
# (Este Mixin es idéntico al de Categorias)
class AdminTecnicoRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Asegura que el usuario logueado tenga el rol 'Administrador' o 'Tecnico'.
    """
    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.rol:
            return False
        return self.request.user.rol.nombre in ['Administrador', 'Tecnico']

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a esta página.")
        return redirect('dashboard' if self.request.user.is_authenticated else 'login')

# --- CRUD de Tipos de Muestra ---

class TipoMuestraListView(AdminTecnicoRequiredMixin, ListView):
    model = TipoMuestra
    template_name = 'tipos_muestras/muestra_lista.html'
    context_object_name = 'tipos_muestras'

class TipoMuestraCreateView(AdminTecnicoRequiredMixin, CreateView):
    model = TipoMuestra
    form_class = TipoMuestraForm
    template_name = 'tipos_muestras/muestra_registrar.html' # Template unificado
    success_url = reverse_lazy('tipo_muestra_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Tipo de Muestra"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Tipo de muestra registrado exitosamente.")
        return super().form_valid(form)

class TipoMuestraUpdateView(AdminTecnicoRequiredMixin, UpdateView):
    model = TipoMuestra
    form_class = TipoMuestraForm
    template_name = 'tipos_muestras/muestra_editar.html' # Template unificado
    success_url = reverse_lazy('tipo_muestra_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Tipo de Muestra"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Tipo de muestra actualizado exitosamente.")
        return super().form_valid(form)

class TipoMuestraDeleteView(AdminTecnicoRequiredMixin, DeleteView):
    model = TipoMuestra
    template_name = 'tipos_muestras/muestra_confirm_delete.html'
    success_url = reverse_lazy('tipo_muestra_list')

    def post(self, request, *args, **kwargs):
        """
        Sobrescrito para seguir el patrón de 'delegar y capturar'.
        """
        self.object = self.get_object()
        try:
            # ✅ DELEGAR AL MODELO
            self.object.delete()
            messages.success(request, f"Tipo de muestra '{self.object.nombre}' eliminado exitosamente.")
        
        except (ValidationError, ProtectedError) as e:
            # ✅ CAPTURAR ERROR DEL MODELO O BBDD
            error_message = str(e)
            if isinstance(e, ValidationError):
                error_message = e.message 
            elif isinstance(e, ProtectedError):
                error_message = f"No se puede eliminar '{self.object}' porque tiene registros relacionados."
                
            messages.error(request, error_message)
        
        return redirect(self.success_url)