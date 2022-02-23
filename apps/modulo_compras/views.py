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
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, FormView, View
from django.urls import reverse_lazy

from apps.mixins import IsSuperuserMixin, ValidatePermissionRequiredMixin
from .forms import *
from .models import *
from apps.modulo_comercial.models import *
from apps.modulo_configuracion.models import *
from apps.modulo_configuracion.forms import *
from apps.modulo_comercial.forms import *

''' Vista para crear negociación con proveedor'''
class StartNegotiationView(CreateView):
    model = Orders
    form_class = OrderForm
    template_name = 'modulo_compras/iniciar_negociacion.html'
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
                    cust = ClientCatal.objects.filter(Q(id_number__icontains=term) | Q(customer__icontains=term) | Q(cel_number__icontains=term))[0:10]
                for i in cust:
                    item = i.toJSON()
                    item['value'] = i.customer
                    data.append(item)

            elif action == 'cartera_cliente':
                data = []
                cartera =  CustomerDebt.objects.filter(customer_id=request.POST['id'])
                for i in cartera:
                    item = i.toJSON()
                    data.append(item)

            elif action == 'search_products':
                data = []
                term = request.POST['term'].strip()
                ids_exclude = json.loads(request.POST['ids'])
                if len(term):
                    prods = clsCatalogoProductosMdl.objects.filter(Q(name__icontains=term) | Q(cod__icontains=term) | Q(pres__icontains=term))[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)

            elif action == 'compare_quantity':
                data = []
                prod_order = OrderPurchaseDetail.objects.filter(product_id=request.POST['id'])
                for i in prod_order:
                    item = i.toJSON()
                    data.append(item)
            
            elif action == 'lost_sales':
                lost_sale = request.POST
                lost_sale_bd = LostSales()
                lost_sale_bd.date = lost_sale['date']
                lost_sale_bd.customer_id = lost_sale['id_cust']
                lost_sale_bd.product_id = lost_sale['id_prod']
                lost_sale_bd.cant = lost_sale['cant']
                lost_sale_bd.save()
            
            elif action == 'add':
                with transaction.atomic():
                    sales = json.loads(request.POST['sales'])
                    orders = Orders()
                    orders.customer_id = sales['customer']
                    orders.order_date = sales['order_date']
                    orders.pay_method = sales['pay_method']
                    orders.deliver_date = sales['deliver_date']
                    orders.order_address = sales['order_address']
                    orders.obs = sales['observation']
                    orders.subtotal = float(sales['subtotal'])
                    orders.iva = float(sales['iva'])
                    orders.dcto = float(sales['dcto'])
                    orders.total = float(sales['total'])
                    orders.save()

                    for i in sales['products']:
                        order_prods = OrdersDetail()
                        order_prods.order_id = orders.id
                        order_prods.product_id = i['id']
                        order_prods.cant = int(i['cant'])
                        order_prods.sale_price = float(i['price_udv'])
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
        context['title'] = 'Crear pedido'
        context['document_title'] = 'Información del cliente'
        context['search_title'] = 'Agregar productos'
        context['transaction_title'] = 'Resumen pedido'
        context['action'] = 'add'
        return context

''' Vista para crear orden de compra'''
class PurchaseOrderView(CreateView):
    model = OrderPurchase
    form_class = OrderPurchaseForm
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
        context['list_url'] = reverse_lazy('comercial:listar_pedidos')
        context['action'] = 'add'
        return context

''' Vista para imprimir ordenes de compra'''

''' Vista para ver ordenes de compra'''

''' Vista para la ventana solicitar cotización'''
class SupplierQuoteView(CreateView):
    model = SupplierQuote
    form_class = SupplierQuoteForm
    template_name = 'modulo_compras/cotizacion_proveedor.html'
    success_url = reverse_lazy("home")

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
        context['list_url'] = reverse_lazy('comercial:listar_pedidos')
        context['action'] = 'add'
        return context
    
''' Vista para la ventana catálogo de productos'''
class CatProdView(TemplateView):
    template_name = 'modulo_compras/cat_prod.html'

''' Vista para crear producto'''
class ProductCreateView(CreateView):
    model = clsCatalogoProductosMdl
    form_class = clsCrearProductoFrm
    template_name = 'modulo_compras/crear_prod.html'
    success_url = reverse_lazy("compras:listar_productos")
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                frmProduct = clsCrearProductoFrm(request.POST)
                data = frmProduct.save()
            elif action == 'create_category':
                with transaction.atomic():
                    frmProductCat = clsCrearCategoriaProductoFrm(request.POST)
                    data = frmProductCat.save()
            elif action == 'create_subcategory':
                with transaction.atomic():
                    frmProductSub = clsCrearSubcategoriaProductoFrm(request.POST)
                    data = frmProductSub.save()
            elif action == 'create_udc':
                with transaction.atomic():
                    frmUdcProd = clsCrearUnidadCompraFrm(request.POST)
                    data = frmUdcProd.save()
            elif action == 'create_udv':
                with transaction.atomic():
                    frmUdvProd = clsCrearUnidadVentaFrm(request.POST)
                    data = frmUdvProd.save()
            elif action == 'product_dim_spe':
                with transaction.atomic():
                    data = request.POST
                    product = clsCatalogoProductosMdl()
                    product.bar_code = data['bar_code']
                    product.name = data['name']
                    product.pres = data['pres']
                    product.brand = data['brand']
                    product.category_id = data['category']
                    product.subcategory_id = data['subcategory']
                    product.udc_id = data['udc']
                    product.quantity_udc = data['quantity_udc']
                    product.price_udc = data['price_udc']
                    product.udv_id = data['udv']
                    product.quantity_udv = data['quantity_udv']
                    product.price_udv = data['price_udv']
                    product.iva = data['iva']
                    product.other_tax = data['other_tax']
                    product.del_time = data['del_time']
                    product.state = data['state']
                    product.save()
                    prod_dim = ProductDimensions()
                    prod_dim.product_id = product.id
                    prod_dim.weight_udc = data['weight_purch']
                    prod_dim.width_udc = data['width_purch']
                    prod_dim.high_udc = data['high_purch']
                    prod_dim.length_udc = data['length_purch']
                    if data.get("ori_purch") == None:
                        prod_dim.orientation_udc = False
                    else:
                        prod_dim.orientation_udc = data['ori_purch']
                    prod_dim.stacking_udc = data['apil_purch']
                    prod_dim.weight_udv = data['weight_sale']
                    prod_dim.width_udv = data['width_sale']
                    prod_dim.high_udv = data['high_sale']
                    prod_dim.length_udv = data['length_sale']    
                    if data.get("ori_sale") == None:
                        prod_dim.orientation_udv = False
                    else:
                        prod_dim.orientation_udv = data['ori_sale']
                    prod_dim.stacking_udv = data['apil_sale']
                    prod_dim.save()
                    prod_sto = ProductStorage()
                    prod_sto.product_id = product.id
                    prod_sto.cross_contamination_set = [i for i in data['cross_contam'] ]
                    prod_sto.restriction_temperature = data['const_temp']
                    prod_sto.save()
            elif action == 'product_dim':
                with transaction.atomic():
                    data = request.POST
                    product = clsCatalogoProductosMdl()
                    product.bar_code = data['bar_code']
                    product.name = data['name']
                    product.pres = data['pres']
                    product.brand = data['brand']
                    product.category_id = data['category']
                    product.subcategory_id = data['subcategory']
                    product.udc_id = data['udc']
                    product.quantity_udc = data['quantity_udc']
                    product.price_udc = data['price_udc']
                    product.udv_id = data['udv']
                    product.quantity_udv = data['quantity_udv']
                    product.price_udv = data['price_udv']
                    product.iva = data['iva']
                    product.other_tax = data['other_tax']
                    product.del_time = data['del_time']
                    product.state = data['state']
                    product.save()
                    prod_dim = ProductDimensions()
                    prod_dim.product_id = product.id
                    prod_dim.weight_udc = data['weight_purch']
                    prod_dim.width_udc = data['width_purch']
                    prod_dim.high_udc = data['high_purch']
                    prod_dim.length_udc = data['length_purch']
                    if data.get("ori_purch") == None:
                        prod_dim.orientation_udc = False
                    else:
                        prod_dim.orientation_udc = data['ori_purch']
                    prod_dim.stacking_udc = data['apil_purch']
                    prod_dim.weight_udv = data['weight_sale']
                    prod_dim.width_udv = data['width_sale']
                    prod_dim.high_udv = data['high_sale']
                    prod_dim.length_udv = data['length_sale']    
                    if data.get("ori_sale") == None:
                        prod_dim.orientation_udv = False
                    else:
                        prod_dim.orientation_udv = data['ori_sale']
                    prod_dim.stacking_udv = data['apil_sale']
                    prod_dim.save()
            elif action == 'product_spe':
                with transaction.atomic():
                    data = request.POST
                    product = clsCatalogoProductosMdl()
                    product.bar_code = data['bar_code']
                    product.name = data['name']
                    product.pres = data['pres']
                    product.brand = data['brand']
                    product.category_id = data['category']
                    product.subcategory_id = data['subcategory']
                    product.udc_id = data['udc']
                    product.quantity_udc = data['quantity_udc']
                    product.price_udc = data['price_udc']
                    product.udv_id = data['udv']
                    product.quantity_udv = data['quantity_udv']
                    product.price_udv = data['price_udv']
                    product.iva = data['iva']
                    product.other_tax = data['other_tax']
                    product.del_time = data['del_time']
                    product.state = data['state']
                    product.save()
                    prod_sto = ProductStorage()
                    prod_sto.product_id = product.id
                    prod_sto.cross_contamination_set = [i for i in data['cross_contam'] ]
                    prod_sto.restriction_temperature = data['const_temp']
                    prod_sto.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Producto'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['frmProductCat'] = clsCrearCategoriaProductoFrm()
        context['frmProductSub'] = clsCrearSubcategoriaProductoFrm()
        context['frmUdcProd'] = clsCrearUnidadCompraFrm()
        context['frmUdvProd'] = clsCrearUnidadVentaFrm()
        return context

''' Vista para cargar productos'''
class CatProdUploadView(TemplateView):
    template_name = 'modulo_compras/prod_upload.html'

''' Vista para listado de productos'''
class ProductListView(ListView):
    model = clsCatalogoProductosMdl
    template_name = 'modulo_compras/listar_productos.html'

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
        context['title_table'] = 'Tabla de Productos'
        context['create_url'] = reverse_lazy('compras:crear_producto')
        context['list_url'] = reverse_lazy("compras:listar_productos")
        return context

''' Vista para editar productos'''
class ActualizarProducto(TemplateView):
    template_name = 'modulo_compras/crear_producto.html'

class ListarCategoriaProd(TemplateView):
    template_name = "modulo_compras/ver_cat_prod.html"

class CrearCatProd(TemplateView):
    template_name = 'modulo_compras/crear_categoria_producto.html'

class ActualizarCatProd(TemplateView):
    template_name = 'modulo_compras/crear_categoria_producto.html'

class ListarSubcatProd(TemplateView):
    template_name = "modulo_compras/ver_subcat_prod.html"

class CrearSubcatProd(TemplateView):
    template_name = 'modulo_compras/crear_subcategoria_producto.html'

class ActualizarSubcatProd(TemplateView):
    template_name = 'modulo_compras/crear_subcategoria_producto.html'

class CrearUniCompra(TemplateView):
    template_name = 'modulo_compras/crear_unidad_compra.html'

class CrearUniVenta(TemplateView):
    template_name = 'modulo_compras/crear_unidad_venta.html'

class CrearCondCompra(TemplateView):
    template_name = 'modulo_compras/crear_condicion_compra.html'

class CrearCondAlm(TemplateView):
    template_name = 'modulo_compras/crear_condicion_almacenamiento.html'

''' Vista para próximas entregas'''
class UpcomingDeliveriesListView(ListView):
    model = OrderPurchase
    template_name = 'modulo_compras/listar_entregas.html'

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

''' Vista para entregas incumplidas'''
class UnfulfilledDeliveriesListView(ListView):
    model = EntregasIncumplidas
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

class OrdersNewsView(TemplateView):
    template_name = 'modulo_compras/novedades_ordenes_compra.html'

''' Vista para listado de actividades'''
class ActivityListView(ListView):
    # Crear bd para actividades
    model = clsCatalogoProductosMdl
    template_name = 'modulo_compras/actividades_compras.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Actividades de usuario'
        return context

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

''' Vista para la ventana catálogo de proveedores'''
class CatSupplierView(TemplateView):
    template_name = 'modulo_compras/prov_cat.html'

''' Vista para crear proveedor'''
class clsCrearProveedorViw(CreateView):
    model = clsCatalogoProveedoresMdl
    form_class = clsCrearProveedorFrm
    template_name = 'modulo_compras/crear_prov.html'
    success_url = reverse_lazy("compras:listar_proveedores")
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                frmsupplier = clsCrearProveedorFrm(request.POST)
                data = frmsupplier.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Proveedor'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

''' Vista para cargar proveedores'''
class CatSuppUploadView(TemplateView):
    template_name = 'modulo_compras/prov_upload.html'

''' Vista para listado de proveedores'''
class clsListarCatalogoProveedoresViw(ListView):
    model = clsCatalogoProveedoresMdl
    template_name = 'modulo_compras/listar_proveedores.html'

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
        context['title_table'] = 'Listado de Proveedores'
        context['create_url'] = reverse_lazy('compras:crear_proveedor')
        context['list_url'] = reverse_lazy("compras:listar_proveedores")
        return context
        
''' Vista para evaluación proveedores'''
class SupplierEvaluationView(CreateView):
    model = EvaluationSuppliers
    form_class = EvaluationSuppliersForm
    template_name = 'modulo_compras/evaluacion_proveedores.html'
    success_url = reverse_lazy("compras:listar_evaluaciones")
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
        context['title'] = 'Realizar evaluación'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

''' Vista para listado de proveedores'''
class SupplierEvalListView(ListView):
    model = EvaluationSuppliers
    template_name = 'modulo_compras/listar_evaluaciones.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in SupplierCatalog.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

''' Vista para la ventana cartera cliente '''
class CarteraSupView(ListView):
    model = SupplierDebt
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
        context['title_table'] = 'Tabla de cartera proveedores'
        return context

def historico_mov_compras(request):
    return render(request, 'modulo_compras/historico_mov_compras.html')

''' Vista para ventana de indicadores compras'''
class PurchaseIndicatorsView(TemplateView):
    template_name = 'modulo_compras/indicadores_compras.html'

