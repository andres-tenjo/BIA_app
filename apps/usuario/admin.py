from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from apps.usuario.models import User

''' Admin departamentos '''
@admin.register(User)
class PersonAdmin(ImportExportModelAdmin):
    pass