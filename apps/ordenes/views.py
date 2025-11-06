from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q # Para búsquedas
from django.db import IntegrityError # Para capturar duplicados

# Importamos todos los modelos necesarios
from .models import Orden, OrdenExamen, OrdenPaquete
from .forms import OrdenCreateForm, OrdenUpdateForm, AddExamenForm, AddPaqueteForm
from examenes.models import Examen
from pacientes.models import Paciente
from paquetes.models import Paquete

# --- REQUISITO: Mixin de Seguridad ---
class PersonalAutorizadoRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.rol:
            return False
        roles_permitidos = [
            'Administrador', 'Recepcionista', 'Analista', 
            'Técnico', 'Jefe de Laboratorio'
        ]
        return self.request.user.rol.nombre in roles_permitidos

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a esta página.")
        return redirect('dashboard' if self.request.user.is_authenticated else 'login')

# ===============================================
# === CRUD para Orden (Principal)
# ===============================================

class OrdenListView(PersonalAutorizadoRequiredMixin, ListView):
    model = Orden
    template_name = 'ordenes/orden_lista.html'
    context_object_name = 'ordenes'
    # Optimizamos la consulta
    queryset = Orden.objects.select_related('paciente', 'convenio').order_by('-fecha_creacion')

class OrdenCreateView(PersonalAutorizadoRequiredMixin, CreateView):
    model = Orden
    form_class = OrdenCreateForm
    template_name = 'ordenes/orden_form_crear.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Crear Nueva Orden (Paso 1)"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Orden creada. Ahora añada exámenes o paquetes.")
        self.object = form.save()
        # Redirigimos al "HUB" de edición (Paso 2)
        return redirect(reverse('orden_update', kwargs={'pk': self.object.pk}))

class OrdenUpdateView(PersonalAutorizadoRequiredMixin, UpdateView):
    model = Orden
    form_class = OrdenUpdateForm
    template_name = 'ordenes/orden_form_editar.html' # El "HUB"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Gestionar Orden #{self.object.orden_id}"
        
        # 1. Obtenemos los IDs de los ítems YA añadidos a esta orden
        examenes_en_orden_ids = self.object.examenes.values_list('examen_id', flat=True)
        paquetes_en_orden_ids = self.object.paquetes.values_list('paquete_id', flat=True)

        # 2. Obtenemos la lista de TODOS los exámenes y paquetes disponibles
        #    (excluyendo los que ya están en la orden)
        q = self.request.GET.get('q', '').strip()
        context['search_query'] = q
        
        # Filtramos solo por 'Activo'
        examenes_disponibles = Examen.objects.filter(estado='Activo')
        paquetes_disponibles = Paquete.objects.filter(estado='Activo')

        if q:
            # Búsqueda inteligente
            examenes_disponibles = examenes_disponibles.filter(
                Q(nombre__icontains=q) | Q(codigo__icontains=q)
            )
            paquetes_disponibles = paquetes_disponibles.filter(
                Q(nombre__icontains=q) # Asumiendo que Paquete no tiene código
            )
        
        # Excluimos los ya añadidos
        context['examenes_disponibles'] = examenes_disponibles.exclude(examen_id__in=examenes_en_orden_ids)
        context['paquetes_disponibles'] = paquetes_disponibles.exclude(paquete_id__in=paquetes_en_orden_ids)
        
        # 3. Formularios simples para los botones "Añadir"
        context['add_examen_form'] = AddExamenForm()
        context['add_paquete_form'] = AddPaqueteForm()
        
        # 4. Pasamos los ítems de la orden (ya añadidos)
        context['items_examen'] = self.object.ordenexamen_set.select_related('examen')
        context['items_paquete'] = self.object.ordenpaquete_set.select_related('paquete')
        
        return context

    def form_valid(self, form):
        """Guarda el formulario y redirige a la misma página de edición."""
        self.object = form.save()  # Guarda manualmente
        messages.success(self.request, "Estado de la orden actualizado.")
        # Redirige a la misma página de edición
        return redirect('orden_update', pk=self.object.pk)

# ===============================================
# === Vistas de ACCIÓN (Añadir/Quitar)
# ===============================================

class AddExamenToOrdenView(PersonalAutorizadoRequiredMixin, View):
    """ Vista simple que solo maneja POST para añadir un examen. """
    def post(self, request, *args, **kwargs):
        orden = get_object_or_404(Orden, pk=self.kwargs['orden_pk'])
        form = AddExamenForm(request.POST)
        
        if form.is_valid():
            examen_id = form.cleaned_data['examen_id']
            examen = get_object_or_404(Examen, pk=examen_id)
            
            try:
                # Usamos el 'through' model para guardar el precio
                OrdenExamen.objects.create(
                    orden=orden,
                    examen=examen,
                    precio_en_orden=examen.precio # Guarda el precio actual del examen
                )
                orden.calcular_totales() # Recalculamos
                messages.success(request, f"Examen '{examen.nombre}' añadido.")
            except IntegrityError:
                messages.error(request, f"El examen '{examen.nombre}' ya está en la orden.")
        
        return redirect(reverse('orden_update', kwargs={'pk': orden.pk}))

class AddPaqueteToOrdenView(PersonalAutorizadoRequiredMixin, View):
    """ Vista simple que añade un paquete. """
    def post(self, request, *args, **kwargs):
        orden = get_object_or_404(Orden, pk=self.kwargs['orden_pk'])
        form = AddPaqueteForm(request.POST)
        
        if form.is_valid():
            paquete_id = form.cleaned_data['paquete_id']
            paquete = get_object_or_404(Paquete, pk=paquete_id)
            
            try:
                OrdenPaquete.objects.create(
                    orden=orden,
                    paquete=paquete,
                    precio_en_orden=paquete.precio # Guarda el precio del PAQUETE
                )
                orden.calcular_totales() # Recalculamos
                messages.success(request, f"Paquete '{paquete.nombre}' añadido.")
            except IntegrityError:
                messages.error(request, f"El paquete '{paquete.nombre}' ya está en la orden.")

        return redirect(reverse('orden_update', kwargs={'pk': orden.pk}))

class RemoveExamenFromOrdenView(PersonalAutorizadoRequiredMixin, View):
    """ Vista simple que solo maneja POST para quitar un examen. """
    def post(self, request, *args, **kwargs):
        orden = get_object_or_404(Orden, pk=self.kwargs['orden_pk'])
        examen_id = self.kwargs['examen_pk']
        
        item = get_object_or_404(OrdenExamen, orden=orden, examen_id=examen_id)
        examen_nombre = item.examen.nombre
        item.delete()
        
        orden.calcular_totales() # Recalculamos
        messages.warning(request, f"Examen '{examen_nombre}' quitado de la orden.")
        
        return redirect(reverse('orden_update', kwargs={'pk': orden.pk}))

class RemovePaqueteFromOrdenView(PersonalAutorizadoRequiredMixin, View):
    """ Vista simple que solo maneja POST para quitar un paquete. """
    def post(self, request, *args, **kwargs):
        orden = get_object_or_404(Orden, pk=self.kwargs['orden_pk'])
        paquete_id = self.kwargs['paquete_pk']
        
        item = get_object_or_404(OrdenPaquete, orden=orden, paquete_id=paquete_id)
        paquete_nombre = item.paquete.nombre
        item.delete()
        
        orden.calcular_totales() # Recalculamos
        messages.warning(request, f"Paquete '{paquete_nombre}' quitado de la orden.")
        
        return redirect(reverse('orden_update', kwargs={'pk': orden.pk}))