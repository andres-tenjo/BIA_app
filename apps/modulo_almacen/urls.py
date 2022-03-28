from django.urls import path
from .views import *

urlpatterns = [
    
    ############################################
    # 1. CATALOGO DE PRODUCTOS
    ############################################
    # 1.1 Ver productos
    path(
        'ver_productos', 
        clsVerCatalogoProductosViw.as_view(), 
        name='ver_productos'
        ),
    
    ############################################
    # 2. ENTRADAS DE ALMACEN
    ############################################
    # 2.1 Menú entradas de almacen
    path(
        'menu_entradas_almacen/', 
        clsMenuEntradasAlmacenViw.as_view(), 
        name='menu_entradas_almacen'
        ),
    # 2.2 Crear entrada de almacen
    path(
        'crear_entradas_almacen/', 
        clsCrearEntradaAlmacenViw.as_view(), 
        name='crear_entradas_almacen'
        ),
    # 2.3 Ver entradas de almacen
    path(
        'ver_entradas_almacen/', 
        clsCrearEntradaAlmacenViw.as_view(), 
        name='ver_entradas_almacen'
        ),
    
    ############################################
    # 3. SALIDAS DE ALMACEN
    ############################################
    # 3.1 Menú salidas de almacen
    path(
        'menu_salidas_almacen/', 
        clsMenuSalidasAlmacenViw.as_view(), 
        name='menu_salidas_almacen'
        ),
    # 3.2 Crear salida de almacen
    path(
        'crear_salida_almacen/', 
        clsCrearSalidaAlmacenViw.as_view(), 
        name='crear_salida_almacen'
        ),
    # 3.3 Ver salidas de almacen
    path(
        'ver_salidas_almacen/', 
        clsVerSalidasAlmacenViw.as_view(), 
        name='ver_salidas_almacen'
        ),

    ############################################
    # 4. INVENTARIO
    ############################################
    # 4.1 Menú inventario
    path(
        'menu_inventario/', 
        clsMenuInventarioViw.as_view(), 
        name='menu_inventario'
        ),
    # 4.2 Crear inventario
    path(
        'crear_inventario/',
        clsCrearInventarioViw.as_view(), 
        name='crear_inventario'
        ),
    # 4.3 Ver inventario
    path(
        'ver_inventarios/',
        clsVerInventarioViw.as_view(), 
        name='ver_inventarios'
        ),

    ############################################
    # 5. CATÁLOGO DE BODEGAS
    ############################################
    # 5.1 Menú catálogo de bodegas
    path(
        'menu_catalogo_bodegas/', 
        clsMenuCatalogoBodegasViw.as_view(), 
        name='menu_catalogo_bodegas'
        ),
    # 5.2 Crear bodega
    path(
        'crear_bodega/', 
        clsCrearBodegaViw.as_view(), 
        name='crear_bodega'
        ),
    # 5.3 Ver bodegas
    path(
        'ver_bodegas/', 
        clsVerCatalogoBodegasViw.as_view(), 
        name='ver_bodegas'
        ),
    # 5.4 Editar bodega
    path(
        'editar_bodega/<int:pk>/',
        clsEditarBodegaViw.as_view(), 
        name='editar_bodega'
        ),

    ]