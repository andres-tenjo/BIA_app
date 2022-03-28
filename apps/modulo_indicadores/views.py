from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView

''' Vista para ventana de indicadores comerciales'''
class CommercialIndicatorsView(TemplateView):
    template_name = 'modulo_indicadores/indicadores_comercial.html'

''' Vista para ventana de indicadores compras'''
class PurchaseIndicatorsView(TemplateView):
    template_name = 'modulo_indicadores/indicadores_compras.html'

''' Vista para ventana de indicadores almacen'''
class LogisticsWarehouseIndicatorsView(TemplateView):
    template_name = 'modulo_indicadores/indicadores_almacen.html'

class LogisticsTransportIndicatorsView(TemplateView):
    template_name = 'modulo_indicadores/indicadores_transporte.html'