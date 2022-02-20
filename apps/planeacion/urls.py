
from django.urls import path
from .views import *

urlpatterns = [
    # Módulo comercial
    # Planeación comercial
    path('plan_comercial', CommercialPlanningMainView.as_view(), name='plan_comercial'),
    path('historico_plan_comercial', HistPlanningComView.as_view(), name='hist_plan_comercial'),
    path('importar_pedidos', OrdersImport.as_view(), name='importar_pedidos'),
    path('planeacion_comercial', CommercialPlanningView.as_view(), name='planeacion_comercial'),
    
    # Planeación de actividades comerciales
    path('plan_act_comercial', CommercialPlanActivitiesView.as_view(), name='plan_act_comercial'),

    # Promociones
    path('promociones', PromotionsView.as_view(), name='promociones'),
    path('crear_promocion', CreatePromotionsView.as_view(), name='crear_promocion'),
    path('listar_promociones', PromotionListView.as_view(), name='listar_promociones'),

    # Novedades
    path('novedades_ventas', SalesNewsView.as_view(), name='novedades_ventas'),
    
    # Tuberia clientes
    # Indicadores comerciales

    # Cartera clientes
    path('cartera_clientes', CarteraCliView.as_view(), name='cartera_clientes'),

    # Módulo compras
    # Planeación compras
    # Planeación comercial
    path('plan_compras', PurchasePlanningMainView.as_view(), name='plan_compras'),
    path('historico_plan_compras', HistPlanningPurchView.as_view(), name='hist_plan_compras'),
    path('planeacion_compras', PurchasePlanningView.as_view(), name='planeacion_compras'),

    # Planeación actividades compras
    path('plan_act_compras', PurchasePlanActivitiesView.as_view(), name='plan_act_compras'),
    
    # Novedades
    path('novedades_compras', PurchaseNewsView.as_view(), name='novedades_compras'),

    # Cartera proveedores
    path('cartera_proveedores', CarteraSuppView.as_view(), name='cartera_proveedores'),

    path('inventario', InventoryListView.as_view(), name='inventario'),
]