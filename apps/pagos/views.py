from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView
from ordenes.models import Orden
from .models import Pago
from .forms import PagoForm

# Asumiendo que el mixin de 'ordenes' es el correcto
from ordenes.views import PersonalAutorizadoRequiredMixin

class PagoCreateView(PersonalAutorizadoRequiredMixin, CreateView):
    """
    Esta vista NO tiene su propio template. Es una vista de 'acción'
    que se llama desde el 'HUB' de la Orden.
    """
    model = Pago
    form_class = PagoForm

    def dispatch(self, request, *args, **kwargs):
        self.orden = get_object_or_404(Orden, pk=self.kwargs['orden_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Asignamos la orden y el usuario
        form.instance.orden = self.orden
        form.instance.registrado_por = self.request.user
        
        # Guardamos el pago
        pago = form.save()
        
        # ¡Importante! Actualizamos el estado de pago de la orden
        self.orden.actualizar_estado_pago() 
        
        messages.success(self.request, f"Pago de ${pago.monto} registrado exitosamente.")
        # Redirigimos de vuelta al "HUB" de la orden
        return redirect(reverse('orden_update', kwargs={'pk': self.orden.pk}))

    def form_invalid(self, form):
        messages.error(self.request, "Error al registrar el pago. Revisa el monto.")
        return redirect(reverse('orden_update', kwargs={'pk': self.orden.pk}))