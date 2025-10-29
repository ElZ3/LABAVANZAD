from django.views.generic import ListView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms

class PaqueteForm(forms.Form):
    """Simula el formulario para registrar/editar paquetes de servicios."""
    nombre = forms.CharField(
        label="Nombre del Paquete",
        max_length=100,
        initial="Paquete Básico de Chequeo"
    )
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea, # Para el campo 'text' (área de texto)
        initial="Incluye hematología completa, química sanguínea y examen de orina."
    )
    precio = forms.DecimalField(
        label="Precio (CLP)",
        max_digits=8,
        decimal_places=2,
        initial=25000.00
    )

# --- Vistas para el CRUD de Paquetes (Funcionalidad Ciega) ---

class paqueteListView(ListView):
    """Muestra la tabla de paquetes."""
    template_name = 'paquetes/paquete_lista.html'
    context_object_name = 'paquetes'
    
    # ESTO ES LO CRUCIAL: La función de simulación
    def get_queryset(self):
        # Simulación de datos de lista para evitar ImproperlyConfigured
        class MockPaquete:
            def __init__(self, pk, nombre, precio):
                self.pk = pk
                self.nombre = nombre
                self.descripcion = "Descripción simulada..."
                self.precio = precio
        return [
            MockPaquete(301, 'Chequeo General', 35000.00),
            MockPaquete(302, 'Perfil Lipídico', 12500.00),
            MockPaquete(303, 'Paquete Materno', 48000.00),
        ]
    
class paqueteCreateView(FormView):
    """Muestra el formulario para registrar un nuevo paquete."""
    template_name = 'paquetes/paquete_registrar.html'
    form_class = PaqueteForm
    success_url = reverse_lazy('paquete_list')

class paqueteUpdateView(UpdateView):
    """Muestra el formulario para editar un paquete existente."""
    template_name = 'paquetes/paquete_form.html'
    form_class = PaqueteForm
    success_url = reverse_lazy('paquete_list')

    def get_object(self, queryset=None):
        # Simula la recuperación de un objeto (necesario para el título de la vista)
        class MockObject:
            pk = self.kwargs['pk']
        return MockObject()

    def get_initial(self):
        initial = super().get_initial()
        # Simulación de precarga para la edición
        initial['nombre'] = "Paquete Premium de Edición"
        initial['precio'] = 99999.99
        return initial

class paqueteDeleteView(DeleteView):
    """Muestra la confirmación de eliminación de un paquete."""
    template_name = 'paquetes/paquete_confirm_delete.html'
    success_url = reverse_lazy('paquete_list')

    def get_object(self, queryset=None):
        # Simula la recuperación del objeto para la confirmación
        class MockObject:
            pk = self.kwargs['pk']
            # Campo para el mensaje de confirmación
            nombre = 'Paquete de Descarte' 
        return MockObject()