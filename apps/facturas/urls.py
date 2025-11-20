from django.urls import path
from . import views

urlpatterns = [
    path('gestion/orden/<int:orden_pk>/generar_factura/', views.FacturaCreateView.as_view(), name='factura_create'),
    path('gestion/factura/<int:pk>/', views.FacturaDetailView.as_view(), name='factura_detalle'),
    
    # Nueva Ruta PDF
    path('gestion/factura/<int:pk>/pdf/', views.FacturaPDFView.as_view(), name='factura_pdf'),
]