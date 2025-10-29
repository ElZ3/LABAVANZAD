from django.urls import path
from . import views
    
urlpatterns = [
        # Rutas para el CRUD de Categorías
        path('gestion/categoria/lista/', views.CategoriaExamenListView.as_view(), name='categoria_list'),
        path('gestion/categoria/registrar/', views.CategoriaExamenCreateView.as_view(), name='categoria_create'),
        path('gestion/categoria/editar/<int:pk>/', views.CategoriaExamenUpdateView.as_view(), name='categoria_update'),
        path('gestion/categoria/eliminar/<int:pk>/', views.CategoriaExamenDeleteView.as_view(), name='categoria_delete'),
    ]
    
