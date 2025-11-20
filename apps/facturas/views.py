import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.staticfiles import finders
from django.views.generic import CreateView, DetailView, View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone

# Importamos xhtml2pdf
from xhtml2pdf import pisa

from ordenes.models import Orden
from .models import Factura
from .forms import FacturaForm
from .utils import generar_numero_factura
from ordenes.views import PersonalAutorizadoRequiredMixin

# --- FUNCIÓN DE AYUDA PARA ESTÁTICOS (Necesaria para xhtml2pdf) ---
def link_callback(uri, rel):
    """
    Convierte URLs de HTML (ej: /static/css/style.css) a rutas absolutas
    del sistema de archivos (C:\Protecto\static\css\style.css) para que
    xhtml2pdf pueda encontrarlos.
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path=result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

    # Asegurarse de que el archivo exista
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

# --- VISTAS ---

class FacturaPDFView(PersonalAutorizadoRequiredMixin, View):
    def get(self, request, pk):
        factura = get_object_or_404(Factura, pk=pk)
        orden = factura.orden
        
        template_path = 'facturas/factura_pdf.html'
        context = {
            'factura': factura,
            'items_examen': orden.ordenexamen_set.select_related('examen').all(),
            'items_paquete': orden.ordenpaquete_set.select_related('paquete').all(),
            'fecha_impresion': timezone.now(),
            'empresa': {
                'nombre': 'Laboratorio Clínico Avanzado',
                'direccion': 'Calle Principal #123, San Salvador',
                'telefono': '2222-0000',
                'email': 'info@labavanzado.com'
            }
        }
        
        # Crear respuesta Django
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Factura_{factura.numero_factura}.pdf"'
        
        # Buscar template
        template = get_template(template_path)
        html = template.render(context)

        # Crear PDF
        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback
        )

        # Si hay error
        if pisa_status.err:
            return HttpResponse('Tuvimos algunos errores <pre>' + html + '</pre>')
            
        return response

# (El resto de vistas CreateView y DetailView se quedan IGUAL que antes)
class FacturaCreateView(PersonalAutorizadoRequiredMixin, CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'facturas/factura_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.orden = get_object_or_404(Orden, pk=self.kwargs['orden_pk'])
        if hasattr(self.orden, 'factura'):
            messages.error(request, "Esta orden ya tiene una factura asociada.")
            return redirect(reverse('orden_update', kwargs={'pk': self.orden.pk}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Generar Factura Automática - Orden #{self.orden.pk}"
        context['orden'] = self.orden
        tipo = 'Convenio' if self.orden.convenio else 'Particular'
        context['proximo_numero'] = generar_numero_factura(tipo)
        return context

    def form_valid(self, form):
        factura = form.save(commit=False)
        factura.orden = self.orden
        factura.creado_por = self.request.user
        
        if self.orden.convenio:
            factura.tipo_factura = 'Convenio'
            factura.cliente_nombre = self.orden.convenio.nombre
        else:
            factura.tipo_factura = 'Particular'
            factura.cliente_nombre = f"{self.orden.paciente.nombre} {self.orden.paciente.apellido}"
            factura.cliente_dui = self.orden.paciente.dui
            
        factura.numero_factura = generar_numero_factura(factura.tipo_factura)
        factura.subtotal = self.orden.subtotal
        factura.descuento = self.orden.descuento_aplicado
        factura.iva = self.orden.iva
        factura.total = self.orden.total_con_iva
        factura.estado = self.orden.estado_pago
        
        factura.save()
        messages.success(self.request, f"Factura {factura.numero_factura} generada correctamente.")
        return redirect(reverse('factura_detalle', kwargs={'pk': factura.pk}))

class FacturaDetailView(PersonalAutorizadoRequiredMixin, DetailView):
    model = Factura
    template_name = 'facturas/factura_detalle.html'
    context_object_name = 'factura'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Factura {self.object.numero_factura}"
        context['items_examen'] = self.object.orden.ordenexamen_set.all()
        context['items_paquete'] = self.object.orden.ordenpaquete_set.all()
        return context