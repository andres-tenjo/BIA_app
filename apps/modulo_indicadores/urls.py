from django.urls import path
from apps.modulo_indicadores import views

urlpatterns = [
    path('indicadores_comerciales/', views.CommercialIndicatorsView.as_view(), name='indicadores_comerciales'),
    path('indicadores_compras', views.PurchaseIndicatorsView.as_view(), name='indicadores_compras'),
    path('indicadores_almacen', views.LogisticsWarehouseIndicatorsView.as_view(), name='indicadores_almacen'),
    path('indicadores_transporte', views.LogisticsTransportIndicatorsView.as_view(), name='indicadores_transporte'),
    ]