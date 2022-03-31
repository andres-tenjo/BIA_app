# Python libraries
import json
from datetime import datetime, date
from pandas import pandas as pd
from django_pandas.io import read_frame
import matplotlib.pyplot as plt
from io import BytesIO
import urllib, base64

# Modelos BIA
from apps.Modelos.Several_func import *
from apps.Modelos.Update_Balances import *
from apps.Modelos.Parameters import *

# Django libraries
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
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, FormView, View
from django.urls import reverse_lazy

# Django-rest libraries
from rest_framework.views import APIView
from rest_framework.response import Response

# BIA files
from apps.mixins import ValidatePermissionRequiredMixin
from .forms import *
from .models import *
from apps.modulo_comercial.models import *
from apps.modulo_configuracion.models import *
from apps.modulo_configuracion.forms import *
from apps.modulo_comercial.forms import *
from apps.functions_views import *
from apps.modulo_configuracion.api.serializers import *

################################################################################################
################################### VISTAS DEL MODULO COMPRAS ##################################
################################################################################################

#################################################################################################
# 1. NEGOCIACIÓN
#################################################################################################
''' 1.1 Vista para menu negociación proveedores'''
class clsMenuNegociacionProveedoresViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_compras/negociacion_proveedor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Iniciar negociación'
        context['create_url'] = reverse_lazy('compras:crear_negociacion')
        context['search_title'] = 'Ver negociaciones'
        context['search_url'] = reverse_lazy('compras:ver_negociacion')
        return context

''' 1.2 Vista para crear negociación con proveedor'''
class clsCrearNegociacionViw(CreateView):
    model = clsPedidosMdl
    # form_class = OrderForm
    template_name = 'modulo_compras/crear_negociacion.html'
    success_url = reverse_lazy("compras:ver_negociacion")

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
        context['title'] = 'Crear negociación'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

''' 1.3 Vista para ver negociacones'''
class clsVerNegociacionesViw(ListView):
    # model = ScheduleCall
    template_name = 'modulo_compras/ver_negociaciones.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla negociaciones'
        context['create_url'] = reverse_lazy("compras:crear_negociacion")
        return context

#################################################################################################
# 2. PROMOCIONES
#################################################################################################
''' 2.1 Vista para menu promociones'''
class clsMenuPromocionesViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_compras/promociones.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Crear promoción'
        context['create_url'] = reverse_lazy('compras:crear_promocion')
        context['search_title'] = 'Ver promociones'
        context['search_url'] = reverse_lazy('compras:ver_promociones')
        return context

''' 2.2 Vista para crear promociones'''
class clsCrearPromocionesView(CreateView):
    # model = ScheduleCall
    # form_class = ScheduleCallForm
    template_name = 'modulo_compras/crear_promocion.html'
    success_url = reverse_lazy('compras:ver_promociones')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear promoción'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

''' 2.3 Vista para ver promociones'''
class clsVerPromocionesViw(ListView):
    # model = ScheduleCall
    template_name = 'modulo_compras/ver_promociones.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla promociones'
        context['create_url'] = reverse_lazy("compras:crear_promocion")
        return context

#################################################################################################
# 3. ORDEN DE COMPRA
#################################################################################################
''' 3.1 Vista para menu ordenes de compra'''
class clsMenuOrdenesCompraViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_compras/ordenes_compra.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Crear orden de compra'
        context['create_url'] = reverse_lazy('compras:crear_orden_compra')
        context['search_title'] = 'Ver ordenes de compra'
        context['search_url'] = reverse_lazy('compras:ver_orden_compra')
        return context

