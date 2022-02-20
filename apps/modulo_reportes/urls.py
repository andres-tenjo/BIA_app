from django.urls import path
from apps.modulo_reportes import views

urlpatterns = [
    path('reportes_generales', views.reportes_generales, name='reportes_generales'),
    path('reportes_modulo_comercial', views.reportes_modulo_comercial, name='reportes_modulo_comercial'),
    path('reportes_modulo_compras', views.reportes_modulo_compras, name='reportes_modulo_compras'),
    path('reportes_modulo_almacen', views.reportes_modulo_almacen, name='reportes_modulo_almacen'),
    path('reportes_modulo_transporte', views.reportes_modulo_transporte, name='reportes_modulo_transporte'),
    path('reportes_costos', views.reportes_costos, name='reportes_costos'),
    ]