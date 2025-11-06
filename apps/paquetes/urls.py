from django.urls import path
from . import views

app_name = 'paquetes'

urlpatterns = [
    # CRUD Paquete
    path('gestion/paquete/lista/', views.PaqueteListView.as_view(), name='paquete_list'),
    path('gestion/paquete/registrar/', views.PaqueteCreateView.as_view(), name='paquete_create'),
    path('gestion/paquete/editar/<int:pk>/', views.PaqueteUpdateView.as_view(), name='paquete_update'),
    path('gestion/paquete/eliminar/<int:pk>/', views.PaqueteDeleteView.as_view(), name='paquete_delete'),
    path('gestion/paquete/ver/<int:pk>/', views.PaqueteDetailView.as_view(), name='paquete_detail'),
    
    # CRUD PaqueteExamen (gestión individual)
    path('gestion/paquete-examen/editar/<int:pk>/', 
         views.PaqueteExamenUpdateView.as_view(), 
         name='paquete_examen_update'),
]