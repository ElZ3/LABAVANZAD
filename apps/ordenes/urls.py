from django.urls import path
from . import views

urlpatterns = [
    # --- CRUD Orden (Principal) ---
    path('gestion/orden/lista/', views.OrdenListView.as_view(), name='orden_lista'),
    path('gestion/orden/registrar/', views.OrdenCreateView.as_view(), name='orden_create'),
    path('gestion/orden/editar/<int:pk>/', views.OrdenUpdateView.as_view(), name='orden_update'),
    
    # --- Vistas de ACCIÓN (Añadir/Quitar) ---
    path('gestion/orden/<int:orden_pk>/add_examen/', 
         views.AddExamenToOrdenView.as_view(), 
         name='orden_add_examen'),
         
    path('gestion/orden/<int:orden_pk>/add_paquete/', 
         views.AddPaqueteToOrdenView.as_view(), 
         name='orden_add_paquete'),
         
    path('gestion/orden/<int:orden_pk>/remove_examen/<int:examen_pk>/', 
         views.RemoveExamenFromOrdenView.as_view(), 
         name='orden_remove_examen'),
    
    path('gestion/orden/<int:orden_pk>/remove_paquete/<int:paquete_pk>/', 
         views.RemovePaqueteFromOrdenView.as_view(), 
         name='orden_remove_paquete'),
]