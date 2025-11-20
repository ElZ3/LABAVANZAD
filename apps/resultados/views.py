from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.db.models import Q

from ordenes.models import Orden
from examenes.models import Examen, ValorReferencia
from .models import Resultado, ResultadoDetalle
from .forms import ResultadoHeaderForm
from ordenes.views import PersonalAutorizadoRequiredMixin

# --- LISTA 1: GESTIÓN DE RESULTADOS (Solo Pendientes) ---
class ResultadoListView(PersonalAutorizadoRequiredMixin, ListView):
    model = Orden
    template_name = 'resultados/resultado_lista.html'
    context_object_name = 'ordenes'
    
    def get_queryset(self):
        # Solo mostramos órdenes cuyo resultado esté en 'Pendiente' (o no exista aún)
        # Y que la orden ya tenga muestras tomadas ('En Proceso')
        return Orden.objects.filter(
            estado='En Proceso',
            resultado__estado='Pendiente'
        ).select_related('paciente', 'resultado').order_by('-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Ingreso de Resultados (Pendientes)"
        return context

# --- LISTA 2: VALIDACIONES (Solo En Espera) ---
class ValidacionListView(PersonalAutorizadoRequiredMixin, ListView):
    model = Resultado
    template_name = 'resultados/validacion_lista.html'
    context_object_name = 'resultados'
    
    def get_queryset(self):
        # REQUISITO: Solo Jefes/Admins
        roles_validadores = ['Jefe de Laboratorio', 'Administrador']
        if not self.request.user.rol.nombre in roles_validadores:
            raise PermissionDenied("Acceso denegado.")
        
        # Solo mostramos resultados que ya fueron llenados ('En Espera')
        return Resultado.objects.filter(
            estado='En Espera'
        ).select_related('orden', 'orden__paciente').order_by('fecha_emision')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Bandeja de Validación"
        return context

# --- VISTA DE FORMULARIO (El Hub Inteligente) ---
class ResultadoIngresoView(PersonalAutorizadoRequiredMixin, UpdateView):
    model = Resultado
    form_class = ResultadoHeaderForm
    template_name = 'resultados/resultado_form.html'
    context_object_name = 'resultado'

    def get_object(self):
        orden_pk = self.kwargs.get('orden_pk')
        orden = get_object_or_404(Orden, pk=orden_pk)
        resultado, created = Resultado.objects.get_or_create(orden=orden)
        return resultado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orden = self.object.orden
        
        # (Lógica de búsqueda de parámetros igual que antes...)
        examenes_directos_q = Q(ordenes=orden)
        examenes_paquetes_q = Q(paquetes__in=orden.paquetes.all())
        todos_examenes = Examen.objects.filter(examenes_directos_q | examenes_paquetes_q).distinct()
        
        context['parametros_list'] = ValorReferencia.objects.filter(
            examen__in=todos_examenes, estado='Activo'
        ).select_related('examen')
        
        detalles = ResultadoDetalle.objects.filter(resultado=self.object)
        context['detalles_map'] = {d.valor_referencia.pk: d.valor_obtenido for d in detalles}
        
        context['titulo'] = f"Resultados - Orden #{orden.pk}"
        context['orden'] = orden
        
        # PERMISOS
        roles_validadores = ['Jefe de Laboratorio', 'Administrador']
        es_jefe = self.request.user.rol and self.request.user.rol.nombre in roles_validadores
        
        # Determinar qué botones mostrar según el estado
        context['modo_ingreso'] = self.object.estado == 'Pendiente'
        context['modo_validacion'] = self.object.estado == 'En Espera' and es_jefe
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        context = self.get_context_data()
        
        # 1. Guardar Valores (Detalles)
        for param in context['parametros_list']:
            val = request.POST.get(f'valor_obtenido_{param.pk}', '').strip()
            if val:
                ResultadoDetalle.objects.update_or_create(
                    resultado=self.object, valor_referencia=param,
                    defaults={'valor_obtenido': val}
                )
            else:
                ResultadoDetalle.objects.filter(resultado=self.object, valor_referencia=param).delete()

        if form.is_valid():
            resultado = form.save(commit=False)
            
            # --- LÓGICA DE BOTONES ---
            
            # A. Técnico guarda borrador (Sigue en Pendiente)
            if 'guardar_borrador' in request.POST:
                resultado.estado = 'Pendiente'
                messages.info(request, "Borrador guardado. Sigue en tu bandeja.")
                resultado.save()
                return redirect(reverse('resultado_ingreso', kwargs={'orden_pk': resultado.orden.pk}))

            # B. Técnico envía a validar (Pasa a En Espera -> Desaparece de su lista)
            elif 'enviar_validacion' in request.POST:
                resultado.estado = 'En Espera'
                messages.success(request, "Resultados enviados a validación.")
                resultado.save()
                return redirect(reverse('resultado_lista')) # Vuelve a su lista

            # C. Jefe devuelve a corrección (Regresa a Pendiente)
            elif 'devolver_correccion' in request.POST:
                resultado.estado = 'Pendiente'
                resultado.validado_por = None
                messages.warning(request, "Resultados devueltos al técnico para corrección.")
                resultado.save()
                return redirect(reverse('validacion_lista'))

            # D. Jefe valida (Pasa a Validado -> Orden Completada)
            elif 'validar_finalizar' in request.POST:
                if not context['modo_validacion']:
                    raise PermissionDenied
                
                resultado.estado = 'Validado'
                resultado.validado_por = request.user
                resultado.fecha_validacion = timezone.now()
                resultado.orden.estado = 'Completada'
                resultado.orden.save()
                resultado.save()
                messages.success(request, "Orden finalizada y validada exitosamente.")
                return redirect(reverse('validacion_lista'))

            return redirect(reverse('orden_update', kwargs={'pk': resultado.orden.pk}))
        else:
            return self.form_invalid(form)