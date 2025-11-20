from django.urls import path
from . import views

urlpatterns = [
    # 2. Submenú: Gestión de Muestras (Lista de Órdenes)
    path('gestion/muestras/lista/', 
         views.MuestraListView.as_view(), 
         name='muestra_lista'),
         
    # "Gestionar" (El Hub de Muestras)
    path('gestion/muestras/gestionar/<int:pk>/', 
         views.MuestraGestionView.as_view(), 
         name='muestra_gestion'),
    
    # --- CRUD Muestras (Acciones) ---
    path('gestion/orden/<int:orden_pk>/muestra/registrar/', 
         views.MuestraCreateView.as_view(), 
         name='muestra_create'),
    
    path('gestion/muestra/editar/<int:pk>/', 
         views.MuestraUpdateView.as_view(), 
         name='muestra_update'),
]