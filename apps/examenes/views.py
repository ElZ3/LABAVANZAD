from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Examen
from .forms import ExamenForm
from usuarios.views import AdminRequiredMixin

class ExamenListView(AdminRequiredMixin, ListView):
    model = Examen
    template_name = 'examenes/examen_lista.html'
    context_object_name = 'examenes'

class ExamenCreateView(AdminRequiredMixin, CreateView):
    model = Examen
    form_class = ExamenForm
    template_name = 'examenes/examen_registrar.html'
    success_url = reverse_lazy('examen_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Nuevo Examen"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Examen registrado exitosamente.")
        return super().form_valid(form)

class ExamenUpdateView(AdminRequiredMixin, UpdateView):
    model = Examen
    form_class = ExamenForm
    template_name = 'examenes/examen_editar.html'
    success_url = reverse_lazy('examen_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Examen"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Examen actualizado exitosamente.")
        return super().form_valid(form)

class ExamenDeleteView(AdminRequiredMixin, DeleteView):
    model = Examen
    template_name = 'examenes/examen_confirm_delete.html'
    success_url = reverse_lazy('examen_list')
    
    def form_valid(self, form):
        messages.success(self.request, f"Examen '{self.object}' eliminado exitosamente.")
        return super().form_valid(form)

