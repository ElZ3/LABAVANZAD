from django.urls import path
from . import views

urlpatterns = [
    # --- CRUD Examen (Principal) ---
    path('gestion/examen/lista/', views.ExamenListView.as_view(), name='examen_list'),
    path('gestion/examen/registrar/', views.ExamenCreateView.as_view(), name='examen_create'),
    path('gestion/examen/editar/<int:pk>/', views.ExamenUpdateView.as_view(), name='examen_update'),
    path('gestion/examen/eliminar/<int:pk>/', views.ExamenDeleteView.as_view(), name='examen_delete'),

    # --- CRUD Metodos (Hijo) ---
    path('gestion/examen/<int:examen_pk>/metodo/registrar/', 
         views.MetodoCreateView.as_view(), 
         name='metodo_create'),
    
    path('gestion/metodo/editar/<int:pk>/', 
         views.MetodoUpdateView.as_view(), 
         name='metodo_update'),
    
    # --- CRUD Valores de Referencia (Hijo) ---
    path('gestion/examen/<int:examen_pk>/valor/registrar/', 
         views.ValorReferenciaCreateView.as_view(), 
         name='valor_referencia_create'),
    
    path('gestion/valor/editar/<int:pk>/', 
         views.ValorReferenciaUpdateView.as_view(), 
         name='valor_referencia_update'),
]