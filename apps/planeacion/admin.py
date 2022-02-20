from import_export import resources

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import *


''' Admin promociones '''
@admin.register(Promotions)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(PromotionProducts)
class PersonAdmin(ImportExportModelAdmin):
    pass

@admin.register(CommercialPlanning)
class PersonAdmin(ImportExportModelAdmin):
    pass
