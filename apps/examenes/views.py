from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from .models import Examen, MetodoExamen, ValorReferencia
from .forms import ExamenForm, MetodoExamenForm, ValorReferenciaForm

# --- Mixin de Seguridad (No cambia) ---
class AdminTecnicoJefeRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.rol:
            return False
        roles_permitidos = ['Administrador', 'Tecnico', 'Jefe de Laboratorio']
        return self.request.user.rol.nombre in roles_permitidos
    
    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a esta página.")
        return redirect('dashboard' if self.request.user.is_authenticated else 'login')

# ===============================================
# === CRUD para Examen (Principal)
# ===============================================

class ExamenListView(AdminTecnicoJefeRequiredMixin, ListView):
    model = Examen
    template_name = 'examenes/examen_lista.html'
    context_object_name = 'examenes'
    queryset = Examen.objects.select_related('categoria', 'tipo_muestra')

class ExamenCreateView(AdminTecnicoJefeRequiredMixin, CreateView):
    model = Examen
    form_class = ExamenForm
    template_name = 'examenes/examen_registrar.html' # Usamos un template simple
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Nuevo Examen"
        return context

    def form_valid(self, form):
        """
        Al crear un examen, guardamos y redirigimos a la vista de 
        EDICIÓN (el "hub") para que el usuario pueda añadir métodos/valores.
        """
        messages.success(self.request, "Examen base creado exitosamente. Ahora añada los métodos y valores.")
        self.object = form.save()
        # Redirige a la vista de "Editar" para el objeto recién creado
        return redirect(reverse('examen_update', kwargs={'pk': self.object.pk}))

class ExamenUpdateView(AdminTecnicoJefeRequiredMixin, UpdateView):
    model = Examen
    form_class = ExamenForm
    template_name = 'examenes/examen_editar.html' # El template "HUB"
    
    def get_context_data(self, **kwargs):
        """
        Este es el "HUB". Pasa el formulario principal y las listas
        de hijos (métodos y valores) al template.
        """
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Examen: {self.object.nombre}"
        # Pasamos las listas de objetos hijos relacionados
        context['metodos_list'] = self.object.metodos.all()
        context['valores_list'] = self.object.valores_referencia.all()
        return context

    def form_valid(self, form):
        self.object = form.save()  # Guardar manualmente
        messages.success(self.request, "Examen actualizado exitosamente.")
        return redirect('examen_list')

class ExamenDeleteView(AdminTecnicoJefeRequiredMixin, DeleteView):
    model = Examen
    template_name = 'examenes/examen_confirm_delete.html'
    success_url = reverse_lazy('examen_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, f"Examen '{self.object.nombre}' eliminado exitosamente.")
        except (ValidationError, ProtectedError) as e:
            error_message = e.message if isinstance(e, ValidationError) else str(e)
            messages.error(request, error_message)
        return redirect(self.success_url)

# ===============================================
# === CRUD para MetodoExamen (Hijo)
# ===============================================

class MetodoCreateView(AdminTecnicoJefeRequiredMixin, CreateView):
    model = MetodoExamen
    form_class = MetodoExamenForm
    template_name = 'examenes/metodo_form.html'

    def dispatch(self, request, *args, **kwargs):
        """ Obtiene el examen padre (FK) desde la URL. """
        self.examen = get_object_or_404(Examen, pk=self.kwargs['examen_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Añadir Método a: {self.examen.nombre}"
        context['examen'] = self.examen
        return context

    def form_valid(self, form):
        form.instance.examen = self.examen
        self.object = form.save()
        messages.success(self.request, f"Método '{self.object.metodo}' añadido exitosamente.")
        return redirect(reverse('examen_update', kwargs={'pk': self.examen.pk}))

class MetodoUpdateView(AdminTecnicoJefeRequiredMixin, UpdateView):
    model = MetodoExamen
    form_class = MetodoExamenForm
    template_name = 'examenes/metodo_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Método"
        context['examen'] = self.object.examen  # ← Usa self.object.examen
        return context
    
    def form_valid(self, form):
        # NO asignes el examen aquí, ya está asignado al objeto existente
        # form.instance.examen = self.examen  ← ESTA LÍNCA CAUSA EL ERROR
        self.object = form.save()
        messages.success(self.request, f"Método '{self.object.metodo}' actualizado exitosamente.")
        return redirect(reverse('examen_update', kwargs={'pk': self.object.examen.pk}))

# ===============================================
# === CRUD para ValorReferencia (Hijo)
# ===============================================

class ValorReferenciaCreateView(AdminTecnicoJefeRequiredMixin, CreateView):
    model = ValorReferencia
    form_class = ValorReferenciaForm
    template_name = 'examenes/valor_referencia_form.html'

    def dispatch(self, request, *args, **kwargs):
        """ Obtiene el examen padre (FK) desde la URL. """
        self.examen = get_object_or_404(Examen, pk=self.kwargs['examen_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Añadir Valor/Parámetro a: {self.examen.nombre}"
        context['examen'] = self.examen
        return context

    def form_valid(self, form):
        form.instance.examen = self.examen
        self.object = form.save()
        messages.success(self.request, "Valor/Parámetro añadido exitosamente.")
        return redirect(reverse('examen_update', kwargs={'pk': self.examen.pk}))

class ValorReferenciaUpdateView(AdminTecnicoJefeRequiredMixin, UpdateView):
    model = ValorReferencia
    form_class = ValorReferenciaForm
    template_name = 'examenes/valor_referencia_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Valor/Parámetro"
        context['examen'] = self.object.examen  # ← Usa self.object.examen
        return context
    
    def form_valid(self, form):
        # NO asignes el examen aquí, ya está asignado
        self.object = form.save()
        messages.success(self.request, "Valor/Parámetro actualizado exitosamente.")
        return redirect(reverse('examen_update', kwargs={'pk': self.object.examen.pk}))