# [tu_app]/views.py (Añadir estas clases debajo de las de Orden)

from django.views.generic import ListView, FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django import forms


# Paso 1: Crear un "Modelo" de Formulario simple para el CRUD de Muestras
class MuestraForm(forms.Form):
    # Definimos los campos que se renderizan manualmente en muestra_form.html
    tipo = forms.ChoiceField(
        choices=[('Sangre', 'Sangre'), ('Orina', 'Orina'), ('Heces', 'Heces')], initial='Sangre'
    )
    fecha_toma = forms.DateTimeField(
        label="Fecha y Hora de Toma", initial="2025-10-23T09:00"
    )
    responsable = forms.CharField(
        label="Responsable de la Toma", max_length=100, initial="Lab. Supervisor"
    )
    estado = forms.ChoiceField(
        choices=[('Recibida', 'Recibida'), ('En Análisis', 'En Análisis'), ('Descartada', 'Descartada')], initial='Recibida'
    )
## --- Vistas para el CRUD de Muestras (Funcionalidad Ciega) ---

class muestraListView(ListView):
    template_name = 'muestras/muestra_list.html'
    context_object_name = 'muestras'
    def get_queryset(self):
        # Devuelve una lista vacía que disparará el bloque {% empty %} en tu HTML
        # Si quisieras ver filas, simplemente devuelve objetos simulados aquí.
        return []


class muestraCreateView(FormView): # Usa FormView para CREATE
    template_name = 'muestras/muestra_registrar.html'
    form_class = MuestraForm
    success_url = reverse_lazy('muestra_list')


class muestraUpdateView(UpdateView): # Usa UpdateView para UPDATE
    template_name = 'muestras/muestra_editar.html'
    form_class = MuestraForm
    success_url = reverse_lazy('muestra_list')

    # Truco OBLIGATORIO: Simula la recuperación de un objeto (con PK para el título)
    def get_object(self, queryset=None):
        class MockObject:
            pk = self.kwargs['pk']
        return MockObject()
    
    # Truco: Sobreescribe los datos iniciales para simular la edición
    def get_initial(self):
        initial = super().get_initial()
        # Simula que la muestra editada tiene el tipo "Heces"
        initial['tipo'] = 'Heces' 
        return initial


class muestraDeleteView(DeleteView):
    template_name = 'muestras/muestra_confirm_delete.html'
    success_url = reverse_lazy('muestra_list')

    # Truco OBLIGATORIO: Simula la recuperación de un objeto para la confirmación
    def get_object(self, queryset=None):
        class MockObject:
            pk = self.kwargs['pk']
            # Necesitas un campo para el mensaje de confirmación
            tipo = 'Sangre (Simulada)' 
        return MockObject()