from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView
from django.db.models import Q
from examenes.models import Examen
from ordenes.models import Orden
from tipos_muestras.models import TipoMuestra
from .models import Muestra
from .forms import MuestraCreateForm, MuestraUpdateForm
from .utils import generar_codigo_muestra
from ordenes.views import PersonalAutorizadoRequiredMixin # Reutilizamos el Mixin
from resultados.models import Resultado
# --- 2. Submenú: Gestión de Muestras ---
class MuestraListView(PersonalAutorizadoRequiredMixin, ListView):
    model = Orden
    template_name = 'muestras/muestra_lista.html'
    context_object_name = 'ordenes'
    
    def get_queryset(self):
        # Mostramos órdenes que están Pendientes O En Proceso
        return Orden.objects.filter(
            Q(estado='Pendiente') | Q(estado='En Proceso')
        ).select_related('paciente').order_by('-fecha_creacion')

# --- "Gestionar" (El Hub de Muestras) ---
class MuestraGestionView(PersonalAutorizadoRequiredMixin, UpdateView):
    model = Orden
    # Usamos un formulario "ficticio" porque no editamos la orden, solo sus hijos
    form_class = MuestraUpdateForm # (Podríamos usar un form vacío)
    template_name = 'muestras/muestra_gestion_hub.html'
    context_object_name = 'orden'

    def get_form(self, form_class=None):
        # Sobrescribimos para que no intente cargar un formulario de 'Muestra'
        # con una instancia de 'Orden'.
        return None # No mostramos un formulario principal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Gestionar Muestras - Orden #{self.object.pk}"
        
        # 1. Obtener todos los Tipos de Muestra REQUERIDOS
        examenes_directos = self.object.examenes.all()
        examenes_paquetes = Examen.objects.filter(paquetes__in=self.object.paquetes.all())
        todos_examenes = (examenes_directos | examenes_paquetes).distinct()
        
        tipos_requeridos = TipoMuestra.objects.filter(
            examen__in=todos_examenes
        ).distinct()
        
        # 2. Obtener las Muestras YA REGISTRADAS
        muestras_registradas = self.object.muestras_registradas.all().select_related('tipo_muestra', 'responsable_toma')
        
        # 3. Comparar para encontrar las pendientes
        tipos_registrados_ids = muestras_registradas.values_list('tipo_muestra_id', flat=True)
        
        context['muestras_pendientes'] = tipos_requeridos.exclude(pk__in=tipos_registrados_ids)
        context['muestras_registradas'] = muestras_registradas
        
        return context

class MuestraCreateView(PersonalAutorizadoRequiredMixin, CreateView):
    model = Muestra
    form_class = MuestraCreateForm
    template_name = 'muestras/muestra_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.orden = get_object_or_404(Orden, pk=self.kwargs['orden_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        Pre-llenamos el formulario con valores automáticos.
        """
        initial = super().get_initial()
        # GENERAR CÓDIGO AUTOMÁTICO
        initial['codigo_barras'] = generar_codigo_muestra(self.orden.pk)
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        
        # ===========================================================
        # === LÓGICA DE FILTRADO DE MUESTRAS (SOLO REQUERIDAS) ===
        # ===========================================================
        
        # 1. Recolectar tipos de muestra de EXÁMENES SUELTOS
        ids_requeridos = set(
            self.orden.examenes.values_list('tipo_muestra_id', flat=True)
        )
        
        # 2. Recolectar tipos de muestra de PAQUETES
        for paquete in self.orden.paquetes.all():
            ids_paquete = paquete.examenes.values_list('tipo_muestra_id', flat=True)
            ids_requeridos.update(ids_paquete)
            
        # 3. Obtener tipos YA REGISTRADOS en esta orden
        ids_registrados = set(
            self.orden.muestras_registradas.values_list('tipo_muestra_id', flat=True)
        )
        
        # 4. RESTA: Requeridos - Registrados = Pendientes
        ids_pendientes = list(ids_requeridos - ids_registrados)
        
        # 5. Crear el QuerySet
        tipos_requeridos_qs = TipoMuestra.objects.filter(pk__in=ids_pendientes)
        
        # Pasamos los datos al formulario
        kwargs['tipos_requeridos_qs'] = tipos_requeridos_qs
        kwargs['usuario_actual'] = self.request.user
        
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Registrar Muestra - Orden #{self.orden.pk}"
        context['orden'] = self.orden
        return context

    def form_valid(self, form):
        form.instance.orden = self.orden
        
        # Generar código si no viene
        if not form.instance.codigo_barras:
             form.instance.codigo_barras = generar_codigo_muestra(self.orden.pk)
             
        # 1. Guardar la Muestra
        self.object = form.save()
        
        # =======================================================
        # === NUEVA LÓGICA: ACTIVAR EL PROCESO DE RESULTADOS ===
        # =======================================================
        
        # Si la orden estaba 'Pendiente', ahora pasa a 'En Proceso'
        # porque ya hay al menos una muestra física en el laboratorio.
        if self.orden.estado == 'Pendiente':
            self.orden.estado = 'En Proceso'
            self.orden.save()
            
        # Creamos el objeto Resultado (Encabezado) vacío si no existe.
        # Esto hace que la orden aparezca inmediatamente en "Gestión de Resultados"
        Resultado.objects.get_or_create(orden=self.orden)
        
        messages.success(self.request, f"Muestra registrada. La orden #{self.orden.pk} pasó a 'En Proceso'.")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('muestra_gestion', kwargs={'pk': self.orden.pk})


class MuestraUpdateView(PersonalAutorizadoRequiredMixin, UpdateView):
    model = Muestra
    form_class = MuestraUpdateForm
    template_name = 'muestras/muestra_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Actualizar Muestra: {self.object.tipo_muestra.nombre}"
        context['orden'] = self.object.orden
        return context
    
    def form_valid(self, form):
        self.object = form.save()  # Guarda la muestra
        messages.success(self.request, "Estado de la muestra actualizado.")

        return redirect(reverse('muestra_gestion', kwargs={'pk': self.object.orden.pk}))
