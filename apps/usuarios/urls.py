from django.urls import path
from . import views

urlpatterns = [
        # Autenticación
        path('login/', views.login_view, name='login'),
        path('logout/', views.logout_view, name='logout'),
    
        # CRUD de Administrador
        path('gestion/usuarios/lista/', views.UserListView.as_view(), name='user_list'),
        path('gestion/usuarios/registrar/', views.UserCreateView.as_view(), name='user_create'),
        path('gestion/usuarios/editar/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
        path('gestion/usuarios/eliminar/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),

        # Perfil de Usuario
        path('perfil/', views.ProfileView.as_view(), name='profile'),
        path('perfil/editar/', views.ProfileUpdateView.as_view(), name='profile_update'),
    ]
    
