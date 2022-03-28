from django.urls import path
from apps.modulo_comercial import views

urlpatterns = [
    # Promociones
    path(
        'ver_promociones/', 
        views.clsVerPromocionesViw.as_view(),
        name='ver_promociones'
        ),

    # Menu pedidos
    path(
        'menu_pedidos/', 
        views.clsMenuPedidosViw.as_view(), 
        name='menu_pedidos'
        ),   
    # Crear pedido
    path(
        'crear_pedido/', 
        views.clsCrearPedidoViw.as_view(), 
        name='crear_pedido'
        ),
    # Ver pedidos
    path(
        'ver_pedidos/', 
        views.clsVerPedidosViw.as_view(), 
        name='ver_pedidos'
        ),
    # Imprimir pedido
    #path(
    # 'sale/invoice/pdf/<int:pk>/', 
    # views.clsImprimirPedidoPdfViw.as_view(), 
    # name='sale_invoice_pdf'
    # ),
    
    # Exportar pedido

    # Menu cotizaciones
    path(
        'menu_cotizaciones/', 
        views.clsMenuCotizacionesViw.as_view(), 
        name='menu_cotizaciones'
        ),
    # Crear cotización
    path(
        'crear_cotizacion/', 
        views.clsCrearCotizacionViw.as_view(), 
        name='crear_cotizacion'
        ),
    # Ver cotización
    path(
        'ver_cotizaciones/', 
        views.clsVerCotizacionesViw.as_view(),
        name='ver_cotizaciones'
        ),

    # Ver productos
    path(
        'ver_productos/', 
        views.clsVerCatalogoProductosViw.as_view(),
        name='ver_productos'
        ),
    
    # Menu agenda llamadas
    path(
        'menu_llamadas/', 
        views.clsMenuLlamadasViw.as_view(), 
        name='menu_llamadas'
        ),
    # Crear llamada
    path(
        'crear_llamada/', 
        views.clsCrearLlamadaView.as_view(),
        name='crear_llamada'
        ),
    # Ver agenda de llamadas
    path(
        'ver_agenda_llamadas/', 
        views.clsVerAgendaLlamadasViw.as_view(),
        name='ver_agenda_llamadas'
        ),

    # Menu catálogo clientes
    path(
        'catalogo_clientes', 
        views.clsMenuCatalogoClientesViw.as_view(), 
        name='catalogo_clientes'
        ),
    # Opciones catálogo clientes
    path(
        'opciones_cliente',
        views.clsOpcionesCatalogoClientesViw.as_view(), 
        name='opciones_cliente'
        ),
    # Exportar plantilla cliente
    path(
        'exportar_plantilla', 
        views.clsExportarPlantillaClientesViw.as_view(), 
        name='exportar_plantilla'
        ),
    # Importar catálogo clientes
    path(
        'importar_catalogo_clientes', 
        views.clsExportarPlantillaClientesViw.as_view(), 
        name='importar_catalogo_clientes'
        ),
    # Crear cliente
    path(
        'crear_cliente', 
        views.clsCrearClienteViw.as_view(), 
        name='crear_cliente'
        ),
    # Ver cliente
    path(
        'listar_clientes', 
        views.clsListarCatalogoClientesViw.as_view(), 
        name='listar_clientes'
        ),
    # Editar cliente
    path(
        'actualizar_cliente/<int:pk>/', 
        views.clsEditarClienteViw.as_view(), 
        name = 'actualizar_cliente'
        ),
    # Exportar catálogo clientes
    path(
        'exportar_catalogo_clientes/', 
        views.clsExportarCatalogoClientesViw.as_view(), 
        name='exportar_catalogo_clientes'
        ),
    
    # Ver cartera cliente
    path(
        'cartera_clientes/', 
        views.clsCarteraClientesViw.as_view(), 
        name='cartera_clientes'
        ),
    
    # Ver tubería cliente
    path(
        'tuberia_clientes/', 
        views.clsTuberiaClientesViw.as_view(), 
        name='tuberia_clientes'
        ),
    
    # Ver pqr cliente
    path(
        'pqr_clientes/', 
        views.clsPqrClientesViw.as_view(), 
        name='pqr_clientes'
        ),

    ]