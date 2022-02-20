from django.urls import path
from apps.modulo_comercial import views

urlpatterns = [
    # Rutas vista promociones
    path('promociones/', views.PromotionView.as_view(),name='promociones'),

    # Rutas vista pedidos
    path('pedidos/', views.CreateOrderView.as_view(), name='crear_pedido'),
    path('lista_pedidos/', views.SaleList.as_view(), name='listar_pedidos'),
    #path('sale/invoice/pdf/<int:pk>/', views.SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
    
    # Rutas vista cotizaciones
    path('cotizaciones/', views.CreateQuoteView.as_view(), name='crear_cotizacion_comercial'),
    path('lista_cotizaciones/', views.QuoteList.as_view(), name='listar_cotizaciones'),

    # Ruta vista productos
    path('productos/', views.ProductView.as_view(),name='productos'),
    
    # Ruta vista visitas
    path('ruta_visitas/', views.VisitsRouteView.as_view(),name='ruta_visitas'),

    # Ruta vista llamadas
    path('listar_llamadas/', views.CallCustomerView.as_view(),name='listar_llamadas'),
    path('agenda_llamadas/', views.CreateCallCustomerView.as_view(),name='agenda_llamadas'),

    # Rutas vista cliente
    path('cliente/catalogo', views.clsMenuCatalogoClientesViw.as_view(), name='cat_cliente'),
    path('cliente/crear', views.CustomerCreateView.as_view(), name='crear_cliente'),
    path('cliente/listado', views.CustomerListView.as_view(), name='listar_clientes'),
    path('cliente/actualizar', views.CustomerUpdateView.as_view(), name='editar_cliente'),
    path('cliente/cargar', views.CatCliUploadView.as_view(), name='cargar_clientes'),

    path('cliente/categoria/listado', views.CategoryCustListView.as_view(), name='crear_cat_cliente'),

    path('cliente/zona/', views.ZoneCliView.as_view(), name='crear_zona_cliente'),
    
    path('cliente/asesor/', views.AdvisorCliView.as_view(), name='crear_asesor_cliente'),
    
    # Ruta vista cartera cliente
    path('cliente/cartera/', views.CarteraCliView.as_view(), name='cartera_cliente'),
    
    # Ruta vista historico
    path('historico_mov_comercial/', views.historico_mov_comercial, name='historico_mov_comercial'),
    
    # Ruta vista indicadores
    path('indicadores_comerciales/', views.CommercialIndicatorsView.as_view(), name='indicadores_comerciales'),

    # Ruta para pruebas
    #path('select_anidados/', views.Select2.as_view(),name='select_anidados'),
    ]