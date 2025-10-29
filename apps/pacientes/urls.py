from django.urls import path
from . import views

urlpatterns = [
        # CRUD de Pacientes
        path('gestion/pacientes/lista/', views.PacienteListView.as_view(), name='paciente_list'),
        path('gestion/registrar/', views.PacienteCreateView.as_view(), name='paciente_create'),
        path('gestion/editar/<int:pk>/', views.PacienteUpdateView.as_view(), name='paciente_update'),
        path('gestion/eliminar/<int:pk>/', views.PacienteDeleteView.as_view(), name='paciente_delete'),
    ]
    
