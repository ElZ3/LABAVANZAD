from django.urls import path
from . import views

urlpatterns = [
        # CRUD de Convenios
        path('gestion/convenios/lista/', views.ConvenioListView.as_view(), name='convenio_list'),
        path('gestion/convenios/registrar/', views.ConvenioCreateView.as_view(), name='convenio_create'),
        path('gestion/convenios/editar/<int:pk>/', views.ConvenioUpdateView.as_view(), name='convenio_update'),
        path('gestion/convenios/eliminar/<int:pk>/', views.ConvenioDeleteView.as_view(), name='convenio_delete'),
    ]
    
