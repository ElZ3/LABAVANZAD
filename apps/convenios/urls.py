from django.urls import path
from . import views

urlpatterns = [
    # Convenio Principal
    path('gestion/convenios/', views.ConvenioListView.as_view(), name='convenio_list'),
    path('gestion/convenios/crear/', views.ConvenioCreateView.as_view(), name='convenio_create'),
    path('gestion/convenios/editar/<int:pk>/', views.ConvenioUpdateView.as_view(), name='convenio_update'),
    path('gestion/convenios/eliminar/<int:pk>/', views.ConvenioDeleteView.as_view(), name='convenio_delete'),
    
    # EL HUB (Detalle)
    path('gestion/convenios/detalle/<int:pk>/', views.ConvenioDetailView.as_view(), name='convenio_detail'),

    # Excepciones Exámenes
    path('gestion/convenios/<int:convenio_pk>/agregar-examen/', 
         views.ConvenioExamenCreateView.as_view(), name='add_desc_examen'),
    path('gestion/convenios/eliminar-examen/<int:pk>/', 
         views.ConvenioExamenDeleteView.as_view(), name='del_desc_examen'),

    # Excepciones Paquetes
    path('gestion/convenios/<int:convenio_pk>/agregar-paquete/', 
         views.ConvenioPaqueteCreateView.as_view(), name='add_desc_paquete'),
    path('gestion/convenios/eliminar-paquete/<int:pk>/', 
         views.ConvenioPaqueteDeleteView.as_view(), name='del_desc_paquete'),
]