# Django libraries
from django.urls import path

# Apps functions
from .views import *
from apps.usuario.views import *

urlpatterns = [
    # Crear empresa
    path(
        'crear_empresa/', 
        clsCrearEmpresaViw.as_view(), 
        name='crear_empresa'
        ),
    # Editar empresa
    path(
        'editar_empresa/<int:pk>/', 
        clsEditarEmpresaViw.as_view(), 
        name='editar_empresa'
        ),

    # Grupos y usuarios
    path(
        'vista_usuarios', 
        clsMenuUsuarioViw.as_view(), 
        name='vista_usuarios'
        ),

    # Catálogo de productos
    path(
        'product_catalogue/', 
        clsMenuCatalogoProductosViw.as_view(), 
        name='product_catalogue'
        ),
    # Opciones catálogo de productos
    path(
        'opciones_producto/', 
        clsOpcionesCatalogoProductoViw.as_view(), 
        name='opciones_producto'
        ),
    # Crear producto
    path(
        'crear_producto/', 
        clsCrearProductoViw.as_view(), 
        name='crear_producto'
        ),
    # Editar producto
    path(
        'actualizar_producto/<int:pk>/', 
        clsEditarProductoViw.as_view(), 
        name = 'actualizar_producto'
        ),
    # Listar productos
    path(
        'listar_productos/', 
        clsListarCatalogoProductosViw.as_view(),
        name='listar_productos'
        ),
    # Exportar plantilla productos
    path(
        'export_products/', 
        clsExportarPlantillaProductosViw.as_view(), 
        name='export_products'
        ),
    # Importar archivo de productos
    path(
        'import_products/', 
        clsImportarCatalogoProductosViw.as_view(), 
        name='import_products'
        ),
    # Exportar catálogo productos
    path(
        'exportar_catalogo_productos/', 
        clsExportarCatalogoProductosViw.as_view(), 
        name='exportar_catalogo_productos'
        ),

    # Catálogo de proveedores
    path(
        'cat_sup/', 
        clsMenuCatalogoProveedoresViw.as_view(), 
        name='cat_proveedores'
        ),
    # Opciones catálogo proveedor
    path(
        'opciones_proveedor/', 
        clsOpcionesCatalogoProveedoresViw.as_view(), 
        name='opciones_proveedor'
        ),
    # Crear proveedor
    path(
        'crear_proveedor/', 
        clsCrearProveedorViw.as_view(), 
        name='crear_proveedor'
        ),
    # Editar proveedor
    path(
        'actualizar_proveedor/<int:pk>/', 
        clsEditarProveedorViw.as_view(), 
        name = 'actualizar_proveedor'
        ),
    # Listar proveedores
    path(
        'listar_proveedores/', 
        clsListarCatalogoProveedoresViw.as_view(),
        name='listar_proveedores'
        ),
    # Exportar plantilla de proveedores
    path(
        'export_suppliers/', 
        clsExportarPlantillaProveedoresViw.as_view(), 
        name='export_suppliers'
        ),
    # Importar archivo de proveedores
    path(
        'import_suppliers/', 
        clsImportarCatalogoProveedoresViw.as_view(), 
        name='import_suppliers'
        ),
    # Exportar catálogo proveedores
    path(
        'exportar_catalogo_proveedores/', 
        clsExportarCatalogoProveedoresViw.as_view(), 
        name='exportar_catalogo_proveedores'
        ),

    # Catálogo de clientes
    path(
        'cat_cli/', 
        clsMenuCatalogoClientesViw.as_view(), 
        name='cat_clientes'
        ),
    # Opciones catálogo de clientes
    path(
        'opciones_cliente/', 
        clsOpcionesCatalogoClientesViw.as_view(), 
        name='opciones_cliente'
        ),
    # Crear cliente
    path(
        'crear_cliente/', 
        clsCrearClienteViw.as_view(), 
        name='crear_cliente'
        ),
    # Editar cliente
    path(
        'actualizar_cliente/<int:pk>/', 
        clsEditarClienteViw.as_view(), 
        name = 'actualizar_cliente'
        ),
    # Listar clientes
    path(
        'listar_clientes/', 
        clsListarCatalogoClientesViw.as_view(),
        name='listar_clientes'
        ),
    # Exportar plantilla de clientes
    path(
        'export_customers/', 
        clsExportarPlantillaClientesViw.as_view(), 
        name='export_customers'
        ),
    # Importar plantilla de clientes
    path(
        'import_customers/', 
        clsImportarCatalogoClientesViw.as_view(), 
        name='import_customers'
        ),
    # Exportar catálogo clientes
    path(
        'exportar_catalogo_clientes/', 
        clsExportarCatalogoClientesViw.as_view(), 
        name='exportar_catalogo_clientes'
        ),
    
    # Catálogo de bodegas
    path(
        'catalogo_bodegas/', 
        clsMenuCatalogoBodegasViw.as_view(), 
        name='catalogo_bodegas'
        ),
    # Crear bodega
    path(
        'crear_bodega/', 
        clsCrearBodegaViw.as_view(), 
        name='crear_bodega'
        ),
    # Listar bodegas
    path(
        'listar_bodegas/', 
        clsListarCatalogoBodegasViw.as_view(), 
        name='listar_bodegas'
        ),
    
    path(
        'editar_bodega/<int:pk>/', 
        clsEditarBodegaViw.as_view(), 
        name='editar_bodega'
        ),
    # Exportar catálogo bodegas
    path(
        'exportar_catalogo_bodegas/', 
        clsExportarCatalogoBodegasViw.as_view(), 
        name='exportar_catalogo_bodegas'
        ),
    
    # Importar historico de movimientos
    path(
        'importar_historico_movimientos/', 
        clsImportarHistoricoMovimientosViw.as_view(), 
        name='importar_historico_movimientos'
        ),
    # Descargar plantilla historico de movimientos
    path(
        'plantilla_historico_movimientos/',
        clsExportarPlantillaHistoricoMovimientosViw.as_view(), 
        name='plantilla_historico_movimientos'
        ),
    
    # Ajustes de inventario vista
    path(
        'ajustes_inventario/',
        clsAjustesInventarioViw.as_view(), 
        name='ajustes_inventario'
        ),
    # Importar ajustes de inventario
    path(
        'importar_ajustes_inventario/', 
        clsImportarAjustesInventarioViw.as_view(), 
        name='importar_ajustes_inventario'
        ),
    # Descargar plantilla ajustes de inventario
    path(
        'plantilla_ajustes_inventario/',
        clsExportarPlantillaAjustesInventarioViw.as_view(), 
        name='plantilla_ajustes_inventario'
        ),
    # Crear ajuste de inventario
    path(
        'crear_ajuste_inventario/',
        clsCrearAjusteInventarioViw.as_view(), 
        name='crear_ajuste_inventario'
        ),
    
    path(
        'descargar_excel/',
        clsExportarPlantillaPrueba.as_view(), 
        name='descargar_excel'
        ),
    ]
    