from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin

from .models import *

''' Admin ordenes de compra '''
@admin.register(OrderPurchase)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(OrderPurchaseDetail)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin cotizaciones proveedor '''
@admin.register(SupplierQuote)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin cotizaciones proveedor '''
@admin.register(EntregasIncumplidas)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(SupplierQuoteDetail)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin gestión y evaluación de proveedores '''
@admin.register(EvaluationSuppliers)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin cartera de proveedores '''
@admin.register(SupplierDebt)
class PersonAdmin(ImportExportModelAdmin):
    pass

''' Admin pagos proveedores '''
@admin.register(SuppliersPayments)
class PersonAdmin(ImportExportModelAdmin):
    pass
