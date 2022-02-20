from django.urls import path
from apps.modulo_logistica import views

urlpatterns = [
    # Productos
    path('catalogo_productos', views.ProductView.as_view(), name='catalogo_productos'),
    
    # Salidas de almacén
    path('salidas_almacen', views.WarehouseExitView.as_view(), name='salidas_almacen'),

    # Inventario
    path('inventario', views.InventoryListView.as_view(), name='inventario'),

    # Bodegas
    path('catalogo_bodegas', views.CatWareView.as_view(), name='catalogo_bodegas'),
    path('crear_bodega', views.WarehouseCreateView.as_view(), name='crear_bodega'),
    path('cargar_bodegas', views.CatWareUploadView.as_view(), name='cargar_bodegas'),
    path('listar_bodegas', views.WarehouseListView.as_view(), name='listar_bodegas'),

    # Actividades
    # Recepción
    path('recepcion', views.ReceptionOrdersView.as_view(), name='recepcion'),

    # Picking pedidos
    path('alistamiento_pedidos', views.PickingOrdersView.as_view(), name='alistamiento_pedidos'),
    
    # Packing pedidos
    path('embalaje', views.PackingOrdersView.as_view(), name='embalaje'),
    
    # Cargue de vehiculos
    path('cargue_vehiculos', views.LoadingTruckOrdersView.as_view(), name='cargue_vehiculos'),
    
    # Conteo de inventario
    path('conteo_inventario', views.InventoryCountView.as_view(), name='conteo_inventario'),
    
    # Remisión de etiquetas
    path('remision_etiquetas', views.remision_etiquetas, name='remision_etiquetas'),
    
    # Ruta de entrega
    path('ruta_entrega', views.DeliveryRouteView.as_view(), name='ruta_entrega'),
    
    # Catálogo de vehiculos
    path('catalogo_vehiculos', views.CatVehicView.as_view(), name='catalogo_vehiculos'),
    path('crear_vehiculo', views.VehicleCreateView.as_view(), name='crear_vehiculo'),
    path('cargar_vehiculos', views.CatVehicUploadView.as_view(), name='cargar_vehiculos'),
    path('listar_vehiculos', views.VehicleListView.as_view(), name='listar_vehiculos'),
    
    # Historico movimientos
    path('hist_mov_logistica', views.hist_mov_logistica, name='hist_mov_logistica'),
    
    # Indicadores
    path('indicadores_almacen', views.LogisticsWarehouseIndicatorsView.as_view(), name='indicadores_almacen'),
    path('indicadores_transporte', views.LogisticsTransportIndicatorsView.as_view(), name='indicadores_transporte'),
    ]