from django.urls import path
from . import views

urlpatterns = [
    # /gestion/orden/10/registrar_pago/
    path('gestion/orden/<int:orden_pk>/registrar_pago/', 
         views.PagoCreateView.as_view(), 
         name='pago_create'),
]