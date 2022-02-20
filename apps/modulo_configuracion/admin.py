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
@admin.register(clsTblDetalleEntradaAlmacen)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin historico movimientos '''
@admin.register(clsHistoricoMovimientosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass