from import_export import resources

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import *

###########################################################
# CIUDADES Y DEPARTAMENTOS
###########################################################
''' Departamentos'''
@admin.register(clsDepartamentosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Ciudades'''
@admin.register(clsCiudadesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# PERFIL EMPRESA
###########################################################
''' Admin empresa'''
@admin.register(clsPerfilEmpresaMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# CATÁLOGO PRODUCTOS
###########################################################
''' Categoría de productos'''
@admin.register(clsCategoriaProductoMdl)
class PersonProductAdmin(ImportExportModelAdmin):
    pass

''' Subcategoría de productos'''
@admin.register(clsSubcategoriaProductoMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Unidad de compra'''
@admin.register(clsUnidadCompraMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Unidad de venta'''
@admin.register(clsUnidadVentaMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Catálogo de productos'''
@admin.register(clsCatalogoProductosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# CATÁLOGO CLIENTES
###########################################################
''' Asesor comercial'''
@admin.register(clsAsesorComercialMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Categoría cliente'''
@admin.register(clsCategoriaClienteMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Margén categoría cliente'''
@admin.register(clsMargenCategoriaClienteMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Zona cliente'''
@admin.register(clsZonaClienteMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Catálogo clientes'''
@admin.register(clsCatalogoClientesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# CATÁLOGO PROVEEDORES
###########################################################
''' Cantidad miníma de compra'''
@admin.register(clsCondicionMinimaCompraMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Descuento proveedores'''
@admin.register(clsCondicionDescuentoProveedorMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Catálogo proveedores '''
@admin.register(clsCatalogoProveedoresMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# CATÁLOGO BODEGAS
###########################################################
''' Catálogo bodegas'''
@admin.register(clsCatalogoBodegasMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# HISTORICO MOVIMIENTOS ALTERNO
###########################################################
''' Histórico pedidos'''
@admin.register(clsHistoricoPedidosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Histórico ordenes de compra'''
@admin.register(clsHistoricoOrdenesCompraMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Histórico movimientos alterno'''
@admin.register(clsHistoricoMovimientosAlternoMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# AJUSTES DE INVENTARIO
###########################################################
''' Ajustes inventario '''
@admin.register(clsAjusteInventarioMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Detalle ajustes inventario '''
@admin.register(clsDetalleAjusteInventarioMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# HISTORICO DE MOVIMIENTOS
###########################################################
''' Historico movimientos '''
@admin.register(clsHistoricoMovimientosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass
  
###########################################################
# LISTA DE PRECIOS
###########################################################
''' Lista de precios'''
@admin.register(clsListaPreciosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Lista de precios detallado'''
@admin.register(clsDetalleListaPreciosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# DEVOLUCIONES CLIENTE
###########################################################
''' Devoluciones cliente'''
@admin.register(clsDevolucionesClienteMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Devoluciones cliente detallado'''
@admin.register(clsDetalleDevolucionesClienteMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# DEVOLUCIONES PROVEEDOR
###########################################################
''' Devoluciones proveedor'''
@admin.register(clsDevolucionesProveedorMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Devoluciones proveedor detallado'''
@admin.register(clsDetalleDevolucionesProveedorMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# OBSEQUIOS
###########################################################
''' Obsequios'''
@admin.register(clsObsequiosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Obsequios detallado'''
@admin.register(clsDetalleObsequiosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# TRASLADOS DE BODEGA
###########################################################
''' Traslados de bodega'''
@admin.register(clsTrasladosBodegasMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Traslados de bodega detallado'''
@admin.register(clsDetalleTrasladosBodegaMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# TIEMPOS DE ENTREGA
###########################################################
''' Tiempos de entrega'''
@admin.register(clsTiemposEntregaMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# VENTAS PERDIDAS
###########################################################
''' Ventas perdidas'''
@admin.register(clsVentasPerdidasMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass
