from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError

from .models import Convenio, ConvenioExamen, ConvenioPaquete
from .forms import ConvenioForm, ConvenioExamenForm, ConvenioPaqueteForm

# --- Mixin de Seguridad (Asumiendo que lo tienes en usuarios o ordenes) ---
# Si no, cópialo aquí. Usaremos uno básico por ahora.
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol.nombre in ['Administrador', 'Jefe de Laboratorio']

# ==========================================
# === CRUD PRINCIPAL (CONVENIOS) ===
# ==========================================

class ConvenioListView(AdminRequiredMixin, ListView):
    model = Convenio
    template_name = 'convenios/convenio_list.html'
    context_object_name = 'convenios'

class ConvenioCreateView(AdminRequiredMixin, CreateView):
    model = Convenio
    form_class = ConvenioForm
    template_name = 'convenios/convenio_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Convenio creado. Ahora puedes agregar descuentos específicos.")
        return super().form_valid(form)

    def get_success_url(self):
        # Al crear, redirige al "Panel de Detalle"
        return reverse('convenio_detail', kwargs={'pk': self.object.pk})

class ConvenioUpdateView(AdminRequiredMixin, UpdateView):
    model = Convenio
    form_class = ConvenioForm
    template_name = 'convenios/convenio_form.html'

    def form_valid(self, form):
        messages.success(self.request, "Datos del convenio actualizados.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('convenio_detail', kwargs={'pk': self.object.pk})

class ConvenioDeleteView(AdminRequiredMixin, DeleteView):
    model = Convenio
    template_name = 'convenios/convenio_confirm_delete.html'
    success_url = reverse_lazy('convenio_list')

    def delete(self, request, *args, **kwargs):
        # Manejo manual para capturar ValidationError del modelo
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, f"Convenio '{self.object.nombre}' eliminado.")
            return redirect(self.success_url)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('convenio_list') # O al detalle

# ==========================================
# === EL HUB (DETALLE DEL CONVENIO) ===
# ==========================================

class ConvenioDetailView(AdminRequiredMixin, DetailView):
    model = Convenio
    template_name = 'convenios/convenio_detail.html'
    context_object_name = 'convenio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos las excepciones a la plantilla
        context['excepciones_examenes'] = self.object.descuentos_examenes.select_related('examen').all()
        context['excepciones_paquetes'] = self.object.descuentos_paquetes.select_related('paquete').all()
        return context

# ==========================================
# === CRUD HIJOS (EXCEPCIONES) ===
# ==========================================

class ConvenioExamenCreateView(AdminRequiredMixin, CreateView):
    model = ConvenioExamen
    form_class = ConvenioExamenForm
    template_name = 'convenios/modal_form.html' # Template genérico

    def form_valid(self, form):
        convenio = get_object_or_404(Convenio, pk=self.kwargs['convenio_pk'])
        form.instance.convenio = convenio
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('examen', "Este examen ya tiene un descuento configurado.")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('convenio_detail', kwargs={'pk': self.kwargs['convenio_pk']})

class ConvenioExamenDeleteView(AdminRequiredMixin, DeleteView):
    model = ConvenioExamen
    
    def get_success_url(self):
        messages.warning(self.request, "Descuento específico eliminado. Aplicará el general.")
        return reverse('convenio_detail', kwargs={'pk': self.object.convenio.pk})

class ConvenioPaqueteCreateView(AdminRequiredMixin, CreateView):
    model = ConvenioPaquete
    form_class = ConvenioPaqueteForm
    template_name = 'convenios/modal_form.html'

    def form_valid(self, form):
        convenio = get_object_or_404(Convenio, pk=self.kwargs['convenio_pk'])
        form.instance.convenio = convenio
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('paquete', "Este paquete ya tiene un descuento configurado.")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('convenio_detail', kwargs={'pk': self.kwargs['convenio_pk']})

class ConvenioPaqueteDeleteView(AdminRequiredMixin, DeleteView):
    model = ConvenioPaquete
    
    def get_success_url(self):
        messages.warning(self.request, "Descuento específico eliminado.")
        return reverse('convenio_detail', kwargs={'pk': self.object.convenio.pk})