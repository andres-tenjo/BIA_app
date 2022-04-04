from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from apps.modulo_configuracion.models import *

##########################################################
# PROMOCIONES
##########################################################
''' Promociones comerciales'''
@admin.register(clsPromocionesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Detalle productos promociones comerciales'''
@admin.register(clsDetalleProductosPromocionesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Detalle clientes promociones comerciales'''
@admin.register(clsDetalleClientesPromocionesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Detalle filtros promociones comerciales'''
@admin.register(clsDetalleFiltrosPromocionesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

##########################################################
# PEDIDOS
##########################################################
''' Pedidos'''
@admin.register(clsPedidosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Detalle pedidos'''
@admin.register(clsDetallePedidosMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

##########################################################
# COTIZACIONES
##########################################################
''' Cotizaciones '''
@admin.register(clsCotizacionesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Detalle cotizaciones'''
@admin.register(clsDetalleCotizacionesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass

##########################################################
# ACTIVIDADES COMERCIALES
##########################################################
''' Actividades comerciales '''
@admin.register(clsActividadesComercialMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass