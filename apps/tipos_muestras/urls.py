from django.urls import path
from . import views

urlpatterns = [
    # Rutas para el CRUD de Tipos de Muestra
    path('gestion/tipo_muestra/lista/', views.TipoMuestraListView.as_view(), name='tipo_muestra_list'),
    path('gestion/tipo_muestra/registrar/', views.TipoMuestraCreateView.as_view(), name='tipo_muestra_create'),
    path('gestion/tipo_muestra/editar/<int:pk>/', views.TipoMuestraUpdateView.as_view(), name='tipo_muestra_update'),
    path('gestion/tipo_muestra/eliminar/<int:pk>/', views.TipoMuestraDeleteView.as_view(), name='tipo_muestra_delete'),
]