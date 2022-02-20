from django.urls import path
from apps.modulo_compras import views
from django.views.generic import TemplateView


urlpatterns = [

    # Negociación
    path('iniciar_negociacion', views.StartNegotiationView.as_view(), name='iniciar_negociacion'),
    
    # Orden de compra
    path('crear_orden_compra', views.PurchaseOrderView.as_view(), name='crear_orden_compra'),

    # Solicitar cotización
    path('sol_cotizacion', views.SupplierQuoteView.as_view(), name='sol_cotizacion'),

    # Productos
    path('cat_productos', views.CatProdView.as_view(), name='cat_prod'),
    path('crear_producto', views.ProductCreateView.as_view(), name='crear_producto'),
    path('cargar_productos', views.CatProdUploadView.as_view(), name='cargar_productos'),
    path('listar_productos', views.ProductListView.as_view(), name='listar_productos'),
    path('editar_producto/<int:pk>', views.ActualizarProducto.as_view(), name='editar_producto'),
    
    path('ver_categoria_prod', views.ListarCategoriaProd.as_view(), name='ver_categoria_prod'),
    path('crear_categoria_producto', views.CrearCatProd.as_view(), name='crear_categoria_producto'),
    path('editar_cat_prod/<int:pk>', views.ActualizarCatProd.as_view(), name='editar_cat_prod'),

    path('ver_subcategoria_prod', views.ListarSubcatProd.as_view(), name='ver_subcategoria_prod'),
    path('crear_subcategoria_producto', views.CrearSubcatProd.as_view(), name='crear_subcategoria_producto'),
    path('editar_subcat_prod/<int:pk>', views.ActualizarSubcatProd.as_view(), name='editar_subcat_prod'),

    path('crear_unidad_compra', views.CrearUniCompra.as_view(), name='crear_unidad_compra'),
    path('crear_unidad_venta', views.CrearUniVenta.as_view(), name='crear_unidad_venta'),
    path('crear_condicion_compra', views.CrearCondCompra.as_view(), name='crear_condicion_compra'),
    path('crear_condicion_almacenamiento', views.CrearCondAlm.as_view(), name='crear_condicion_almacenamiento'),

    # Gestiónar ordenes de compra
    path('proximas_entregas', views.UpcomingDeliveriesListView.as_view(), name='proximas_entregas'),
    path('entregas_incumplidas', views.UnfulfilledDeliveriesListView.as_view(), name='entregas_incumplidas'),
    path('novedades_ordenes_compra', views.OrdersNewsView.as_view(), name='novedades_ordenes_compra'),
    
    # Actividades
    path('actividades_compras', views.ActivityListView.as_view(), name='actividades_compras'),
    
    # Proveedores
    path('cat_proveedores', views.CatSupplierView.as_view(), name='cat_proveedores'),
    path('crear_proveedor', views.clsCrearProveedorViw.as_view(), name='crear_proveedor'),
    path('cargar_proveedores', views.CatSuppUploadView.as_view(), name='cargar_proveedores'),
    path('listar_proveedores', views.clsListarCatalogoProveedoresViw.as_view(), name='listar_proveedores'),
    
    # Gestión proveedores
    path('evaluacion_proveedores', views.SupplierEvaluationView.as_view(), name='evaluacion_proveedores'),
    path('listar_evaluaciones', views.SupplierEvalListView.as_view(), name='listar_evaluaciones'),
    path('cartera_proveedores', views.CarteraSupView.as_view(), name='cartera_proveedores'),
    
    # Gestión de módulo compras
    path('historico_mov_compras', views.historico_mov_compras, name='historico_mov_compras'),
    path('indicadores_compras', views.PurchaseIndicatorsView.as_view(), name='indicadores_compras'),
    ]