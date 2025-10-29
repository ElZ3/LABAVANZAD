from django.urls import path
from . import views

urlpatterns = [
        # CRUD de Pacientes
        path('gestion/pacientes/lista/', views.PacienteListView.as_view(), name='paciente_list'),
        path('gestion/pacientes/registrar/', views.PacienteCreateView.as_view(), name='paciente_create'),
        path('gestion/pacientes/editar/<int:pk>/', views.PacienteUpdateView.as_view(), name='paciente_update'),
        path('gestion/pacientes/eliminar/<int:pk>/', views.PacienteDeleteView.as_view(), name='paciente_delete'),
    ]
    
