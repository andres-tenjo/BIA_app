from import_export import resources

from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import *

''' Admin planeación comercial '''
@admin.register(clsIndicadoresComercialesMdl)
class PersonAdmin(ImportExportModelAdmin):
    pass
