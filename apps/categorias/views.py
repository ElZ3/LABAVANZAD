from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import CategoriaExamen
from .forms import CategoriaExamenForm
from usuarios.views import AdminRequiredMixin 
    
    # --- CRUD de Categorías de Examen ---
    
class CategoriaExamenListView(AdminRequiredMixin, ListView):
        model = CategoriaExamen
        template_name = 'categorias/categoria_lista.html'
        context_object_name = 'categorias'
    
class CategoriaExamenCreateView(AdminRequiredMixin, CreateView):
        model = CategoriaExamen
        form_class = CategoriaExamenForm
        template_name = 'categorias/categoria_registrar.html'
        success_url = reverse_lazy('categoria_list')
    
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['titulo'] = "Registrar Nueva Categoría"
            return context
    
        def form_valid(self, form):
            messages.success(self.request, "Categoría registrada exitosamente.")
            return super().form_valid(form)
    
class CategoriaExamenUpdateView(AdminRequiredMixin, UpdateView):
        model = CategoriaExamen
        form_class = CategoriaExamenForm
        template_name = 'categorias/categoria_editar.html'
        success_url = reverse_lazy('categoria_list')
    
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['titulo'] = "Editar Categoría"
            return context
    
        def form_valid(self, form):
            messages.success(self.request, "Categoría actualizada exitosamente.")
            return super().form_valid(form)
    
class CategoriaExamenDeleteView(AdminRequiredMixin, DeleteView):
        model = CategoriaExamen
        template_name = 'categorias/categoria_confirm_delete.html'
        success_url = reverse_lazy('categoria_list')
    
        def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            if self.object.examen_set.exists():
                messages.error(request, f"No se puede eliminar la categoría '{self.object.nombre}' porque está asignada a uno o más exámenes.")
                return redirect(self.success_url)
            
            messages.success(request, f"Categoría '{self.object.nombre}' eliminada exitosamente.")
            return super().post(request, *args, **kwargs)
    
