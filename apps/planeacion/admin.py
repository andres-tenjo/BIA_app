from import_export import resources

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from apps.modulo_configuracion.models import *

###########################################################
# INDICADORES COMERCIALES
###########################################################
''' Indicadores comerciales'''
@admin.register(clsIndicadoresComercialesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# INDICADORES COMPRAS
###########################################################
''' Indicadores compras'''
@admin.register(clsIndicadoresComprasMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

###########################################################
# INDICADORES ALMACEN
###########################################################
''' Indicadores almacen'''
@admin.register(clsIndicadoresAlmacenMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass
