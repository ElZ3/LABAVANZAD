# [tu_app]/urls.py

from django.urls import path
from . import views

urlpatterns = [

    path('gestion/resultados/lista', views.resultadoListView.as_view(), name='resultado_list'),
    path('resultados/registrar/', views.resultadoCreateView.as_view(), name='resultado_create'),
    path('resultados/editar/<int:pk>/', views.resultadoUpdateView.as_view(), name='resultado_update'),
    path('resultados/eliminar/<int:pk>/', views.resultadoDeleteView.as_view(), name='resultado_delete'),
]