from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from .models import *

''' Admin pedidos '''
@admin.register(Orders)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(OrdersDetail)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(LostSales)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin cotizaciones '''
@admin.register(Quotes)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(QuotesDetail)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin ruta visitas '''
@admin.register(VisitsRoute)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin cartera clientes '''
@admin.register(CustomerDebt)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin pagos clientes '''
@admin.register(CustomerPayments)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin agenda llamadas '''
@admin.register(ScheduleCall)
class PersonAdmin(ImportExportModelAdmin):
    pass


