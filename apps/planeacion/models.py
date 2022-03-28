# Pyhton libraries


# Django libraries
from django.db import models
from apps.modulo_configuracion.models import *

# BIA files
from apps.choices import *
from apps.models import BaseModel
from apps.usuario.models import *

''' Tablas planificación comercial'''
# Tabla indicadores comerciales
class clsIndicadoresComercialesMdl(models.Model):
    creation_date =  models.DateTimeField('Fecha creación')
    measurement_date = models.DateTimeField('Fecha medición', blank=True, null=True)
    indicator = models.CharField('Indicador', max_length=200)
    set = models.CharField('Conjunto', max_length=200, blank=True, null=True) # General o categoría
    subset= models.CharField('Subconjunto', max_length=200, blank=True, null=True)# pk por categoría
    objetive = models.DecimalField('Objetivo', max_digits=10, decimal_places=2, blank=True, null=True)
    real = models.DecimalField('Real', max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment = models.DecimalField('Cumplimiento', max_digits=10, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Indicador comercial'
        verbose_name_plural = 'Indicadores comerciales'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.set
