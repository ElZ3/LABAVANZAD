# [tu_app]/urls.py (Agregando estas líneas a tu urlpatterns)

from django.urls import path
from . import views

urlpatterns = [

    # URLs para Paquetes
    path('gestion/paquetes/lista/', views.paqueteListView.as_view(), name='paquete_list'),
    path('gestion/paquetes/registrar/', views.paqueteCreateView.as_view(), name='paquete_create'),
    path('gestion/paquetes/editar/<int:pk>/', views.paqueteUpdateView.as_view(), name='paquete_update'),
    path('gestion/paquetes/eliminar/<int:pk>/', views.paqueteDeleteView.as_view(), name='paquete_delete'),
]