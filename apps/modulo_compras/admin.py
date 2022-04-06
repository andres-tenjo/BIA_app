from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from apps.modulo_configuracion.models import *

################################################
# ORDENES DE COMPRA
################################################
''' Ordenes de compra '''
@admin.register(clsOrdenesCompraMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Detalle ordenes de compra '''
@admin.register(clsDetalleOrdenesCompraMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

################################################
# EVALUACIÓN PROVEEDORES
################################################
''' Evaluación de proveedores '''
@admin.register(clsEvaluacionProveedorMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass
