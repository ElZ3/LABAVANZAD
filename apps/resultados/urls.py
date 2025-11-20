from django.urls import path
from . import views

urlpatterns = [
    # 3.1 Submenú: Gestión de Resultados (Lista de Órdenes)
    path('gestion/resultados/lista/', 
         views.ResultadoListView.as_view(), 
         name='resultado_lista'),
         
    # 3.2 Submenú: Validaciones (Lista de Resultados)
    path('gestion/validaciones/lista/', 
         views.ValidacionListView.as_view(), 
         name='validacion_lista'),
    
    # "Gestionar" (El Hub de Ingreso/Validación)
    path('gestion/orden/<int:orden_pk>/ingresar_resultados/', 
         views.ResultadoIngresoView.as_view(), 
         name='resultado_ingreso'),
]