# Python libraries
import json
from datetime import datetime, date
import time
from pandas import pandas as pd

# Modelos BIA
from apps.Modelos.Several_func import *
from apps.Modelos.Update_Balances import *

# Django libraries
from django.conf import settings
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from django.urls import reverse_lazy

# Django-rest libraries
from rest_framework.views import APIView
from rest_framework.response import Response

# BIA files
from apps.mixins import ValidatePermissionRequiredMixin
from .forms import *
from .models import *
from apps.modulo_comercial.models import *
from apps.modulo_logistica.models import *
from apps.modulo_compras.models import *
from apps.functions_views import *
from apps.Modelos.Several_func import *

################################################################################################
############################### VISTAS DEL MODULO PLANEACIÓN ###################################
################################################################################################

#################################################################################################
# 1. PLANEACIÓN COMERCIAL
#################################################################################################
''' 1.1 Vista menú planeación comercial'''
class clsMenuPlaneacionComercialViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_planeacion/planeacion_comercial.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Establecer Indicadores'
        context['create_url'] = reverse_lazy('planeacion:planeacion_comercial_indicadores')
        context['search_title'] = 'Ver historico'
        context['search_url'] = reverse_lazy('planeacion:planeacion_comercial_historico')
        return context

''' 1.2 Vista planeación comercial - indicadores'''
class clsPlaneacionComercialEstablecerIndicadoresViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modulo_planeacion/planeacion_comercial_establecer_indicadores.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'jsnConsultarIndicadoresjsn':
                lstIndicadoresGenerales = ['Total_Sales_Objetive', 'Customer_Retention_Rate', 'Sales_Deepening', 'New_Customers', 'Margin']
                lstQrsIndicadores = [ {i: fncRetornarDataGraficolst('General', i)} for i in lstIndicadoresGenerales ]
                response = JsonResponse(lstQrsIndicadores, safe=False)
            if action == 'btnConsultarCiudadesClientesjsn':
                
                
                # lstCiudades = dtfCatalogoClientes['city'].tolist()
                # lstDuplicadosCiudades = fncDuplicadoListatpl(lstCiudades)
                
                response = JsonResponse(dtfCiudadesClientes, safe=False)
            else:
                jsnData['error'] = 'No se encontraron resultados'
        except Exception as e:
            jsnData['error'] = str(e)
            response = JsonResponse(jsnData, safe=False)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Planeación comercial - Establecer indicadores'
        return context

''' 1.3 Vista planeación comercial - histórico'''
class clsPlaneacionComercialHistoricoViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modulo_planeacion/planeacion_comercial_historico.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'jsnConsultarIndicadoresjsn':
                print('si')
                jsnData = []
                qrsIndicadorVentaTotal = fncRetornarDataGraficolst('General', 'Total_Sales_Objetive')
                print(qrsIndicadorVentaTotal)
                # qrsIndicadorVentasNuevas = fncRetornarDataGraficolst('General', 'Customer_Retention_Rate')
                # qrsIndicadorProfundizacionClientes = fncRetornarDataGraficolst('General', 'Sales_Deepening')
                # qrsIndicadorClientesNuevos = fncRetornarDataGraficolst('General', 'New_Customers')
                # qrsIndicadorMargenVentas = fncRetornarDataGraficolst('General', 'Margin')

                print('si')
            else:
                data['error'] = 'No se encontraron resultados'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

#################################################################################################
# 2. PLANEACIÓN COMPRAS
#################################################################################################
''' 2.1 Vista menú planeación compras'''
class clsMenuPlaneacionComprasViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_planeacion/planeacion_compras.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Establecer Indicadores'
        context['create_url'] = reverse_lazy('planeacion:planeacion_compras_indicadores')
        context['search_title'] = 'Ver historico'
        context['search_url'] = reverse_lazy('planeacion:planeacion_compras_historico')
        return context

''' 2.2 Vista planeación compras - indicadores'''
class clsPlaneacionComprasEstablecerIndicadoresViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modulo_planeacion/planeacion_compras_establecer_indicadores.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_data':
                print('si')
            else:
                data['error'] = 'No se encontraron resultados'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

''' 2.3 Vista planeación compras - histórico'''
class clsPlaneacionComprasHistoricoViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modulo_planeacion/planeacion_compras_historico.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_data':
                print('si')
            else:
                data['error'] = 'No se encontraron resultados'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

#################################################################################################
# 3. PLANEACIÓN ALMACÉN
#################################################################################################
''' 3.1 Vista menú planeación almacén'''
class clsMenuPlaneacionAlmacenViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_planeacion/planeacion_almacen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Establecer Indicadores'
        context['create_url'] = reverse_lazy('planeacion:planeacion_almacen_indicadores')
        context['search_title'] = 'Ver historico'
        context['search_url'] = reverse_lazy('planeacion:planeacion_almacen_historico')
        return context

''' 3.2 Vista planeación almacén - indicadores'''
class clsPlaneacionAlmacenEstablecerIndicadoresViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modulo_planeacion/planeacion_almacen_establecer_indicadores.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_data':
                print('si')
            else:
                data['error'] = 'No se encontraron resultados'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

''' 3.3 Vista planeación almacén - histórico'''
class clsPlaneacionAlmacenHistoricoViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modulo_planeacion/planeacion_almacen_historico.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_data':
                print('si')
            else:
                data['error'] = 'No se encontraron resultados'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
