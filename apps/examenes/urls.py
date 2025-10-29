from django.urls import path
from . import views

urlpatterns = [
    # Rutas para el CRUD de Exámenes
    # (Ya no contiene las rutas de Categoría)
    path('gestion/examenes/lista/', views.ExamenListView.as_view(), name='examen_list'),
    path('gestion/examenes/registrar/', views.ExamenCreateView.as_view(), name='examen_create'),
    path('gestion/examenes/editar/<int:pk>/', views.ExamenUpdateView.as_view(), name='examen_update'),
    path('gestion/examenes/eliminar/<int:pk>/', views.ExamenDeleteView.as_view(), name='examen_delete'),
]

