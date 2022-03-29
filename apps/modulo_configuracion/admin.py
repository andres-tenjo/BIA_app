from import_export import resources

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import *

''' Admin departamentos '''
@admin.register(clsDepartamentosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin ciudades '''
@admin.register(clsCiudadesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin empresa '''
@admin.register(clsPerfilEmpresaMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin productos '''
@admin.register(clsCategoriaProductoMdl)
class PersonProductAdmin(ImportExportModelAdmin):
    pass

@admin.register(clsSubcategoriaProductoMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(clsUnidadCompraMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(clsUnidadVentaMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(clsCatalogoProductosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(clsAsesorComercialMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin clientes '''
@admin.register(clsCategoriaClienteMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(clsMargenCategoriaClienteMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(clsZonaClienteMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(clsCatalogoClientesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin proveedores '''
@admin.register(clsCatalogoProveedoresMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin bodegas '''
@admin.register(clsCatalogoBodegasMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin historico pedidos '''
@admin.register(clsHistoricoPedidosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin saldos inventario '''
@admin.register(clsSaldosInventarioMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin ajuste inventario '''
@admin.register(clsAjusteInventarioMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin entradas de almacén '''
@admin.register(clsEntradasAlmacenMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin entradas de almacén '''
@admin.register(clsDetalleEntradaAlmacen)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin salidas de almacén '''
@admin.register(clsSalidasAlmacenMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin historico movimientos '''
@admin.register(clsHistoricoMovimientosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass
  
'''Admin historico alterno de movimientos'''
@admin.register(clsHistoricoMovimientosAlternoMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

'''Admin pedidos general'''
@admin.register(clsPedidosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

'''Admin pedidos detallado'''
@admin.register(clsDetallePedidosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

'''Admin ordenes de compra general'''
@admin.register(clsOrdenesCompraMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

'''Admin ordenes de compra detallado'''
@admin.register(clsDetalleOrdenesCompraMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

'''Admin lista de precios general'''
@admin.register(clsListaPreciosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

'''Admin lista de precios detallado'''
@admin.register(clsDetalleListaPreciosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

'''Admin cotizaciones general'''
@admin.register(clsCotizacionesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

'''Admin cotizaciones detallado'''
@admin.register(clsDetalleCotizacionesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass