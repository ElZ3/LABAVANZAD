from django.urls import path
from . import views

urlpatterns = [
    
    # CRUD de Roles
    path('gestion/roles/lista/', views.RolListView.as_view(), name='rol_list'),
    path('gestion/roles/registrar/', views.RolCreateView.as_view(), name='rol_create'),
    path('gestion/roles/editar/<int:pk>/', views.RolUpdateView.as_view(), name='rol_update'),
    path('gestion/roles/eliminar/<int:pk>/', views.RolDeleteView.as_view(), name='rol_delete'),

]

