from django.urls import path
from apps.modulo_compras import views
from django.views.generic import TemplateView


urlpatterns = [

    # Menu negociaciones
    path(
        'menu_negociacion/', 
        views.clsMenuNegociacionProveedoresViw.as_view(), 
        name='menu_negociacion'
        ),
    # Crear negociación
    path(
        'crear_negociacion/', 
        views.clsCrearNegociacionViw.as_view(), 
        name='crear_negociacion'
        ),
    # Ver negociaciones
    path(
        'ver_negociacion/', 
        views.clsVerNegociacionesViw.as_view(), 
        name='ver_negociacion'
        ),

    # Menu promociones
    path(
        'menu_promociones/', 
        views.clsMenuPromocionesViw.as_view(), 
        name='menu_promociones'
        ),
    # Crear promoción
    path(
        'crear_promocion/', 
        views.clsCrearPromocionesView.as_view(), 
        name='crear_promocion'
        ),
    # Ver promociones
    path(
        'ver_promociones/', 
        views.clsVerPromocionesViw.as_view(), 
        name='ver_promociones'
        ),
    
    # Menu ordenes de compra
    path(
        'menu_orden_compra/', 
        views.clsMenuOrdenesCompraViw.as_view(), 
        name='menu_orden_compra'
        ),
    # Crear orden de compra
    path(
        'crear_orden_compra/', 
        views.clsCrearOrdenCompraViw.as_view(), 
        name='crear_orden_compra'
        ),
    # Ver orden de compra
    path(
        'ver_orden_compra/', 
        views.clsVerOrdenesCompraViw.as_view(), 
        name='ver_orden_compra'
        ),
    # Imprimir ordenes compra

    # Menu cotización proveedor
    path(
        'menu_cotizacion_proveedor/', 
        views.clsMenuCotizacionProveedorViw.as_view(), 
        name='menu_cotizacion_proveedor'
        ),
    # Crear cotización proveedor
    path(
        'crear_cotizacion_proveedor/', 
        views.clsCrearCotizacionViw.as_view(), 
        name='crear_cotizacion_proveedor'
        ),
    # Ver cotizaciones proveedor
    path(
        'ver_cotizacion_proveedor/', 
        views.clsVerCotizacionesViw.as_view(), 
        name='ver_cotizacion_proveedor'
        ),
    # Imprimir cotización proveedor

    # Menu catálogo de productos
    path(
        'catalogo_productos/', 
        views.clsMenuCatalogoProductosViw.as_view(), 
        name='catalogo_productos'
        ),
    # Opciones catálogo de productos
    path(
        'opciones_producto/', 
        views.clsOpcionesCatalogoProductoViw.as_view(), 
        name='opciones_producto'
        ),
    # Crear producto
    path(
        'crear_producto/', 
        views.clsCrearProductoViw.as_view(), 
        name='crear_producto'
        ),
    # Editar producto
    path(
        'actualizar_producto/<int:pk>/', 
        views.clsEditarProductoViw.as_view(), 
        name = 'actualizar_producto'
        ),
    # Listar productos
    path(
        'listar_productos/', 
        views.clsListarCatalogoProductosViw.as_view(),
        name='listar_productos'
        ),
    # Importar archivo de productos
    path(
        'import_products/', 
        views.clsImportarCatalogoProductosViw.as_view(), 
        name='import_products'
        ),

    # Menu gestiónar ordenes de compra
    path(
        'menu_gestion_ordenes_compra/', 
        views.clsMenuGestionarOrdenesCompraViw.as_view(), 
        name='menu_gestion_ordenes_compra'
        ),
    # Próximas entregas
    path(
        'proximas_entregas/', 
        views.clsProximasEntregasViw.as_view(), 
        name='proximas_entregas'
        ),
    path(
        'entregas_incumplidas/', 
        views.clsEntregasIncumplidasViw.as_view(), 
        name='entregas_incumplidas'
        ),
    
    # Proveedores
    # Menu catálogo de proveedores
    path(
        'catalogo_proveedores/', 
        views.clsMenuCatalogoProveedoresViw.as_view(), 
        name='catalogo_proveedores'
        ),
    # Opciones catálogo proveedor
    path(
        'opciones_proveedor/', 
        views.clsOpcionesCatalogoProveedoresViw.as_view(), 
        name='opciones_proveedor'
        ),
    # Crear proveedor
    path(
        'crear_proveedor/', 
        views.clsCrearProveedorViw.as_view(), 
        name='crear_proveedor'
        ),
    # Editar proveedor
    path(
        'actualizar_proveedor/<int:pk>/', 
        views.clsEditarProveedorViw.as_view(), 
        name = 'actualizar_proveedor'
        ),
    # Listar proveedores
    path(
        'listar_proveedores/', 
        views.clsListarCatalogoProveedoresViw.as_view(),
        name='listar_proveedores'
        ),
    # Exportar plantilla de proveedores
    path(
        'export_suppliers/', 
        views.clsExportarPlantillaProveedoresViw.as_view(), 
        name='export_suppliers'
        ),
    # Importar archivo de proveedores
    path(
        'importar_proveedores/', 
        views.clsImportarCatalogoProveedoresViw.as_view(), 
        name='importar_proveedores'
        ),
    # Exportar catálogo proveedores
    path(
        'exportar_catalogo_proveedores/', 
        views.clsExportarCatalogoProveedoresViw.as_view(), 
        name='exportar_catalogo_proveedores'
        ),
    
    # Menu evaluación proveedores
    path(
        'evaluacion_proveedor/', 
        views.clsMenuEvaluacionProveedorViw.as_view(), 
        name='evaluacion_proveedor'
        ),
    # Crear evaluación proveedor
    path(
        'crear_evaluacion_proveedor/', 
        views.clsCrearEvaluacionProveedorViw.as_view(), 
        name='crear_evaluacion_proveedor'
        ),
    # Ver evaluación proveedor
    path(
        'ver_evaluacion_proveedor/', 
        views.clsVerEvaluacionProveedorViw.as_view(), 
        name='ver_evaluacion_proveedor'
        ),
    
    # Ver cartera de proveedores
    path(
        'cartera_proveedores', 
        views.clsCarteraProveedoresViw.as_view(), 
        name='cartera_proveedores'
        ),
    
    ]