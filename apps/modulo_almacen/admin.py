from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from apps.modulo_configuracion.models import *

################################################
# ENTRADAS DE ALMACEN
################################################
''' Entradas de almacen'''
@admin.register(clsEntradasAlmacenMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Detalle entradas de almacen'''
@admin.register(clsDetalleEntradaAlmacen)
class PersonAdmin(ImportExportModelAdmin):
    pass

################################################
# SALIDAS DE ALMACEN
################################################
''' Salidas de almacén '''
@admin.register(clsSalidasAlmacenMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Detalle salidas de almacén '''
@admin.register(clsDetalleSalidasAlmacenMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

################################################
# INVENTARIO
################################################
''' Saldos de inventario '''
@admin.register(clsSaldosInventarioMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass