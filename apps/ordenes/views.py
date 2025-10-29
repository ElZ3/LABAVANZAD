# [tu_app]/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django import forms
from django.forms import ModelForm

# Paso 1: Crear un "Modelo" de Formulario simple para el CRUD
# Usamos un Form normal ya que no queremos que interactúe con la DB.
# Esto solo sirve para simular la existencia de un "form" en el contexto de las vistas.

class OrdenForm(forms.Form):
    # Definimos los campos mínimos para que la plantilla 'orden_form.html' no falle
    # Los tipos de campo corresponden a los que tu HTML espera:
    paciente_id = forms.IntegerField(label="Paciente ID", initial=1)
    convenio_id = forms.IntegerField(label="Convenio ID", initial=1)
    fecha_creacion = forms.DateTimeField(label="Fecha de Creación", initial="2025-10-22T10:00")
    metodo_entrega = forms.ChoiceField(
        choices=[('Email', 'Email'), ('Impreso', 'Impreso')], initial='Impreso'
    )
    prioridad = forms.ChoiceField(
        choices=[('Rutina', 'Rutina'), ('Preferente', 'Preferente'), ('Urgente', 'Urgente')], initial='Rutina'
    )
    estado = forms.ChoiceField(
        choices=[('Pendiente', 'Pendiente'), ('En Proceso', 'En Proceso'), ('Completada', 'Completada'), ('Cancelada', 'Cancelada')], initial='Pendiente'
    )

    # Nota: Si estuvieras usando ModelForm, esta simulación no sería necesaria.


# --- Vistas para el CRUD de Órdenes (Funcionalidad Ciega) ---

class ordenListView(ListView):
    # La vista que muestra la tabla con el botón de Registro
    template_name = 'ordenes/orden_lista.html'
    context_object_name = 'ordenes'

    # Truco: Sobreescribir get_queryset para devolver una lista vacía
    def get_queryset(self):
        # Devuelve una lista vacía que disparará el bloque {% empty %} en tu HTML
        # Si quisieras ver filas, simplemente devuelve objetos simulados aquí.
        return []

    # Truco 2: Simular un objeto de datos (solo si necesitas un ejemplo en la lista)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Objetos simulados para ver la estructura de la tabla
    #     class MockOrden:
    #         pk = 901
    #         paciente_id = 1
    #         fecha_creacion = '2025-10-22 10:00:00'
    #         prioridad = 'Urgente'
    #         estado = 'Pendiente'
    #         def __str__(self): return f"Orden #{self.pk}"
    #     context['ordenes'] = [MockOrden()]
    #     return context


class ordenCreateView(FormView): # <--- CAMBIO CLAVE
    # La vista que muestra el formulario de registro
    template_name = 'ordenes/orden_registrar.html'
    form_class = OrdenForm        # Usamos el Formulario simulado
    success_url = reverse_lazy('orden_list')


class ordenUpdateView(UpdateView):
    # La vista que muestra el formulario de edición (necesita un objeto ficticio)
    template_name = 'ordenes/orden_editar.html'
    form_class = OrdenForm
    success_url = reverse_lazy('orden_list')

    # Truco: Simular la recuperación de un objeto para que la vista no falle
    def get_object(self, queryset=None):
        # Simula un objeto con la PK pasada por la URL
        class MockObject:
            pk = self.kwargs['pk']
        return MockObject()
    
    # Truco: Pasar datos iniciales al formulario (simular precarga)
    def get_initial(self):
        initial = super().get_initial()
        # Puedes añadir valores iniciales basados en MockObject si lo necesitas
        # initial['paciente_id'] = 5 
        return initial


class ordenDeleteView(DeleteView):
    # La vista que muestra la confirmación de eliminación
    template_name = 'ordenes/orden_confirm_delete.html'
    success_url = reverse_lazy('orden_list')

    # Truco: Simular la recuperación de un objeto para que la vista no falle
    def get_object(self, queryset=None):
        # Simula un objeto con la PK pasada por la URL
        class MockObject:
            pk = self.kwargs['pk']
            # Necesitas un campo simple para el mensaje de confirmación
            fecha_creacion = '2025-10-22 10:00:00' 
        return MockObject()