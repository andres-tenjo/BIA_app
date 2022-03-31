# Python libraries
import json
from datetime import datetime, date
from pandas import pandas as pd
from django_pandas.io import read_frame
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import urllib, base64

# Modelos BIA
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

# Django libraries
from apps.mixins import IsSuperuserMixin, ValidatePermissionRequiredMixin
from .forms import *
from .models import *
from apps.modulo_comercial.models import *
from apps.modulo_configuracion.models import *
from apps.modulo_configuracion.forms import *
from apps.functions_views import *
from apps.modulo_configuracion.api.serializers import *

################################################################################################
################################### VISTAS DEL MODULO ALMACEN ##################################
################################################################################################

#################################################################################################
# 1. PRODUCTOS
#################################################################################################
''' 1.1 Vista para ver productos '''
class clsVerCatalogoProductosViw(LoginRequiredMixin, ListView):
    model = clsCatalogoProductosMdl
    template_name = 'modulo_almacen/ver_productos.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'slcBuscarProductosjsn':
                jsnData = []
                strBuscarProducto = request.POST['term'].strip()
                if len(strBuscarProducto):
                    qrsCatalogoProductos = clsCatalogoProductosMdl.objects.filter(Q(product_desc__icontains=strBuscarProducto) | Q(id__icontains=strBuscarProducto))[0:10]
                for i in qrsCatalogoProductos:
                    dctJsn = i.toJSON()
                    dctJsn['value'] = i.product_desc
                    jsnData.append(dctJsn)
            elif action == 'frmEliminarProductojsn':
                qrsCatalogoProductos = clsCatalogoProductosMdl.objects.get(pk=request.POST['id'])
                if qrsCatalogoProductos.state == "AC":
                    qrsCatalogoProductos.state = "IN"
                    qrsCatalogoProductos.save()
                else:
                    qrsCatalogoProductos.state = "AC"
                    qrsCatalogoProductos.save()
                jsnData = qrsCatalogoProductos.toJSON()
            else:
                jsnData['error'] = 'Ha ocurrido un error'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Búsqueda de Productos'
        return context

#################################################################################################
# 2. ENTRADAS DE ALMACEN
#################################################################################################
''' 2.1 Vista menu entradas de almacén'''
class clsMenuEntradasAlmacenViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_almacen/entradas_almacen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Crear entrada de almacen'
        context['create_url'] = reverse_lazy('almacen:crear_entrada_almacen')
        context['search_title'] = 'Ver entradas de almacen'
        context['search_url'] = reverse_lazy('almacen:ver_entradas_almacen')
        return context

''' 2.2 Vista crear entrada de almacén'''
class clsCrearEntradaAlmacenViw(CreateView):
    model = clsPedidosMdl
    # form_class = WarehouseEntryForm
    template_name = 'modulo_almacen/crear_entrada_almacen.html'
    success_url = reverse_lazy("almacen:ver_entradas_almacen")

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
                    cust = clsCatalogoClientesMdl.objects.filter(Q(id_number__icontains=term) | Q(customer__icontains=term) | Q(cel_number__icontains=term))[0:10]
                for i in cust:
                    item = i.toJSON()
                    item['value'] = i.customer
                    data.append(item)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear entrada almacen'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

''' 2.3 Vista para ver entradas de almacen'''
class clsVerEntradasAlmacenViw(ListView):
    # model = ScheduleCall
    template_name = 'modulo_almacen/ver_entrada_almacen.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla entradas de almacen'
        context['create_url'] = reverse_lazy("compras:crear_negociacion")
        return context

#################################################################################################
# 3. SALIDAS DE ALMACEN
#################################################################################################
''' 3.1 Vista menu salidas de almacén'''
class clsMenuSalidasAlmacenViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_almacen/salidas_almacen.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Crear salida de almacen'
        context['create_url'] = reverse_lazy('almacen:crear_salida_almacen')
        context['search_title'] = 'Ver salidas de almacen'
        context['search_url'] = reverse_lazy('almacen:ver_salidas_almacen')
        return context

''' 3.2 Vista crear salida de almacén'''
class clsCrearSalidaAlmacenViw(CreateView):
    # model = WarehouseOutFlows
    # form_class = WarehouseExitForm
    template_name = 'modulo_almacen/crear_salida_almacen.html'
    success_url = reverse_lazy('almacen:ver_salidas_almacen')

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
                    order = clsPedidosMdl.objects.filter(
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
                        Q(id__icontains=term))[0:10]
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
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

''' 3.3 Vista ver salidas de almacén'''
class clsVerSalidasAlmacenViw(ListView):
    # model = ScheduleCall
    template_name = 'modulo_almacen/ver_salida_almacen.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla salidas de almacen'
        context['create_url'] = reverse_lazy("compras:crear_salida_almacen")
        return context

#################################################################################################
# 4. INVENTARIO
#################################################################################################
''' 4.1 Vista para menu inventario'''
class clsMenuInventarioViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_almacen/inventario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Crear inventario'
        context['create_url'] = reverse_lazy('almacen:crear_inventario')
        context['search_title'] = 'Ver inventario'
        context['search_url'] = reverse_lazy('almacen:ver_inventarios')
        return context

''' 4.2 Vista para crear inventario'''
class clsCrearInventarioViw(CreateView):
    # model = WarehouseOutFlows
    # form_class = WarehouseExitForm
    template_name = 'modulo_almacen/crear_inventario.html'
    success_url = reverse_lazy('almacen:ver_inventarios')

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
                    order = clsPedidosMdl.objects.filter(
                        Q(identification__business_name__icontains=term) | 
                        Q(id__icontains=term))[0:10]
                for i in order:
                    item = i.toJSON()
                    item['value'] = i.identification.business_name
                    data.append(item)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frmSup'] = clsCrearProveedorFrm()
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

''' 4.3 Vista para ver inventarios'''
class clsVerInventarioViw(ListView):
    # model = Inventory
    template_name = 'modulo_almacen/ver_inventario.html'

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

#################################################################################################
# 5. CATÁLOGO DE BODEGAS
#################################################################################################

''' 5.1 Vista para la ventana catálogo de bodegas'''
class clsMenuCatalogoBodegasViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_almacen/catalogo_bodegas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Crear bodega'
        context['create_url'] = reverse_lazy('almacen:crear_bodega')
        context['search_title'] = 'Buscar bodega'
        context['search_url'] = reverse_lazy('almacen:ver_bodegas')
        return context

''' 5.2 Vista para crear bodega'''
class clsCrearBodegaViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = clsCatalogoBodegasMdl
    form_class = clsCatalogoBodegasFrm
    template_name = 'modulo_almacen/crear_bodega.html'
    success_url = reverse_lazy("almacen:ver_bodegas")
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCrearBodegajsn':
                with transaction.atomic():
                    frmCrearBodega = clsCatalogoBodegasFrm(request.POST)
                    jsnData = frmCrearBodega.save()
            elif action == 'slcFiltrarCiudadesjsn':
                jsnData = [{'id': '', 'text': '------------'}]
                for i in clsCiudadesMdl.objects.filter(department_id=request.POST['intId']):
                    jsnData.append({'id': i.id, 'text': i.city_name})
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear bodega'
        context['create_url'] = reverse_lazy('almacen:crear_bodega')
        context['list_url'] = self.success_url
        context['action'] = 'frmCrearBodegajsn'
        return context

''' 5.3 Vista para ver e inactivar bodegas'''
class clsVerCatalogoBodegasViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = clsCatalogoBodegasMdl
    template_name = 'modulo_almacen/ver_bodegas.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'slcBuscarBodegajsn':
                jsnData = []
                strBodega = request.POST['term'].strip()
                if len(strBodega):
                    qrsCatalogoBodegas = clsCatalogoBodegasMdl.objects.filter(Q(warehouse_name__icontains=strBodega) | Q(contact_name__icontains=strBodega))[0:10]
                for i in qrsCatalogoBodegas:
                    dctJsn = i.toJSON()
                    dctJsn['value'] = i.warehouse_name
                    jsnData.append(dctJsn)
            elif action == 'btnEliminarBodegajsn':
                qrsCatalogoBodegas = clsCatalogoBodegasMdl.objects.get(pk=request.POST['id'])
                if qrsCatalogoBodegas.state == "AC":
                    qrsCatalogoBodegas.state = "IN"
                    qrsCatalogoBodegas.save()
                else:
                    qrsCatalogoBodegas.state = "AC"
                    qrsCatalogoBodegas.save()
                jsnData = qrsCatalogoBodegas.toJSON()
            else:
                jsnData['error'] = 'Ha ocurrido un error'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla de Bodegas'
        context['create_url'] = reverse_lazy('almacen:crear_bodega')
        context['list_url'] = reverse_lazy('almacen:ver_bodegas')
        return context

''' 5.4 Vista para editar bodega'''
class clsEditarBodegaViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = clsCatalogoBodegasMdl
    form_class = clsCatalogoBodegasFrm
    template_name = 'modulo_almacen/crear_bodega.html'
    success_url = reverse_lazy("almacen:ver_bodegas")
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmEditarBodegajsn':
                frmEditarBodega = self.get_form()
                jsnData = frmEditarBodega.save()
            elif action == 'slcFiltrarCiudadesjsn':
                jsnData = [{'id': '', 'text': '------------'}]
                for i in clsCiudadesMdl.objects.filter(department_id=request.POST['intId']):
                    jsnData.append({'id': i.id, 'text': i.city_name})
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar bodega'
        context['create_url'] = reverse_lazy('almacen:crear_bodega')
        context['list_url'] = self.success_url
        context['action'] = 'frmEditarBodegajsn'
        return context
