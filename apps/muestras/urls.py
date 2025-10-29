# [tu_app]/urls.py (Ejemplo, si estuviera en la misma carpeta)

from django.urls import path
from . import views

urlpatterns = [
    # Rutas para el CRUD de Muestras
    path('gestion/muestras/lista/', views.muestraListView.as_view(), name='muestra_list'),
    path('gestion/muestras/registrar/', views.muestraCreateView.as_view(), name='muestra_create'),
    path('gestion/muestras/editar/<int:pk>/', views.muestraUpdateView.as_view(), name='muestra_update'),
    path('gestion/muestras/eliminar/<int:pk>/', views.muestraDeleteView.as_view(), name='muestra_delete'),
]