''' 3.2 Vista para crear orden de compra'''
class clsCrearOrdenCompraViw(CreateView):
    # model = OrderPurchase
    # form_class = OrderPurchaseForm
    template_name = 'modulo_compras/crear_orden_compra.html'
    success_url = reverse_lazy("home")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def upd_cart_sta(self, bd):
        date_today = date.today()
        for i in bd:
            if i.state == 'AC' and i.next_payment_date < date_today:
                i.state = 'VE'
                i.save()

    def cartera(self, bd, credit_value):
        l = None
        cartera = bd.to_dataframe()
        cartera = cartera.drop(['user_creation', 'date_creation', 'user_update', 'date_update','movement_type', 'credit_value', 'balance_credit_value'], axis=1)
        if cartera[cartera['state'] == 'Vencida'].empty == False and cartera[cartera['state'] == 'Activa'].empty == False:
            state = 'Vencida'
            min_pay = float(cartera[cartera['state'] == 'Vencida']['balance_payment'].sum())
            total_pay = float(cartera[cartera['state'] == 'Activa']['balance_payment'].sum()) + min_pay
            msg = f'Se presenta una mora con el proveedor de $ {min_pay} con pago inmediato'
            l = [state, credit_value, min_pay, total_pay, msg]
        elif cartera[cartera['state'] == 'Vencida'].empty == False:
            state = 'Vencida'
            min_pay = float(cartera[cartera['state'] == 'Vencida']['balance_payment'].sum())
            total_pay = float(cartera[cartera['state'] == 'Vencida']['balance_payment'].sum())
            msg = f'Se presenta una mora con el proveedor de $ {min_pay} con pago inmediato'
            l = [state, credit_value, min_pay, total_pay, msg]
        elif cartera[cartera['state'] == 'Activa'].empty == False:
            state = 'Activa'
            min_pay = 0
            total_pay = float(cartera[cartera['state'] == 'Activa']['balance_payment'].sum())
            msg = f'Se tiene un cupo disponible con el proveedor de $ {credit_value} para compra de crédito'
            l = [state, credit_value, min_pay, total_pay, msg]
        return l

    def post(self,request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_supplier':
                data = []
                term = request.POST['term'].strip()
                if len(term):
                    sup = clsCatalogoProveedoresMdl.objects.filter(
                        Q(identification__icontains=term) | 
                        Q(supplier_name__icontains=term) | 
                        Q(contact_name__icontains=term))[0:10]
                for i in sup:
                    item = i.toJSON()
                    item['value'] = i.supplier_name
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
        context['list_url'] = reverse_lazy('compras:ver_orden_compra')
        context['action'] = 'add'
        return context

''' 3.3 Vista para ver ordenes de compra'''
class clsVerOrdenesCompraViw(ListView):
    # model = ScheduleCall
    template_name = 'modulo_compras/ver_ordenes_compra.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla ordenes de compra'
        context['create_url'] = reverse_lazy("compras:crear_orden_compra")
        return context

''' 3.4 Vista para imprimir ordenes de compra'''


#################################################################################################
# 4. COTIZACIONES PROVEEDORES
#################################################################################################
''' 4.1 Vista para menu ordenes de compra'''
class clsMenuCotizacionProveedorViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_compras/cotizacion_proveedor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Crear cotización'
        context['create_url'] = reverse_lazy('compras:crear_cotizacion_proveedor')
        context['search_title'] = 'Ver cotizaciones'
        context['search_url'] = reverse_lazy('compras:ver_cotizacion_proveedor')
        return context

''' 4.2 Vista para la ventana crear cotización'''
class clsCrearCotizacionViw(CreateView):
    # model = SupplierQuote
    # form_class = SupplierQuoteForm
    template_name = 'modulo_compras/crear_cotizacion.html'
    success_url = reverse_lazy('compras:ver_cotizacion_proveedor')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_supplier':
                data = []
                term = request.POST['term'].strip()
                if len(term):
                    sup = clsCatalogoProveedoresMdl.objects.filter(
                        Q(identification__icontains=term) | 
                        Q(supplier_name__icontains=term) | 
                        Q(contact_name__icontains=term))[0:10]
                for i in sup:
                    item = i.toJSON()
                    item['value'] = i.supplier_name
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

''' 4.3 Vista para la ventana ver cotizaciones'''
class clsVerCotizacionesViw(ListView):
    # model = ScheduleCall
    template_name = 'modulo_compras/ver_cotizaciones.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla cotizaciones'
        context['create_url'] = reverse_lazy("compras:crear_cotizacion_proveedor")
        return context

#################################################################################################
# 5. CATALOGO DE PRODUCTOS
#################################################################################################
''' 5.1 Vista menú catálogo de productos'''
class clsMenuCatalogoProductosViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_compras/catalogo_productos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options_title'] = 'Opciones de catálogo'
        context['options_url'] = reverse_lazy('compras:opciones_producto')
        context['create_title'] = 'Crear producto'
        context['create_url'] = reverse_lazy('compras:crear_producto')
        context['search_title'] = 'Ver productos'
        context['search_url'] = reverse_lazy('compras:listar_productos')
        return context

''' 5.2 Vista opciones producto'''
class clsOpcionesCatalogoProductoViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modulo_compras/opciones_catalogo_productos.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCrearCategoriaProductojsn':
                with transaction.atomic():
                    frmCategoriaProducto = clsCrearCategoriaProductoFrm(request.POST)
                    jsnData = frmCategoriaProducto.save()
            elif action == 'tblCategoriaProductojsn':
                jsnData = []
                for i in clsCategoriaProductoMdl.objects.all():
                    jsnData.append(i.toJSON())
                for i in range(0, len(jsnData)):
                    jsnData[i]['n'] = i + 1
            elif action == 'frmEditarCategoriaProductojsn':
                qrsCategoriaProducto = clsCategoriaProductoMdl.objects.get(pk=int(request.POST['id']))
                qrsCategoriaProducto.product_cat = request.POST['product_cat']
                qrsCategoriaProducto.save()
            elif action == 'frmEliminarCategoriaProductojsn':
                qrsCategoriaProducto = clsCategoriaProductoMdl.objects.get(pk=request.POST['id'])
                if qrsCategoriaProducto.state == "AC":
                    qrsCategoriaProducto.state = "IN"
                    qrsCategoriaProducto.save()
                else:
                    qrsCategoriaProducto.state = "AC"
                    qrsCategoriaProducto.save()
                qrsSubcategoriaProducto = clsSubcategoriaProductoMdl.objects.filter(product_cat_id=request.POST['id'])
                if qrsSubcategoriaProducto:
                    for i in qrsSubcategoriaProducto:
                        if i.state == "AC":
                            i.state = "IN"
                            i.save()
                        else:
                            i.state = "AC"
                            i.save()
            elif action == 'slcCategoriaProductojsn':
                jsnData = []
                qrsCategoriaProducto =  clsCategoriaProductoMdl.objects.filter(state='AC')
                for i in qrsCategoriaProducto:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.product_cat
                    jsnData.append(dctJsn)
            elif action == 'frmCrearSubcategoriaProductojsn':
                with transaction.atomic():
                    frmSubcategoriaProducto = clsCrearSubcategoriaProductoFrm(request.POST)
                    jsnData = frmSubcategoriaProducto.save()
            elif action == 'frmEditarSubcategoriaProductojsn':
                qrsSubcategoriaProducto = clsSubcategoriaProductoMdl.objects.get(pk=int(request.POST['id']))
                qrsSubcategoriaProducto.product_subcat = request.POST['product_subcat']
                qrsSubcategoriaProducto.product_cat_id = request.POST['product_cat']
                qrsSubcategoriaProducto.save()
            elif action == 'tblSubcategoriaProductojsn':
                jsnData = []
                for i in clsSubcategoriaProductoMdl.objects.all():
                    jsnData.append(i.toJSON())
                for i in range(0, len(jsnData)):
                    jsnData[i]['n'] = i + 1
            elif action == 'frmEliminarSubcategoriaProductojsn':
                qrsSubcategoriaProducto = clsSubcategoriaProductoMdl.objects.get(pk=request.POST['id'])
                if qrsSubcategoriaProducto.state == "AC":
                    qrsSubcategoriaProducto.state = "IN"
                    qrsSubcategoriaProducto.save()
                else:
                    qrsSubcategoriaProducto.state = "AC"
                    qrsSubcategoriaProducto.save()
            elif action == 'frmCrearUnidadComprajsn':
                with transaction.atomic():
                    frmUnidadCompra = clsCrearUnidadCompraFrm(request.POST)
                    jsnData = frmUnidadCompra.save()
            elif action == 'frmEditarUnidadComprajsn':
                qrsUnidadCompra = clsUnidadCompraMdl.objects.get(pk=int(request.POST['id']))
                qrsUnidadCompra.purchase_unit = request.POST['purchase_unit']
                qrsUnidadCompra.save()
            elif action == 'tblUnidadComprajsn':
                jsnData = []
                for i in clsUnidadCompraMdl.objects.all():
                    jsnData.append(i.toJSON())
                for i in range(0, len(jsnData)):
                    jsnData[i]['n'] = i + 1
            elif action == 'frmEliminarUnidadComprajsn':
                qrsUnidadCompra = clsUnidadCompraMdl.objects.get(pk=request.POST['id'])
                if qrsUnidadCompra.state == "AC":
                    qrsUnidadCompra.state = "IN"
                    qrsUnidadCompra.save()
                else:
                    qrsUnidadCompra.state = "AC"
                    qrsUnidadCompra.save()
            elif action == 'frmCrearUnidadVentajsn':
                with transaction.atomic():
                    frmUnidadVenta = clsCrearUnidadVentaFrm(request.POST)
                    jsnData = frmUnidadVenta.save()
            elif action == 'frmEditarUnidadVentajsn':
                qrsUnidadVenta = clsUnidadVentaMdl.objects.get(pk=int(request.POST['id']))
                qrsUnidadVenta.sales_unit = request.POST['sales_unit']
                qrsUnidadVenta.save()
            elif action == 'tblUnidadVentajsn':
                jsnData = []
                for i in clsUnidadVentaMdl.objects.all():
                    jsnData.append(i.toJSON())
                for i in range(0, len(jsnData)):
                    jsnData[i]['n'] = i + 1
            elif action == 'frmEliminarUnidadVentajsn':
                qrsUnidadVenta = clsUnidadVentaMdl.objects.get(pk=request.POST['id'])
                if qrsUnidadVenta.state == "AC":
                    qrsUnidadVenta.state = "IN"
                    qrsUnidadVenta.save()
                else:
                    qrsUnidadVenta.state = "AC"
                    qrsUnidadVenta.save()
            elif action == 'btnExportarCatalogojsn':
                qrsCategoriaProducto =  clsCategoriaProductoMdl.objects.filter(state='AC')
                if not qrsCategoriaProducto:
                    strMensaje = 'Para cargar productos masivos, debe crear categorías de producto'
                    jsnData['error'] = strMensaje
                qrsSubcategoriaProducto = clsSubcategoriaProductoMdl.objects.filter(state='AC')
                if not qrsSubcategoriaProducto:
                    strMensaje = 'Para cargar productos masivos, debe crear subcategorías de producto'
                    jsnData['error'] = strMensaje
                qrsUnidadCompra = clsUnidadCompraMdl.objects.filter(state='AC')
                if not qrsUnidadCompra:
                    strMensaje = 'Para cargar productos masivos, debe crear unidades de compra de producto'
                    jsnData['error'] = strMensaje
                qrsUnidadVenta = clsUnidadVentaMdl.objects.filter(state='AC')
                if not qrsUnidadVenta:
                    strMensaje = 'Para cargar productos masivos, debe crear unidades de venta de producto'
                    jsnData['error'] = strMensaje
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('compras:crear_producto')
        context['list_url'] = reverse_lazy("compras:listar_productos")
        context['frmProductCat'] = clsCrearCategoriaProductoFrm()
        context['frmProductSub'] = clsCrearSubcategoriaProductoFrm()
        context['frmUdcProd'] = clsCrearUnidadCompraFrm()
        context['frmUdvProd'] = clsCrearUnidadVentaFrm()
        return context

''' 5.3 Vista para importar archivo de productos'''
class clsImportarCatalogoProductosViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_compras/importar_catalogo_productos.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lstNombresColumnas = [
            'Descripción producto',
            'Código de barras',
            'Marca',
            'Categoría producto',
            'Subcategoría producto',
            'Unidad de compra',
            'Cantidad unidad de compra',
            'Precio de compra',
            'Unidad de venta',   
            'Cantidad unidad de venta',
            'Precio de venta',
            'Iva',
            'Otros impuestos',
            'Tiempo de entrega proveedor'
            ]
        tplValidaciones = (
            ((False,), (True, 60), (True, 1), (False,)),
            ((True, 'bar_code', clsCatalogoProductosMdl), (True, 20), (True, 1), (False,)),
            ((False,), (True, 60), (True, 1), (False,)),
            ((False,), (True, 2), (True, 1), (True, clsCategoriaProductoMdl)),
            ((False,), (True, 2), (True, 1), (True, clsSubcategoriaProductoMdl)),
            ((False,), (True, 2), (True, 1), (True, clsUnidadCompraMdl)),
            ((True, int), (True, 3), (True, 1), (False,)),
            ((True, float), (True, 13), (True, 2), (False,)),
            ((False,), (True, 2), (True, 1), (True, clsUnidadVentaMdl)),
            ((True, int), (True, 3), (True, 1), (False,)),
            ((True, float), (True, 13), (True, 2), (False,)),
            ((True, float), (True, 30), (True, 1), (False,)),
            ((True, float), (True, 5), (True, 1), (False,)),
            ((True, float), (True, 5), (True, 1), (False,)),
            )
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCargarArchivojsn':
                filCatalogoProductos = request.FILES['file']
                if str(filCatalogoProductos).endswith('.xlsx'):
                    dtfProductos = pd.read_excel(filCatalogoProductos)
                    dtfProductos = dtfProductos.fillna(0)
                    lstValidarImportacion = [ fncValidarImportacionlst(dtfProductos, i, j) for (i, j) in zip(lstNombresColumnas, tplValidaciones) ]
                    lstValidarImportacion = [ i for n in lstValidarImportacion for i in n ]
                    if len(lstValidarImportacion):
                        jsnProductos = dtfProductos.to_json(orient="split")
                        jsnData['jsnProductos'] = jsnProductos
                        jsnData['lstValidarImportacion'] = lstValidarImportacion
                        jsnData['strErrorArchivo'] = 'El archivo presenta errores, desea descargarlos?'
                        response = JsonResponse(jsnData, safe=False)
                    else:
                        with transaction.atomic():
                            for i in (dtfProductos.values.tolist()):
                                if int(i[1]) > 0:
                                    clsCatalogoProductosMdl.objects.create(
                                    product_desc = i[0],
                                    bar_code = int(i[1]),
                                    trademark = i[2],
                                    product_cat_id = int(i[3]),
                                    product_subcat_id = int(i[4]),
                                    purchase_unit_id = int(i[5]),
                                    quantity_pu = int(i[6]),
                                    cost_pu = float(i[7]),
                                    sales_unit_id = int(i[8]),
                                    quantity_su = int(i[9]),
                                    full_sale_price = float(i[10]),
                                    split = int(i[6]/i[9]),
                                    iva = float(i[11]),
                                    other_tax = float(i[12]),
                                    supplier_lead_time = int(i[13])
                                    )
                                else:
                                    clsCatalogoProductosMdl.objects.create(
                                    product_desc = i[0],
                                    trademark = i[2],
                                    product_cat_id = int(i[3]),
                                    product_subcat_id = int(i[4]),
                                    purchase_unit_id = int(i[5]),
                                    quantity_pu = int(i[6]),
                                    cost_pu = float(i[7]),
                                    sales_unit_id = int(i[8]),
                                    quantity_su = int(i[9]),
                                    full_sale_price = float(i[10]),
                                    split = int(i[6]/i[9]),
                                    iva = float(i[11]),
                                    other_tax = float(i[12]),
                                    supplier_lead_time = int(i[13])
                                    )
                        jsnData['success'] = '¡Se ha cargado el archivo a su base de datos con éxito!'
                        response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['error'] = 'Compruebe el formato del archivo'
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'btnArchivoErroresjsn':
                jsnProductos = request.POST['jsnProductos']
                dtfProductos = pd.read_json(jsnProductos, orient='split')
                lstValidarImportacion = json.loads(request.POST['lstValidarImportacion'])
                lstErroresCeldas = list( dict.fromkeys([ i[1] for i in lstValidarImportacion ]) )
                dtfProductos = fncAgregarErroresDataframedtf(dtfProductos, lstValidarImportacion, lstErroresCeldas)
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="catalogo_productos.xlsx"'
                with pd.ExcelWriter(response) as writer:
                    dtfProductos.to_excel(writer, sheet_name='VALIDAR', index=False)
                    fncAgregarFormatoColumnasError(writer, lstValidarImportacion, 'VALIDAR', lstNombresColumnas)
                    fncAgregarAnchoColumna(writer, False, dtfProductos, 'VALIDAR')
        except Exception as e:
            jsnData['error'] = str(e)
            response = JsonResponse(jsnData, safe=False)
        return response

''' 5.4 Vista para crear producto'''
class clsCrearProductoViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = clsCatalogoProductosMdl
    form_class = clsCrearProductoFrm
    template_name = 'modulo_compras/crear_producto.html'
    success_url = reverse_lazy("compras:listar_productos")
    url_redirect = success_url
    permission_required = 'bia_add_productcatalogue'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCrearProductojsn':
                frmCrearProducto = clsCrearProductoFrm(request.POST)
                jsnData = frmCrearProducto.save()
            elif action == 'frmCrearCategoriaProductojsn':
                with transaction.atomic():
                    frmCrearCategoriaProducto = clsCrearCategoriaProductoFrm(request.POST)
                    jsnData = frmCrearCategoriaProducto.save()
            elif action == 'frmCrearSubcategoriaProductojsn':
                with transaction.atomic():
                    frmCrearSubcategoriaProducto = clsCrearSubcategoriaProductoFrm(request.POST)
                    jsnData = frmCrearSubcategoriaProducto.save()
            elif action == 'frmCrearUnidadComprajsn':
                with transaction.atomic():
                    frmUnidadCompra = clsCrearUnidadCompraFrm(request.POST)
                    jsnData = frmUnidadCompra.save()
            elif action == 'frmCrearUnidadVentajsn':
                with transaction.atomic():
                    frmUnidadVenta = clsCrearUnidadVentaFrm(request.POST)
                    jsnData = frmUnidadVenta.save()
            elif action == 'slcBuscarCategoriaProductojsn':
                jsnData = []
                qrsCategoriaProducto = clsCategoriaProductoMdl.objects.all()
                for i in qrsCategoriaProducto:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.product_cat
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarSubcategoriaProductojsn':
                jsnData = []
                qrsSubcategoriaProducto =clsSubcategoriaProductoMdl.objects.all()
                for i in qrsSubcategoriaProducto:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.product_subcat
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarUnidadComprajsn':
                jsnData = []
                qrsUnidadCompra =clsUnidadCompraMdl.objects.all()
                for i in qrsUnidadCompra:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.purchase_unit
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarUnidadVentajsn':
                jsnData = []
                qrsUnidadVenta =clsUnidadVentaMdl.objects.all()
                for i in qrsUnidadVenta:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.sales_unit
                    jsnData.append(dctJsn)
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Producto'
        context['create_url'] = reverse_lazy('compras:crear_producto')
        context['list_url'] = self.success_url
        context['action'] = 'frmCrearProductojsn'
        context['frmProductCat'] = clsCrearCategoriaProductoFrm()
        context['frmProductSub'] = clsCrearSubcategoriaProductoFrm()
        context['frmUdcProd'] = clsCrearUnidadCompraFrm()
        context['frmUdvProd'] = clsCrearUnidadVentaFrm()
        return context

''' 5.5 Vista para listar e inactivar productos'''
class clsListarCatalogoProductosViw(LoginRequiredMixin, ListView):
    model = clsCatalogoProductosMdl
    template_name = 'modulo_compras/ver_productos.html'

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
        context['create_url'] = reverse_lazy('compras:crear_producto')
        context['list_url'] = reverse_lazy("compras:listar_productos")
        context['options_url'] = reverse_lazy('compras:opciones_producto')
        return context

''' 5.6 Vista para editar producto'''
class clsEditarProductoViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = clsCatalogoProductosMdl
    form_class = clsCrearProductoFrm
    template_name = 'modulo_compras/crear_producto.html'
    success_url = reverse_lazy("compras:listar_productos")
    permission_required = 'bia_change_productcatalogue'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmEditarProductojsn':
                frmEditarProducto = self.get_form()
                jsnData = frmEditarProducto.save()
            elif action == 'frmCrearCategoriaProductojsn':
                with transaction.atomic():
                    frmCrearCategoriaProducto = clsCrearCategoriaProductoFrm(request.POST)
                    jsnData = frmCrearCategoriaProducto.save()
            elif action == 'frmCrearSubcategoriaProductojsn':
                with transaction.atomic():
                    frmCrearSubcategoriaProducto = clsCrearSubcategoriaProductoFrm(request.POST)
                    jsnData = frmCrearSubcategoriaProducto.save()
            elif action == 'frmCrearUnidadComprajsn':
                with transaction.atomic():
                    frmUnidadCompra = clsCrearUnidadCompraFrm(request.POST)
                    jsnData = frmUnidadCompra.save()
            elif action == 'frmCrearUnidadVentajsn':
                with transaction.atomic():
                    frmUnidadVenta = clsCrearUnidadVentaFrm(request.POST)
                    jsnData = frmUnidadVenta.save()
            elif action == 'slcBuscarCategoriaProductojsn':
                jsnData = []
                qrsCategoriaProducto = clsCategoriaProductoMdl.objects.all()
                for i in qrsCategoriaProducto:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.product_cat
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarSubcategoriaProductojsn':
                jsnData = []
                qrsSubcategoriaProducto =clsSubcategoriaProductoMdl.objects.all()
                for i in qrsSubcategoriaProducto:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.product_subcat
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarUnidadComprajsn':
                jsnData = []
                qrsUnidadCompra =clsUnidadCompraMdl.objects.all()
                for i in qrsUnidadCompra:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.purchase_unit
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarUnidadVentajsn':
                jsnData = []
                qrsUnidadVenta =clsUnidadVentaMdl.objects.all()
                for i in qrsUnidadVenta:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.sales_unit
                    jsnData.append(dctJsn)
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar producto'
        context['list_url'] = self.success_url
        context['action'] = 'frmEditarProductojsn'
        context['frmProductCat'] = clsCrearCategoriaProductoFrm()
        context['frmProductSub'] = clsCrearSubcategoriaProductoFrm()
        context['frmUdcProd'] = clsCrearUnidadCompraFrm()
        context['frmUdvProd'] = clsCrearUnidadVentaFrm()
        return context

#################################################################################################
# 6. GESTIONAR ORDENES DE COMPRA
#################################################################################################
''' 6.1 Vista para menu gestión ordenes de compra'''
class clsMenuGestionarOrdenesCompraViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_compras/gestionar_ordenes_compra.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Próximas entregas'
        context['create_url'] = reverse_lazy('compras:proximas_entregas')
        context['search_title'] = 'Entregas incumplidas'
        context['search_url'] = reverse_lazy('compras:entregas_incumplidas')
        return context

''' 6.2 Vista para próximas entregas'''
class clsProximasEntregasViw(ListView):
    # model = OrderPurchase
    template_name = 'modulo_compras/proximas_entregas.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in OrderPurchase.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

''' 6.3 Vista para entregas incumplidas'''
class clsEntregasIncumplidasViw(ListView):
    # model = EntregasIncumplidas
    template_name = 'modulo_compras/entregas_incumplidas.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in EntregasIncumplidas.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

#################################################################################################
# 7. CATALOGO DE PROVEEDORES
#################################################################################################
''' 7.1 Vista menú catálogo de proveedores'''
class clsMenuCatalogoProveedoresViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_compras/catalogo_proveedores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options_title'] = 'Opciones de catálogo'
        context['options_url'] = reverse_lazy('compras:opciones_proveedor')
        context['create_title'] = 'Crear proveedor'
        context['create_url'] = reverse_lazy('compras:crear_proveedor')
        context['search_title'] = 'Buscar proveedor'
        context['search_url'] = reverse_lazy('compras:listar_proveedores')
        return context

''' 7.2 Vista opciones proveedores'''
class clsOpcionesCatalogoProveedoresViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modulo_compras/opciones_catalogo_proveedores.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'slcBuscarProveedorjsn':
                jsnData = []
                strProveedor = request.POST['term'].strip()
                if len(strProveedor):
                    qrsCatalogoProveedores = clsCatalogoProveedoresMdl.objects.filter(Q(supplier_name__icontains=strProveedor) | Q(identification__icontains=strProveedor) | Q(contact_name__icontains=strProveedor))[0:10]
                for i in qrsCatalogoProveedores:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.supplier_name
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarProductojsn':
                jsnData = []
                strProducto = request.POST['term'].strip()
                if len(strProducto):
                    qrsCatalogoProductos = clsCatalogoProductosMdl.objects.filter(Q(product_desc__icontains=strProducto) | Q(id__icontains=strProducto))[0:10]
                for i in qrsCatalogoProductos:
                    dctJsn = i.toJSON()
                    dctJsn['value'] = i.product_desc
                    jsnData.append(dctJsn)
            elif action == 'tblCantidadesMinimasjsn':
                jsnData = []
                for i in clsCondicionMinimaCompraMdl.objects.all():
                    jsnData.append(i.toJSON())
                for i in range(0, len(jsnData)):
                    jsnData[i]['n'] = i + 1
            elif action == 'btnGuardarCondicionCantidadMinimajsn':
                with transaction.atomic():
                    intProveedorId = request.POST['proveedor']
                    jsnProductos = json.loads(request.POST['items'])
                    for i in jsnProductos:
                        clsCondicionMinimaCompraMdl.objects.create(
                            supplier_id = intProveedorId,
                            product_id = i['id'],
                            min_amount = i['cantidad']
                        )
            elif action == 'frmEditarCantidadMinimajsn':
                qrsCantidadMinimaProducto = clsCondicionMinimaCompraMdl.objects.get(pk=int(request.POST['id']))
                qrsCantidadMinimaProducto.min_amount = int(request.POST['cantidad'])
                qrsCantidadMinimaProducto.state = request.POST['estado']
                qrsCantidadMinimaProducto.save()
            elif action == 'tblCondicionDescuentojsn':
                jsnData = []
                for i in clsCondicionDescuentoProveedorMdl.objects.all():
                    jsnData.append(i.toJSON())
                for i in range(0, len(jsnData)):
                    jsnData[i]['n'] = i + 1
            elif action == 'frmGuardarCondicionDescuentojsn':
                with transaction.atomic():
                    intProveedorId = request.POST['proveedor']
                    jsnProductos = json.loads(request.POST['items'])
                    for i in jsnProductos:
                        clsCondicionDescuentoProveedorMdl.objects.create(
                            supplier_id = intProveedorId,
                            product_id = i['id'],
                            min_amount = i['cantidad'],
                            discount = i['descuento']
                        )
            elif action == 'frmEditarCondicionDescuentojsn':
                qrsCantidadMinimaProducto = clsCondicionDescuentoProveedorMdl.objects.get(pk=int(request.POST['id']))
                qrsCantidadMinimaProducto.min_amount = int(request.POST['cantidad'])
                qrsCantidadMinimaProducto.discount = float(request.POST['descuento'])
                qrsCantidadMinimaProducto.state = request.POST['estado']
                qrsCantidadMinimaProducto.save()
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

''' 7.3 Vista para exportar plantilla de proveedores'''
class clsExportarPlantillaProveedoresViw(APIView):

    def get(self, request):
        lstCeldasExcel = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1', 'M1', 'N1', 'O1', 'P1', 'Q1', 'R1']
        lstComentariosExcel = [
            'Digita NT si tu proveedor es persona Natural, si tu proveedor es persona Juridica digita JU (debes mantener las mayusculas)',
            'Según el tipo de identificación digita: CC para Cédula, NI para Nit, RU para Rut (debes mantener las mayusculas)',
            'Digita el número de identificación sin signos, en caso que sea NIT o RUT ingresa el digito de verificación al final sin espacios',
            'Ingresa el Nombre o razón social de tu proveedor de acuerdo a la identificación que ingresaste',
            'Ingresa el correo electronico de tu proveedor, es indispensable que lleve el formato con la @, en caso que no lo tengas deja este campo vacio',
            'Ingresa el nombre de la persona que recibe tus solicitudes',
            'Ingresa el número de celular o fijo de la persona que recibe tus solicitudes',
            'Digita el nombre de otra persona que tambien atienda tus solicitudes, sino aplica deja el espacio vacio',
            'Digita el numero de contacto de esta segunda persona que tambien atiende tus solicitudes, sino aplica deja el espacio vacio',
            'De acuerdo a ubicación de tu proveedor digita el numero del departamento que corresponda según la hoja de este archivo llamada "DEPARTAMENTOS", por ejemplo si es Bogotá digita 5',
            'De acuerdo al departamento que acabas de ingresar, digita el número que corresponda a la ciudad según la hoja de este archivo llamada "CIUDAD", por ejemplo si es Bogotá digita 167',
            'Ingresa la dirección de tu proveedor',
            'Ingresa solo en número el código postal de acuerdo a la ubicación de proveedor',
            'Si con tu proveedor tienes un acuerdo de un monto mínimo de compra por favor incluye el valor sin puntos, puedes incluir dos décimales',
            'Digita CD si tu proveedor te hace entrega de los productos en tu ubicación, SD si tu debes recogerlo en la ubicación de tu proveedor y MX si ambas son posibles (debes mantener las mayusculas)',
            'Si tu proveedor te da crédito digita CR, si pagas contraentrega o anticipado ingresa CO (ingresalo en mayusculas)',
            'Solo para el caso que ingresaste CR de crédito digita en número de días que tienes para el crédito, por ejemplo 30, si no tienes crédito deja este campo vacio',
            'Ingresa el monto de crédito que manejas con el proveedor, no incluyas puntos, si no tienes crédito deja este campo vacio',
        ]
        qrsDepartamentos = clsDepartamentosMdl.objects.all()
        srlDepartamentos = clsDepartamentosMdlSerializer(qrsDepartamentos, many=True)
        dtfDepartamentos = pd.DataFrame(srlDepartamentos.data)
        dtfDepartamentos = dtfDepartamentos.rename(columns={'id':'Código', 'department_name':'Departamento'})
        qrsCiudades = clsCiudadesMdl.objects.all()
        srlCiudades = clsCiudadesMdlSerializer(qrsCiudades, many=True)
        dtfCiudades = pd.DataFrame(srlCiudades.data)
        dtfCiudades = dtfCiudades.rename(columns={'id':'Código', 'city_name':'Ciudad'})
        dtfProveedores = pd.DataFrame(
            {
                'Tipo de persona':[],
                'Tipo de identificación':[],
                'Número de identificación':[],
                'Nombre proveedor':[],
                'Email':[],
                'Nombre contacto':[],
                'Celular contacto':[],
                'Nombre contacto 2':[],
                'Celular contacto 2':[],
                'Departamento':[],
                'Ciudad':[],
                'Dirección':[],
                'Código postal':[],
                'Valor mínimo de compra':[],
                'Condición de entrega':[],
                'Método de pago':[],
                'Días de crédito':[],
                'Cupo de crédito':[]
            }, 
            index = [i for i in range (0, 0)]
            )
        lstNombresColumnas = list(dtfProveedores.columns.values)
        lstTotalColumnas = [ i for i in range (1, len(lstNombresColumnas) + 1) ]
        lstTipoDato = [
            'Alfabético', 
            'Alfabético', 
            'Numérico', 
            'AlfaNumérico',
            'Alfabético', 
            'Alfabético', 
            'Numérico', 
            'Alfabético',
            'Numérico', 
            'Alfabético', 
            'Alfabético', 
            'AlfaNumérico',
            'Numérico', 
            'Decimal',
            'Alfabético',
            'Alfabético', 
            'Numérico', 
            'Decimal'
            ]
        lstLongitudMaxima = [
            2, 
            2, 
            10, 
            100,
            100, 
            100, 
            50, 
            100,
            50, 
            3, 
            3, 
            100,
            6, 
            30,
            2, 
            2, 
            3, 
            30
            ]
        lstCaracteresEspeciales = [
            'NO PERMITE', 
            'NO PERMITE', 
            'NO PERMITE', 
            'PERMITE Ñ',
            'PERMITE (@ .)', 
            'PERMITE Ñ', 
            'NO PERMITE', 
            'PERMITE Ñ',
            'NO PERMITE', 
            'NO PERMITE', 
            'NO PERMITE', 
            'NO PERMITE',
            'NO PERMITE', 
            'NO PERMITE',
            'NO PERMITE',
            'NO PERMITE', 
            'NO PERMITE', 
            'NO PERMITE'
            ]
        lstObservaciones = lstComentariosExcel
        lstCampoObligatorio = [
            'SI', 
            'SI', 
            'SI', 
            'SI',
            'SI', 
            'SI', 
            'SI', 
            'NO',
            'NO', 
            'SI', 
            'SI', 
            'SI',
            'SI', 
            'NO',
            'SI', 
            'SI', 
            'NO', 
            'NO'
            ]
        dtfInstructivoPlantilla = pd.DataFrame(
            {'Nº': lstTotalColumnas, 
            'NOMBRE CAMPO': lstNombresColumnas, 
            'TIPO DE DATO': lstTipoDato,
            'LONGITUD MAX': lstLongitudMaxima,
            'CARACTERES ESPECIALES': lstCaracteresEspeciales,
            'OBSERVACIONES': lstObservaciones,
            'OBLIGATORIO': lstCampoObligatorio,
            },
            index = [i for i in range (0, len(lstTipoDato))]
            )
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="catalogo_proveedores.xlsx"'
        with pd.ExcelWriter(response) as writer:
            dtfProveedores.to_excel(writer, sheet_name='PLANTILLA', index=False)
            dtfInstructivoPlantilla.to_excel(writer, sheet_name='INSTRUCTIVO', index=False)
            dtfDepartamentos.to_excel(writer, sheet_name='DEPARTAMENTOS', index=False)
            dtfCiudades.to_excel(writer, sheet_name='CIUDADES', index=False)
            fncAgregarAnchoColumna(writer, False, dtfProveedores, 'PLANTILLA')
            fncAgregarAnchoColumna(writer, True, dtfInstructivoPlantilla, 'INSTRUCTIVO')
            fncAgregarAnchoColumna(writer, True, dtfDepartamentos, 'DEPARTAMENTOS')
            fncAgregarAnchoColumna(writer, True, dtfCiudades, 'CIUDADES')
            fncAgregarComentarioCeldas(writer, 'PLANTILLA', lstCeldasExcel, lstComentariosExcel)
        return response

''' 7.4 Vista para importar archivo proveedores'''
class clsImportarCatalogoProveedoresViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_compras/importar_catalogo_proveedores.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lstNombresColumnas = [
            'Tipo de persona',
            'Tipo de identificación',
            'Número de identificación',
            'Nombre proveedor',
            'Email',
            'Nombre contacto',
            'Celular contacto',
            'Nombre contacto 2',
            'Celular contacto 2',
            'Departamento',
            'Ciudad',
            'Dirección',
            'Código postal',
            'Valor mínimo de compra',
            'Condición de entrega',
            'Método de pago',
            'Días de crédito',
            'Cupo de crédito',
            ]
        tplValidaciones = (
            ((False,), (True, 2), (True, 1), (False,), (True, ('NT', 'JU'))),
            ((False,), (True, 2), (True, 1), (False,), (True, ('CC', 'NI', 'RU'))),
            ((True, 'identification', clsCatalogoProveedoresMdl), (True, 10), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, 'mail'), (True, 100), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, int), (True, 50), (True, 1), (False,)),
            ((False,), (True, 100), (False,), (False,)),
            ((True, int), (True, 50), (False,), (False,)),
            ((False,), (True, 3), (True, 1), (True, clsDepartamentosMdl)),
            ((False,), (True, 3), (True, 1), (True, clsCiudadesMdl)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, int), (True, 6), (True, 1), (False,)),
            ((True, float), (True, 30), (False, ), (False,)),
            ((False,), (True, 2), (True, 1), (False,), (True, ('CD', 'SD', 'MX'))),
            ((False,), (True, 2), (True, 1), (False,), (True, ('CR', 'CO'))),
            ((True, int), (True, 3), (False, ), (False,)),
            ((True, float), (True, 30), (False, ), (False,))
            )
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCargarArchivojsn':
                filCatalogoProveedores = request.FILES['file']
                if str(filCatalogoProveedores).endswith('.xlsx'):
                    dtfProveedores = pd.read_excel(filCatalogoProveedores)
                    dtfProveedores = dtfProveedores.fillna(0)
                    lstValidarImportacion = [ fncValidarImportacionlst(dtfProveedores, i, j) for (i, j) in zip(lstNombresColumnas, tplValidaciones) ]
                    lstValidarImportacion = [ i for n in lstValidarImportacion for i in n ]
                    if len(lstValidarImportacion):
                        jsnProveedores = dtfProveedores.to_json(orient="split")
                        jsnData['jsnProveedores'] = jsnProveedores
                        jsnData['lstValidarImportacion'] = lstValidarImportacion
                        jsnData['strErrorArchivo'] = 'El archivo presenta errores ¿desea descargarlos?'
                        response = JsonResponse(jsnData, safe=False)
                    else:
                        with transaction.atomic():
                            for i in (dtfProveedores.values.tolist()):
                                clsCatalogoProveedoresMdl.objects.create(
                                person_type = i[0],
                                id_type = i[1],
                                identification = int(i[2]),
                                supplier_name = i[3],
                                email = i[4],
                                contact_name = i[5],
                                contact_cel = int(i[6]),
                                other_contact_name = i[7],
                                other_contact_cel = int(i[8]),
                                department_id = i[9],
                                city_id = i[10],
                                supplier_address = i[11],
                                postal_code = int(i[12]),
                                min_purchase_value = float(i[13]),
                                logistic_condition = i[14],
                                pay_method = i[15],
                                credit_days = int(i[16]),
                                credit_limit = float(i[17])
                                )
                        jsnData['success'] = '¡Se ha cargado el archivo a su base de datos con éxito!'
                        response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['error'] = 'Compruebe el formato del archivo'
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'btnArchivoErroresjsn':
                jsnProveedores = request.POST['jsnProveedores']
                dtfProveedores = pd.read_json(jsnProveedores, orient='split')
                lstValidarImportacion = json.loads(request.POST['lstValidarImportacion'])
                lstErroresCeldas = list( dict.fromkeys([ i[1] for i in lstValidarImportacion ]) )
                dtfProveedores = fncAgregarErroresDataframedtf(dtfProveedores, lstValidarImportacion, lstErroresCeldas)
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="catalogo_proveedores.xlsx"'
                with pd.ExcelWriter(response) as writer:
                    dtfProveedores.to_excel(writer, sheet_name='VALIDAR', index=False)
                    fncAgregarFormatoColumnasError(writer, lstValidarImportacion, 'VALIDAR', lstNombresColumnas)
                    fncAgregarAnchoColumna(writer, False, dtfProveedores, 'VALIDAR')
        except Exception as e:
            jsnData['error'] = str(e)
            response = JsonResponse(jsnData, safe=False)
        return response

''' 7.5 Vista para crear proveedor'''
class clsCrearProveedorViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = clsCatalogoProveedoresMdl
    form_class = clsCrearProveedorFrm
    template_name = 'modulo_compras/crear_proveedor.html'
    success_url = reverse_lazy("compras:listar_proveedores")
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCrearProveedorjsn':
                frmCrearProveedor = clsCrearProveedorFrm(request.POST)
                jsnData = frmCrearProveedor.save()
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
        context['title'] = 'Crear Proveedor'
        context['list_url'] = self.success_url
        context['action'] = 'frmCrearProveedorjsn'
        return context

''' 7.6 Vista para listar e inactivar proveedores'''
class clsListarCatalogoProveedoresViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = clsCatalogoProveedoresMdl
    template_name = 'modulo_compras/listar_proveedores.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'slcBuscarProveedoresjsn':
                jsnData = []
                strProveedor = request.POST['term'].strip()
                if len(strProveedor):
                    qrsCatalogoProveedores = clsCatalogoProveedoresMdl.objects.filter(Q(supplier_name__icontains=strProveedor) | Q(identification__icontains=strProveedor) | Q(contact_name__icontains=strProveedor))[0:10]
                for i in qrsCatalogoProveedores:
                    dctJsn = i.toJSON()
                    dctJsn['value'] = i.supplier_name
                    jsnData.append(dctJsn)
            elif action == 'btnEliminarProveedorjsn':
                qrsCatalogoProveedores = clsCatalogoProveedoresMdl.objects.get(pk=request.POST['id'])
                if qrsCatalogoProveedores.state == "AC":
                    qrsCatalogoProveedores.state = "IN"
                    qrsCatalogoProveedores.save()
                else:
                    qrsCatalogoProveedores.state = "AC"
                    qrsCatalogoProveedores.save()
                jsnData = qrsCatalogoProveedores.toJSON()
            else:
                jsnData['error'] = 'Ha ocurrido un error'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Listado de Proveedores'
        context['create_url'] = reverse_lazy('configuracion:crear_proveedor')
        context['list_url'] = reverse_lazy("configuracion:listar_proveedores")
        context['options_url'] = reverse_lazy('configuracion:opciones_proveedor')
        return context

''' 7.7 Vista para editar proveedor'''
class clsEditarProveedorViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = clsCatalogoProveedoresMdl
    form_class = clsCrearProveedorFrm
    template_name = 'modulo_compras/crear_proveedor.html'
    success_url = reverse_lazy("compras:listar_proveedores")
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmEditarProveedorjsn':
                frmEditarProveedor = self.get_form()
                jsnData = frmEditarProveedor.save()
            elif action == 'slcFiltrarCiudadesjsn':
                jsnData = [{'id': '', 'text': '------------'}]
                for i in clsCiudadesMdl.objects.filter(department_id=request.POST['id']):
                    jsnData.append({'id': i.id, 'text': i.city_name})
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Proveedor'
        context['list_url'] = self.success_url
        context['action'] = 'frmEditarProveedorjsn'
        return context

''' 7.8 Vista para exportar catálogo de proveedores'''
class clsExportarCatalogoProveedoresViw(APIView):

    def get(self, request):
        qrsCatalogoProveedores = clsCatalogoProveedoresMdl.objects.all()
        srlCatalogoProveedores = clsCatalogoProveedoresMdlSerializer(qrsCatalogoProveedores, many=True)
        dtfProveedores = pd.DataFrame(srlCatalogoProveedores.data)
        dtfProveedores = dtfProveedores.rename(columns={
            'id':'Código',
            'date_creation': 'Fecha de creación',
            'date_update': 'Fecha de actualización',
            'person_type_display':'Tipo de persona',
            'id_type_display': 'Tipo de identificación',
            'identification': 'Número de identificación',
            'supplier_name':'Nombre proveedor',
            'email': 'Email',
            'contact_name': 'Nombre contacto',
            'contact_cel': 'Celular contacto',
            'other_contact_name': 'Nombre contacto 2',
            'other_contact_cel': 'Celular contacto 2',
            'department': 'Departamento',
            'city': 'Ciudad',
            'supplier_address': 'Dirección',
            'postal_code': 'Código postal',
            'min_purchase_value': 'Valor mínimo de compra',
            'logistic_condition_display': 'Condición de entrega',
            'pay_method_display': 'Método de pago',
            'credit_days': 'Días de crédito',
            'credit_limit': 'Cupo de crédito',
            'state_display': 'Estado'
            })
        lstNombresColumnas = [
            'Código',
            'Fecha de creación',
            'Fecha de actualización',
            'Tipo de persona',
            'Tipo de identificación',
            'Número de identificación',
            'Nombre proveedor',
            'Email',
            'Nombre contacto',
            'Celular contacto',
            'Nombre contacto 2',
            'Celular contacto 2',
            'Departamento',
            'Ciudad',
            'Dirección',
            'Código postal',
            'Valor mínimo de compra',
            'Condición de entrega',
            'Método de pago',
            'Días de crédito',
            'Cupo de crédito',
            'Estado'
            ]
        dtfProveedores =dtfProveedores.reindex(columns=lstNombresColumnas)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="catalogo_proveedores.xlsx"'
        with pd.ExcelWriter(response) as writer:
            dtfProveedores.to_excel(writer, sheet_name='CATALOGO_PROVEEDORES', index=False)
            fncAgregarAnchoColumna(writer, True, dtfProveedores, 'CATALOGO_PROVEEDORES')
        return response
        
