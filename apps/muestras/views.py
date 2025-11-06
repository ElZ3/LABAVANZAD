from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView
from ordenes.models import Orden
from tipos_muestras.models import TipoMuestra
from .models import Muestra
from .forms import MuestraCreateForm, MuestraUpdateForm

# Importamos el Mixin de permisos que ya definimos en la app 'ordenes'
from ordenes.views import PersonalAutorizadoRequiredMixin

class MuestraCreateView(PersonalAutorizadoRequiredMixin, CreateView):
    model = Muestra
    form_class = MuestraCreateForm
    template_name = 'muestras/muestra_form.html'

    def dispatch(self, request, *args, **kwargs):
        """ Obtiene la orden padre (FK) desde la URL. """
        self.orden = get_object_or_404(Orden, pk=self.kwargs['orden_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Pasa el 'usuario_actual' y los 'tipos_requeridos' al __init__ del formulario.
        """
        kwargs = super().get_form_kwargs()
        
        # 1. Obtener los Tipos de Muestra REQUERIDOS por los exámenes de la orden
        examenes_en_orden = self.orden.examenes.all()
        paquetes_en_orden = self.orden.paquetes.all()
        
        # Obtenemos los 'tipo_muestra_id' de exámenes y de exámenes dentro de paquetes
        tipos_req_ids = set(examenes_en_orden.values_list('tipo_muestra_id', flat=True))
        for paquete in paquetes_en_orden:
            ids_paquete = paquete.examenes.all().values_list('tipo_muestra_id', flat=True)
            tipos_req_ids.update(ids_paquete)
            
        # 2. Obtener los Tipos de Muestra YA REGISTRADOS para esta orden
        tipos_reg_ids = self.orden.muestras_registradas.values_list('tipo_muestra_id', flat=True)
        
        # 3. Filtramos: Requeridos MENOS Registrados
        tipos_pendientes_ids = [pk for pk in tipos_req_ids if pk not in tipos_reg_ids]
        
        # Pasamos el QuerySet filtrado
        kwargs['tipos_requeridos'] = TipoMuestra.objects.filter(pk__in=tipos_pendientes_ids)
        kwargs['usuario_actual'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Registrar Muestra para Orden #{self.orden.orden_id}"
        context['orden'] = self.orden
        return context

    def form_valid(self, form):
        """ Asigna la orden padre antes de guardar. """
        form.instance.orden = self.orden
        self.object = form.save()  # Guarda el objeto pero NO redirige automáticamente
        messages.success(self.request, f"Muestra '{form.instance.tipo_muestra.nombre}' registrada.")
        # Regresa al "HUB" de edición de la orden padre
        return redirect(reverse('orden_update', kwargs={'pk': self.orden.pk}))

class MuestraUpdateView(PersonalAutorizadoRequiredMixin, UpdateView):
    model = Muestra
    form_class = MuestraUpdateForm
    template_name = 'muestras/muestra_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Actualizar Muestra: {self.object.tipo_muestra.nombre}"
        context['orden'] = self.object.orden # Pasamos la orden para el botón "Volver"
        return context
    
    def form_valid(self, form):
        self.object = form.save()  # Guarda el objeto pero NO redirige automáticamente
        messages.success(self.request, "Estado de la muestra actualizado.")
        # Regresa al "HUB" de edición de la orden padre
        return redirect(reverse('orden_update', kwargs={'pk': self.object.orden.pk}))