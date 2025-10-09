from django.urls import path
from . import views

urlpatterns = [
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/registro/', views.registro_paciente, name='registro_paciente'),
]