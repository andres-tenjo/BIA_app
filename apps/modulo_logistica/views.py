import json
from datetime import datetime, date
from pandas import pandas as pd
from django_pandas.io import read_frame
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import urllib, base64

from django.db import transaction
from django.core.serializers import serialize
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, FormView
from django.urls import reverse_lazy

from apps.mixins import IsSuperuserMixin, ValidatePermissionRequiredMixin
from .forms import *
from .models import *
from apps.modulo_comercial.models import *
from apps.modulo_configuracion.models import *
from apps.modulo_configuracion.forms import *

''' Vista para la ventana productos '''
class ProductView(ListView):
    model = clsCatalogoProductosMdl
    template_name = 'modulo_logistica/productos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in clsCatalogoProductosMdl.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla de productos'
        return context

''' Vista para la ventana salidas de almacén'''
class WarehouseExitView(CreateView):
    model = WarehouseOutFlows
    form_class = WarehouseExitForm
    template_name = 'modulo_logistica/salidas_almacen.html'
    success_url = reverse_lazy("home")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_customer':
                data = []
                term = request.POST['term'].strip()
                if len(term):
                    order = Orders.objects.filter(
                        Q(identification__business_name__icontains=term) | 
                        Q(id__icontains=term))[0:10]
                for i in order:
                    item = i.toJSON()
                    item['value'] = i.identification.business_name
                    data.append(item)
            elif action == 'create_supplier':
                with transaction.atomic():
                    frmSupplier = clsCrearProveedorFrm(request.POST)
                    data = frmSupplier.save()
            elif action == 'supplier_debt':
                data = {}
                debt =  SupplierDebt.objects.filter(supplier_id=request.POST['id'])
                credit_value = request.POST['credit_value']
                self.upd_cart_sta(debt)
                if debt:
                    bd = debt.exclude(state="CE")
                    if bd:
                        cart = self.cartera(bd, credit_value)
                        data['cartera'] = cart
                else:
                    state = 'Activa'
                    msg = f'Se tiene un cupo disponible con el proveedor de $ {credit_value} para compra de crédito'
                    data['msg'] = msg
                    data['credit_value'] = credit_value
                    data['state'] = state
            elif action == 'search_products':
                data = []
                term = request.POST['term'].strip()
                ids_exclude = json.loads(request.POST['ids'])
                if len(term):
                    prods = clsCatalogoProductosMdl.objects.filter(
                        Q(product_desc__icontains=term) | 
                        Q(id__icontains=term) | 
                        Q(presentation__icontains=term))[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.product_desc
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    purch = json.loads(request.POST['sales'])
                    orders = OrderPurchase()
                    orders.supplier_id = purch['supplier']
                    orders.order_date = purch['order_date']
                    orders.pay_method = purch['pay_method']
                    orders.deliver_date = purch['deliver_date']
                    orders.deliver_hour = purch['deliver_hour']
                    orders.order_address = purch['order_address']
                    orders.obs = purch['observation']
                    orders.urgency_level = purch['urgency_level']
                    orders.subtotal = float(purch['subtotal'])
                    orders.iva = float(purch['iva'])
                    orders.dcto = float(purch['dcto'])
                    orders.total = float(purch['total'])
                    orders.save()
                    for i in purch['products']:
                        order_prods = OrderPurchaseDetail()
                        order_prods.order_purchase_id = orders.id
                        order_prods.product_id = i['id']
                        order_prods.cant = int(i['cant'])
                        order_prods.purch_price = float(i['price_udc'])
                        order_prods.subtotal = float(i['subtotal'])
                        order_prods.iva = float(i['iva'])
                        order_prods.dcto = float(i['desc'])
                        order_prods.total = float(i['total'])
                        order_prods.save()
                    data = {'id': orders.id}
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frmSup'] = clsCrearProveedorFrm()
        context['list_url'] = reverse_lazy('comercial:listar_pedidos')
        context['action'] = 'add'
        return context

''' Vista para la ventana inventario'''
class InventoryListView(ListView):
    model = Inventory
    template_name = 'modulo_logistica/inventario.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Inventory.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla de inventario'
        return context

''' Vista para la ventana catálogo de bodegas'''
class CatWareView(TemplateView):
    template_name = 'modulo_logistica/bod_cat.html'

''' Vista para crear bodega'''
class WarehouseCreateView(CreateView):
    #model = WarehouseCatalogue
    #form_class = WarehouseCatalogForm
    template_name = 'modulo_logistica/crear_bodega.html'
    success_url = reverse_lazy("logistica:listar_bodegas")
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                frmwarehouse = WarehouseCatalogForm(request.POST)
                data = frmwarehouse.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Bodega'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

''' Vista para cargar bodegas'''
class CatWareUploadView(TemplateView):
    template_name = 'modulo_logistica/bod_upload.html'

''' Vista para listado de bodegas'''
class WarehouseListView(ListView):
    #model = WarehouseCatalogue
    template_name = 'modulo_logistica/listar_bodegas.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in WarehouseCatalogue.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Listado de bodegas'
        context['create_url'] = reverse_lazy("logistica:crear_bodega")
        return context

''' Vista para entradas de almacén'''
class ReceptionOrdersView(TemplateView):
    template_name = 'modulo_logistica/recepcion.html'

''' Vista para picking pedidos'''
class PickingOrdersView(TemplateView):
    template_name = 'modulo_logistica/alistamiento_pedidos.html'

''' Vista para packing pedidos'''
class PackingOrdersView(TemplateView):
    template_name = 'modulo_logistica/embalaje.html'

''' Vista para cargue de pedidos'''
class LoadingTruckOrdersView(TemplateView):
    template_name = 'modulo_logistica/cargue_vehiculos.html'

''' Vista para conteo de inventarios'''
class InventoryCountView(TemplateView):
    template_name = 'modulo_logistica/conteo_inventario.html'

def remision_etiquetas(request):
    return render(request, 'modulo_logistica/remision_etiquetas.html')

''' Vista para conteo de inventarios'''
class DeliveryRouteView(TemplateView):
    template_name = 'modulo_logistica/ruta_entrega.html'

# Vehiculos
''' Vista para la ventana catálogo de vehiculos'''
class CatVehicView(TemplateView):
    template_name = 'modulo_logistica/cat_veh.html'

''' Vista para crear bodega'''
class VehicleCreateView(CreateView):
    #model = VehicleCatalogue
    #form_class = VehiclecatalogForm
    template_name = 'modulo_logistica/crear_vehiculo.html'
    success_url = reverse_lazy("logistica:listar_vehiculos")
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                frmvehicle = VehiclecatalogForm(request.POST)
                data = frmvehicle.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Vehiculo'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

''' Vista para cargar bodegas'''
class CatVehicUploadView(TemplateView):
    template_name = 'modulo_logistica/veh_upload.html'

''' Vista para listado de bodegas'''
class VehicleListView(ListView):
    #model = VehicleCatalogue
    template_name = 'modulo_logistica/listar_vehiculos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in VehicleCatalogue.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Listado de vehiculos'
        context['create_url'] = reverse_lazy("logistica:crear_vehiculo")
        return context

def hist_mov_logistica(request):
    return render(request, 'modulo_logistica/hist_mov_logistica.html')

''' Vista para ventana de indicadores logistica'''
class LogisticsWarehouseIndicatorsView(TemplateView):
    template_name = 'modulo_logistica/indicadores_almacen.html'

class LogisticsTransportIndicatorsView(TemplateView):
    template_name = 'modulo_logistica/indicadores_transporte.html'