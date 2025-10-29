from django.urls import path
from . import views

urlpatterns = [
    # Rutas para el CRUD de Ordenes
    path('gestion/ordenes/lista/', views.ordenListView.as_view(), name='orden_list'),
    path('gestion/ordenes/registrar/', views.ordenCreateView.as_view(), name='orden_create'),
    path('gestion/ordenes/editar/<int:pk>/', views.ordenUpdateView.as_view(), name='orden_update'),
    path('gestion/ordenes/eliminar/<int:pk>/', views.ordenDeleteView.as_view(), name='orden_delete'),
]

