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
from apps.modulo_almacen.models import *
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
            elif action == 'btnConsultarCiudadesClientesjsn':
                lstSelectCiudad = fncRetornarDataSelectdct('modulo_configuracion_clssalidasalmacenmdl')
                if type(lstSelectCiudad) == str:
                    jsnData['strError'] = lstSelectCiudad
                    response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['lstSelectCiudad'] = lstSelectCiudad
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'slcIndicadorCiudadjsn':
                intCiudad = request.POST['intCiudad']
                strIndicadorCiudad = request.POST['strIndicadorCiudad']
                dctIndicadorCiudad = fncRetornarDataGraficolst('City', strIndicadorCiudad, intCiudad)
                response = JsonResponse(dctIndicadorCiudad, safe=False)
            elif action == 'btnConsultarZonasClientesjsn':
                lstSelectZonas = fncRetornarDataSelectdct('modulo_configuracion_clszonaclientemdl', 'customer_zone')
                if type(lstSelectZonas) == str:
                    jsnData['strError'] = lstSelectZonas
                    response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['lstSelectZonas'] = lstSelectZonas
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'slcIndicadorZonajsn':
                intZona = request.POST['intZona']
                strIndicadorZona = request.POST['strIndicadorZona']
                dctIndicadorZona = fncRetornarDataGraficolst('Zones', strIndicadorZona, intZona)
                response = JsonResponse(dctIndicadorZona, safe=False)
            elif action == 'btnConsultarCategoriasClientesjsn':
                lstSelectCategoriaCliente = fncRetornarDataSelectdct('modulo_configuracion_clscategoriaclientemdl', 'customer_cat')
                if type(lstSelectCategoriaCliente) == str:
                    jsnData['strError'] = lstSelectCategoriaCliente
                    response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['lstSelectCategoriaCliente'] = lstSelectCategoriaCliente
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'slcIndicadorCategoriaClientejsn':
                intCategoriaCliente = request.POST['intCategoriaCliente']
                strIndicadorCategoriaCliente = request.POST['strIndicadorCategoriaCliente']
                dctIndicadorCategoriaCliente = fncRetornarDataGraficolst('Customer_Category', strIndicadorCategoriaCliente, intCategoriaCliente)
                response = JsonResponse(dctIndicadorCategoriaCliente, safe=False)
            elif action == 'btnConsultarAsesoresComercialesjsn':
                lstSelectAsesorComercial = fncRetornarDataSelectdct('modulo_configuracion_clsasesorcomercialmdl', 'advisor')
                if type(lstSelectAsesorComercial) == str:
                    jsnData['strError'] = lstSelectAsesorComercial
                    response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['lstSelectAsesorComercial'] = lstSelectAsesorComercial
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'slcIndicadorAsesorComercialjsn':
                intAsesorComercial = request.POST['intAsesorComercial']
                strIndicadorAsesorComercial = request.POST['strIndicadorAsesorComercial']
                dctIndicadorAsesorComercial = fncRetornarDataGraficolst('Adviser', strIndicadorAsesorComercial, intAsesorComercial)
                response = JsonResponse(dctIndicadorAsesorComercial, safe=False)
            elif action == 'btnGuardarPlaneacionComercialjsn':
                lstIndicadoresGenerales = json.loads(request.POST['lstIndicadoresGenerales'])
                lstTablaCiudades = json.loads(request.POST['lstTablaCiudades'])
                lstTablaZonas = json.loads(request.POST['lstTablaZonas'])
                lstTablaCategoriaCliente = json.loads(request.POST['lstTablaCategoriaCliente'])
                lstTablaAsesorComercial = json.loads(request.POST['lstTablaAsesorComercial'])
                lstIndicadoresDetallados = [lstTablaCiudades, lstTablaZonas, lstTablaCategoriaCliente, lstTablaAsesorComercial]
                def fncGuardarIndicadorGeneral(strIndicador, fltObjetivo):
                    with transaction.atomic():
                        clsIndicadoresComercialesMdl.objects.create(
                            creation_date = datetime.now(),
                            indicator = strIndicador,
                            set = 'General',
                            objetive = float(fltObjetivo)
                        )
                def fncGuardarIndicadorDetallado(strIndicador, strSet, intSubset, fltObjetivo):
                    with transaction.atomic():
                        clsIndicadoresComercialesMdl.objects.create(
                            creation_date = datetime.now(),
                            indicator = strIndicador,
                            set = strSet,
                            subset = intSubset,
                            objetive = float(fltObjetivo)
                        )
                for i in lstIndicadoresGenerales:
                    if i['fltObjetivo'] != '':
                        fncGuardarIndicadorGeneral(i['strIndicador'], i['fltObjetivo'])
                for i in lstIndicadoresDetallados:
                    if len(i) >1:
                        for j in i:
                            fncGuardarIndicadorDetallado(j['intIndicador'], j['strSet'], j['intSubset'], j['fltObjetivoIndicador'])
                jsnData['strSuccess'] = 'Se ha establecido su planeación comercial'
                response = JsonResponse(jsnData, safe=False)
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
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'jsnConsultarIndicadorGeneralActual':
                jsnData['fltObjetivoGeneralActual'] = float(5300000)
                jsnData['fltRealGeneralActual'] = float(2700000)
                jsnData['strCumplimientoIndicador'] = '50%'
                response = JsonResponse(jsnData, safe=False)
            elif action == 'btnConsultarCiudadesjsn':
                lstSelect = fncRetornarDataSelectdct('modulo_configuracion_clssalidasalmacenmdl')
                if type(lstSelect) == str:
                    jsnData['strError'] = lstSelect
                    response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['lstSelect'] = lstSelect
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'btnConsultarZonasjsn':
                lstSelect = fncRetornarDataSelectdct('modulo_configuracion_clszonaclientemdl', 'customer_zone')
                if type(lstSelect) == str:
                    jsnData['strError'] = lstSelect
                    response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['lstSelect'] = lstSelect
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'btnConsultarCategoriaClientejsn':
                lstSelect = fncRetornarDataSelectdct('modulo_configuracion_clscategoriaclientemdl', 'customer_cat')
                if type(lstSelect) == str:
                    jsnData['strError'] = lstSelect
                    response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['lstSelect'] = lstSelect
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'btnConsultarAsesorComercialjsn':
                lstSelect = fncRetornarDataSelectdct('modulo_configuracion_clsasesorcomercialmdl', 'advisor')
                if type(lstSelect) == str:
                    jsnData['strError'] = lstSelect
                    response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['lstSelect'] = lstSelect
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'jsnConsultarIndicadorDetalladoActual':
                jsnData['fltObjetivo'] = float(5300000)
                jsnData['fltReal'] = float(2700000)
                jsnData['strCumplimientoIndicador'] = '50%'
                response = JsonResponse(jsnData, safe=False)
            elif action == 'jsnConsultarHistoricoIndicadorGeneral':
                intIndicadorGeneral = request.POST['intIndicadorGeneral']
                dctIndicadorAsesorComercial = fncRetornarDataGraficolst('General', intIndicadorGeneral)
                response = JsonResponse(dctIndicadorAsesorComercial, safe=False)
            elif action == 'jsnConsultarIndicadorDetalladoHistorico':
                strSet = request.POST['strSet']
                intIndicadorDetalladoHistorico = request.POST['intIndicadorDetalladoHistorico']
                intDetalleCategoriaActual = request.POST['intDetalleCategoriaActual']
                dctIndicadorCategoriaCliente = fncRetornarDataGraficolst(strSet, intIndicadorDetalladoHistorico, intDetalleCategoriaActual)
                response = JsonResponse(dctIndicadorCategoriaCliente, safe=False)
            else:
                jsnData['error'] = 'No se encontraron resultados'
        except Exception as e:
            jsnData['error'] = str(e)
            response = JsonResponse(jsnData, safe=False)
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Planeación comercial - Historico indicadores'
        return context

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
