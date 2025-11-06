from django.urls import path
from . import views

urlpatterns = [
    # --- CRUD Muestras (Hijo de Orden) ---
    
    # /gestion/orden/10/muestra/registrar/
    path('gestion/orden/<int:orden_pk>/muestra/registrar/', 
         views.MuestraCreateView.as_view(), 
         name='muestra_create'),
    
    # /gestion/muestra/editar/501/
    path('gestion/muestra/editar/<int:pk>/', 
         views.MuestraUpdateView.as_view(), 
         name='muestra_update'),
    
    # (No implementamos borrado, se anula la orden o se 'Rechaza' la muestra)
]