#################################################################################################
# 8. EVALUACIÓN DE PROVEEDORES
#################################################################################################
''' 8.1 Vista para menu evaluación de proveedores'''
class clsMenuEvaluacionProveedorViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_compras/evaluacion_proveedor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Crear evaluación proveedor'
        context['create_url'] = reverse_lazy('compras:crear_evaluacion_proveedor')
        context['search_title'] = 'Ver evaluaciones proveedores'
        context['search_url'] = reverse_lazy('compras:ver_evaluacion_proveedor')
        return context

''' 8.2 Vista para evaluación proveedores'''
class clsCrearEvaluacionProveedorViw(CreateView):
    # model = EvaluationSuppliers
    # form_class = EvaluationSuppliersForm
    template_name = 'modulo_compras/crear_evaluacion_proveedor.html'
    success_url = reverse_lazy("compras:ver_evaluacion_proveedor")
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear evaluación'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

''' 8.3 Vista para listado de proveedores'''
class clsVerEvaluacionProveedorViw(ListView):
    # model = EvaluationSuppliers
    template_name = 'modulo_compras/ver_evaluaciones_proveedor.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in clsCatalogoProveedoresMdl.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla evaluaciones proveedor'
        context['create_url'] = reverse_lazy("compras:crear_evaluacion_proveedor")
        return context

#################################################################################################
# 9. CARTERA DE PROVEEDORES
#################################################################################################
''' 9.1 Vista para la ventana cartera cliente '''
class clsCarteraProveedoresViw(ListView):
    # model = SupplierDebt
    template_name = 'modulo_compras/cartera_proveedores.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in SupplierDebt.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla cartera proveedores'
        return context