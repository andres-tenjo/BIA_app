# Python libraries
import json
import os
from datetime import timedelta, datetime, date
from pandas import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, PageBreak, Spacer, Table, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm 
from reportlab.lib import colors
                                                                                    
# Modelos BIA
from apps.Modelos.Several_func import *
from apps.Modelos.Update_Balances import *
from apps.Modelos.Parameters import *

# Django libraries
from django.conf import settings
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
from django.template.loader import get_template
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, FormView, View
from django.urls import reverse_lazy
#from weasyprint import HTML, CSS

# BIA files
from apps.mixins import ValidatePermissionRequiredMixin
from .forms import *
from .models import *
from apps.modulo_configuracion.models import *
from apps.planeacion.models import *
from apps.modulo_compras.models import *
from apps.modulo_almacen.models import *
from apps.modulo_configuracion.forms import *
from apps.functions_views import *
from apps.modulo_configuracion.api.serializers import *

# Django-rest libraries
from rest_framework.views import APIView

################################################################################################
################################## VISTAS DEL MODULO COMERCIAL #################################
################################################################################################

#################################################################################################
# 1. PROMOCIONES
#################################################################################################
''' 1.1 Vista para ver promociones'''
class clsVerPromocionesViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = clsPromocionesMdl
    template_name = 'modulo_comercial/ver_promociones.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in clsPromocionesMdl.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in clsPromocionesMdl.objects.filter(prom_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla de promociones vigentes'
        return context

#################################################################################################
# 2. PEDIDOS
#################################################################################################
''' 2.1 Vista para menu pedidos'''
class clsMenuPedidosViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_comercial/pedidos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Crear pedido'
        context['create_url'] = reverse_lazy('comercial:crear_pedido')
        context['search_title'] = 'Ver pedido'
        context['search_url'] = reverse_lazy('comercial:ver_pedidos')
        return context

''' 2.2 Vista para crear pedido'''
class clsCrearPedidoViw(CreateView):
    model = clsPedidosMdl
    form_class = clsPedidosFrm
    template_name = 'modulo_comercial/crear_pedido.html'
    success_url = reverse_lazy('comercial:ver_pedidos')

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
            msg = f'El cliente presenta una mora de $ {min_pay} con pago inmediato'
            l = [state, credit_value, min_pay, total_pay, msg]
        elif cartera[cartera['state'] == 'Vencida'].empty == False:
            state = 'Vencida'
            min_pay = float(cartera[cartera['state'] == 'Vencida']['balance_payment'].sum())
            total_pay = float(cartera[cartera['state'] == 'Vencida']['balance_payment'].sum())
            msg = f'El cliente presenta una mora de $ {min_pay} con pago inmediato'
            l = [state, credit_value, min_pay, total_pay, msg]
        elif cartera[cartera['state'] == 'Activa'].empty == False:
            state = 'Activa'
            min_pay = 0
            total_pay = float(cartera[cartera['state'] == 'Activa']['balance_payment'].sum())
            msg = f'El cliente tiene un cupo disponible de $ {credit_value} para compra de crédito'
            l = [state, credit_value, min_pay, total_pay, msg]
        return l

    def post(self,request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_customer':
                data = []
                term = request.POST['term'].strip()
                if len(term):
                    cust = clsCatalogoClientesMdl.objects.filter(
                        Q(identification__icontains=term) | 
                        Q(business_name__icontains=term) | 
                        Q(cel_number__icontains=term))[0:10]
                for i in cust:
                    item = i.toJSON()
                    item['value'] = i.business_name
                    data.append(item)
            elif action == 'create_customer':
                with transaction.atomic():
                    frmCustomer = clsCrearClienteFrm(request.POST)
                    data = frmCustomer.save()
            elif action == 'cartera_cliente':
                data = {}
                cartera =  CustomerDebt.objects.filter(customer_id=request.POST['id'])
                credit_value = request.POST['credit_value']
                self.upd_cart_sta(cartera)
                if cartera:
                    bd = cartera.exclude(state="CE")
                    if bd:
                        cart = self.cartera(bd, credit_value)
                        data['cartera'] = cart
                else:
                    state = 'Activa'
                    msg = f'El cliente tiene un cupo disponible de $ {credit_value} para compra de crédito'
                    data['msg'] = msg
                    data['credit_value'] = credit_value
                    data['state'] = state
            elif action == 'search_products':
                data = []
                term = request.POST['term'].strip()
                ids_exclude = json.loads(request.POST['ids'])
                if len(term):
                    prods = clsCatalogoProductosMdl.objects.filter(Q(product_desc__icontains=term) | Q(id__icontains=term))[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.product_desc
                    data.append(item)
            elif action == 'compare_quantity':
                data = {}
                orders = [ i.toJSON() for i in OrderPurchaseDetail.objects.filter(product_id=request.POST['id']) ]
                if orders:
                    data['prod_order'] = orders
                else:
                    date_today = date.today()
                    del_days = date_today + timedelta(days=4)
                    data['del_days'] = del_days.strftime("%Y-%m-%d")
            elif action == 'helper_table':
                data = {}
                catalogo = clsCatalogoProductosMdl.objects.all()
                catalogo = catalogo.to_dataframe()
                pedidos = clsDetallePedidosMdl.objects.filter(state='CU')
                cust_base = pedidos.filter(customer_id=request.POST['id_cust'])
                cust_base = cust_base.to_dataframe()
                cat_base = pedidos.filter(city=request.POST['city'], category_cust=request.POST['category_cust'])
                cat_base = cat_base.to_dataframe()
                gen_base = pedidos.to_dataframe()
                added = json.loads(request.POST['ids'])

                def unique_order(df):
                    item_count= df.drop(columns= ['Unnamed: 0', 'order', 'Fecha', 'Estado movto.', 'Bodega',
                                                    'Cant. pedida', 'Cant. pendiente', 'Cant. comprom.', 'Cant. remision',
                                                    'Cant. factura', 'Razón social cliente factura',
                                                    'Desc. ciudad', 'Nombre vendedor cliente', 'DIVISION', 'Fecha entrega',
                                                    'Precio unit.', 'Mes', 'Valor total', 'Semana'])
                    item_probability= item_count.assign(Prob= 100)
                    return item_probability

                def prob_new_bases(df1, df2, var, filt):
                    if filt== 'subcategory':
                        df1= df1.merge(df2, on= 'product', how= 'left')\
                            .drop(columns= ['Fecha creación', 'Referencia', 'Ubicación', 'Desc. item_y', 'LINEA',  
                                            'Compra', 'Venta', 'Cant. disponible', 'Ultimo costo uni.', 'IVA',     
                                            'Costo prom. uni.', 'Código barra principal', 'Fecha última compra',   
                                            'Fecha última venta', 'TIPO DE PRODUCTO', 'category'])
                    else:
                        df1= df1.merge(df2, on= 'product', how= 'left')\
                            .drop(columns= ['Fecha creación', 'Referencia', 'Ubicación', 'Desc. item_y', 'LINEA',  
                                            'Compra', 'Venta', 'Cant. disponible', 'Ultimo costo uni.', 'IVA',     
                                            'Costo prom. uni.', 'Código barra principal', 'Fecha última compra',   
                                            'Fecha última venta', 'TIPO DE PRODUCTO', 'subcategory'])
                    df1.rename(columns= {'Desc. item_x': 'Desc. item'}, inplace= True)
                    new_a= df1[df1[filt]== var]
                    return calculated_probability(new_a, new_a)

                def calculated_probability(df1, df2):    
                    item_count= df1.groupby(['product', 'Desc. item'])['order'].count().reset_index()\
                        .sort_values(by= 'order', ascending= False)
                    item_probability= item_count.assign(Prob= item_count['order']/ df2['order']\
                        .nunique()* 100)
                    item_probability.drop(columns= ['order'], inplace= True)
                    return item_probability

                def prob_per_item(df1, df2, l):
                    base_item_probability= None
                    complete_orders= [df2[df2['order']== i] for i in df1['order']]
                    if len(complete_orders)== 1:        
                        complete_orders= complete_orders[0]
                        item_probability= unique_order(complete_orders)
                    elif len(complete_orders)> 1:
                        complete_orders= pd.concat(complete_orders)
                        item_probability= calculated_probability(complete_orders, df1)
                    return item_probability

                def two_bases_concatenated(df1, df2, l):
                    item_probability= pd.concat([df1, df2])
                    item_probability.drop_duplicates(subset= 'product', keep= 'first', inplace= True)
                    item_probability= [item_probability[item_probability['product']== i] for i in \
                        item_probability['product'] if i not in l]
                    return item_probability

                def prob_list(l):
                    var= None
                    if len(l)== 1:
                        var= l[0]
                    elif len(l)> 1:
                        var= pd.concat(l)
                        var.sort_values(by= 'Prob', ascending= False, inplace= True)
                    return var

                def actualized_bases(df, l):
                    orders_numbers= df[df['product']== l[0]]
                    filter_recursion= [df[df['order']== i] for i in orders_numbers['order']]
                    if len(filter_recursion)== 1:
                        filter_recursion= filter_recursion[0]
                    elif len(filter_recursion)> 1:
                        filter_recursion= pd.concat(filter_recursion)
                    return filter_recursion

                def filter_results(df1, df2):
                    new_a= [df1[df1['product']== i] for i in df1['product'] if i not in df2]
                    return prob_list(new_a)

                def new_bases(l1, df, l2, added):
                    new_a= None
                    n= 0
                    var= df[df['product']== l1[0]]    
                    var= var.iloc[0]['subcategory']
                    if var== '':
                        var= df[df['product']== l1[0]]
                        var= var['category']
                        if var== '':
                            new_a= calculated_probability(l2[2], l2[2])
                            return filter_results(new_a, added)
                        else:
                            filt= 'category'
                            new_a= prob_new_bases(l2[0], df, var, filt)
                            new_a= filter_results(new_a, added)
                            if new_a is not None:
                                return new_a
                            else:
                                n+= 1
                                return new_bases(l1, df, l2[n: ], added)
                    else:
                        filt= 'subcategory'
                        new_a= prob_new_bases(l2[0], df, var, filt)
                        new_a= filter_results(new_a, added)
                        if new_a is not None:
                            return new_a
                        else:
                            n+= 1
                            return new_bases(l1, df, l2[n: ], added)    
                    
                def validated_bases(l1, l2, df, memo= None):
                    memo= memo
                    item_probability= None
                    n= 0
                    if len(l1)== 1:
                        if len(l1[0])!= 0:
                            orders_numbers= l1[0][l1[0]['product']== l2[0]]
                            if len(orders_numbers['order'])>= 1:
                                item_probability= prob_per_item(orders_numbers, l1[0], added)
                                item_probability= pd.concat([item_probability, memo])
                                item_probability.drop_duplicates(subset= 'product', keep= 'first', inplace= True)
                                if df is not None:
                                    item_probability= two_bases_concatenated(item_probability, df, added)
                                    item_probability= prob_list(item_probability)
                            else:
                                item_probability= two_bases_concatenated(df, memo, added)
                                item_probability= prob_list(item_probability)
                        else:
                            if df is not None:
                                if memo is not None:
                                    item_probability= two_bases_concatenated(df, memo, added)
                                    item_probability= prob_list(item_probability)
                                else:
                                    item_probability= df
                        return item_probability
                    elif len(l1)> 1:
                        n-= 1
                        base_orders_numbers= l1[1][l1[1]['product']== l2[0]]
                        if len(base_orders_numbers['order'])>= 1:
                            memo= prob_per_item(base_orders_numbers, l1[1], added)            
                        return validated_bases(l1[: n], l2, df, memo)

                def helper(rec_added, recursion, added, cust_base, cat_base, gen_base, memo= None):    
                    added= added
                    cust_base= cust_base
                    cat_base= cat_base
                    gen_base= gen_base
                    memo= memo
                    item_probability, filter_recursion= None, None
                    n= 0
                    if len(rec_added)== 1:
                        item_probability= validated_bases([recursion, cust_base], rec_added, memo)
                        if item_probability is not None:
                            item_probability= filter_results(item_probability, added)
                            if item_probability is not None:
                                return item_probability
                            else:
                                new_a= new_bases(rec_added, catalogo, [cust_base, cat_base, gen_base], added)
                                return filter_results(new_a, added)
                        else:
                            item_probability= new_bases(rec_added, catalogo, [cust_base, cat_base, gen_base], added)
                            return item_probability
                    else:
                        n+= 1
                        if len(recursion)== 0:
                            filter_recursion= actualized_bases(cust_base, rec_added)
                        else:
                            filter_recursion= actualized_bases(recursion, rec_added)
                        memo= validated_bases([recursion, cust_base], rec_added, memo)
                        return helper(rec_added[n: ], filter_recursion, added, cust_base, cat_base, gen_base, memo)
                
                x= helper(added, cust_base, added, cust_base, cat_base, gen_base)

            elif action == 'lost_sales':
                lost_sale = request.POST
                lost_sale_bd = clsVentasPerdidasMdl()
                lost_sale_bd.date = lost_sale['date']
                lost_sale_bd.customer_id = lost_sale['id_cust']
                lost_sale_bd.product_id = lost_sale['id_prod']
                lost_sale_bd.cant = lost_sale['cant']
                lost_sale_bd.save()
            elif action == 'add':
                with transaction.atomic():
                    sales = json.loads(request.POST['sales'])
                    orders = clsPedidosMdl()
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
                    if orders.pay_method == 'CR':
                        cartera = CustomerDebt()
                        cartera.customer_id = sales['customer']
                        cartera.order_id = orders.id
                        cartera.order_value = float(sales['total'])
                        
                        # Vairables para cartera
                        cartera.term = float(sales['total'])
                        cartera.next_payment_date = float(sales['total'])
                        cartera.next_payment_value = float(sales['total'])
                        cartera.balance_payment = float(sales['total'])
                        cartera.credit_value = float(sales['total'])
                        cartera.balance_credit_value = float(sales['total'])

                    for i in sales['products']:
                        order_prods = clsDetallePedidosMdl()
                        order_prods.order_id = orders.id
                        order_prods.customer_id = sales['customer']
                        order_prods.category_cust = sales['category_cust']
                        order_prods.city = sales['order_city']
                        order_prods.product_id = i['id']
                        order_prods.cant = int(i['cant'])
                        order_prods.sale_price = float(i['price_udv'])
                        order_prods.subtotal = float(i['subtotal'])
                        order_prods.iva = float(i['iva'])
                        order_prods.dcto = float(i['desc'])
                        order_prods.total = float(i['total'])
                        order_prods.save()
                    data = {'id': orders.id}
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frmCust'] = clsCrearClienteFrm()
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

''' 2.3 Vista para ver pedido'''
class clsVerPedidosViw(ListView):
    model = clsPedidosMdl
    template_name = 'modulo_comercial/ver_pedidos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in clsPedidosMdl.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in clsDetallePedidosMdl.objects.filter(order_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla de pedidos'
        return context

''' 2.4 Vista para imprimir pedido pdf'''
class clsImprimirPedidoPdfViw(View):

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('modulo_comercial/invoice.html')
            context = {
                'sale': clsPedidosMdl.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'CONVERGENCIA SOLUCIONES S.A.S', 'NIT': '900817889-2', 'address': 'Calle 158 # 96a 25'},
                'icon': '{}{}'.format(settings.STATIC_URL, 'img/home/logo.png')
            }
            print(context)
            html = template.render(context)
            css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.5.3-dist/css/bootstrap.min.css')
            print(css_url)
            pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
            return HttpResponse(pdf, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('comercial:ver_pedidos'))

''' 2.5 Vista para exportar pedido excel'''


#################################################################################################
# 3. COTIZACIONES
#################################################################################################
''' 3.1 Vista para menu cotizaciones'''
class clsMenuCotizacionesViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_comercial/cotizaciones.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Crear cotización'
        context['create_url'] = reverse_lazy('comercial:crear_cotizacion')
        context['search_title'] = 'Ver cotización'
        context['search_url'] = reverse_lazy('comercial:ver_cotizaciones')
        return context

''' 3.2 Vista para crear cotización'''
class clsCrearCotizacionViw(CreateView):
    model = Quotes
    form_class = QuoteForm
    template_name = 'modulo_comercial/crear_cotizacion.html'
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
                    cust = clsCatalogoClientesMdl.objects.filter(
                        Q(identification__icontains=term) | 
                        Q(business_name__icontains=term) | 
                        Q(cel_number__icontains=term))[0:10]
                for i in cust:
                    item = i.toJSON()
                    item['value'] = i.business_name
                    data.append(item)
            elif action == 'create_customer':
                with transaction.atomic():
                    frmCustomer = clsCrearClienteFrm(request.POST)
                    data = frmCustomer.save()
            elif action == 'search_products':
                data = []
                term = request.POST['term'].strip()
                ids_exclude = json.loads(request.POST['ids'])
                
                if len(term):
                    prods = clsCatalogoProductosMdl.objects.filter(Q(product_desc__icontains=term) | Q(id__icontains=term))[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.product_desc
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    sales = json.loads(request.POST['sales'])
                    quotes = Quotes()
                    quotes.doc = sales['doc']
                    quotes.customer_id = sales['customer']
                    quotes.order_date = sales['order_date']
                    quotes.deliver_date = sales['deliver_date']
                    quotes.subtotal = float(sales['subtotal'])
                    quotes.iva = float(sales['iva'])
                    quotes.dcto = float(sales['dcto'])
                    quotes.total = float(sales['total'])
                    quotes.save()
                    for i in sales['products']:
                        quotes_prods = QuotesDetail()
                        quotes_prods.order_id = quotes.id
                        quotes_prods.product_id = i['id']
                        quotes_prods.cant = int(i['cant'])
                        quotes_prods.sale_price = float(i['unit_price'])
                        quotes_prods.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy('comercial:ver_cotizaciones')
        context['frmCust'] = clsCrearClienteFrm()
        context['action'] = 'add'
        return context

''' 3.3 Vista para ver cotizaciones'''
class clsVerCotizacionesViw(ListView):
    model = Quotes
    template_name = 'modulo_comercial/ver_cotizaciones.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Quotes.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in QuotesDetail.objects.filter(order_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla de cotizaciones'
        return context

#################################################################################################
# 4. CATÁLOGO PRODUCTOS
#################################################################################################
''' 4.1 Vista para ver productos'''
class clsVerCatalogoProductosViw(LoginRequiredMixin, ListView):
    model = clsCatalogoProductosMdl
    template_name = 'modulo_comercial/ver_productos.html'

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
# 5. AGENDA DE LLAMADAS
#################################################################################################
''' 5.1 Vista para menu llamadas'''
class clsMenuLlamadasViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_comercial/llamadas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Agendar llamada'
        context['create_url'] = reverse_lazy('comercial:crear_llamada')
        context['search_title'] = 'Ver agenda de llamadas'
        context['search_url'] = reverse_lazy('comercial:ver_agenda_llamadas')
        return context

''' 5.2 Vista para crear llamada'''
class clsCrearLlamadaView(CreateView):
    model = ScheduleCall
    form_class = ScheduleCallForm
    template_name = 'modulo_comercial/crear_llamada.html'
    success_url = reverse_lazy('comercial:ver_agenda_llamadas')
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
        context['title'] = 'Agendar llamada'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

''' 5.3 Vista para ver llamadas'''
class clsVerAgendaLlamadasViw(ListView):
    model = ScheduleCall
    template_name = 'modulo_comercial/ver_agenda_llamadas.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

#################################################################################################
# 6. CATÁLOGO DE CLIENTES
#################################################################################################
''' 6.1 Vista para menu catálogo de clientes'''
class clsMenuCatalogoClientesViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_comercial/catalogo_clientes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options_title'] = 'Opciones de catálogo'
        context['options_url'] = reverse_lazy('comercial:opciones_cliente')
        context['create_title'] = 'Crear cliente'
        context['create_url'] = reverse_lazy('comercial:crear_cliente')
        context['search_title'] = 'Buscar cliente'
        context['search_url'] = reverse_lazy('comercial:listar_clientes')
        return context

''' 6.2 Vista para opciones cliente'''
class clsOpcionesCatalogoClientesViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modulo_comercial/opciones_catalogo_clientes.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCrearCategoriaClientejsn':
                with transaction.atomic():
                    strCategoriaCliente = request.POST['customer_cat']
                    jsnMargenCategoriaCliente = json.loads(request.POST['margin_cat'])
                    qrsCrearCategoriaCliente = clsCategoriaClienteMdl.objects.create(
                        customer_cat = strCategoriaCliente
                    )
                    for i in jsnMargenCategoriaCliente:
                        for j in i:
                            clsMargenCategoriaClienteMdl.objects.create(
                                customer_cat_id = qrsCrearCategoriaCliente.id,
                                product_cat_id = j['id'],
                                margin_min = float(j['margin_min']),
                                margin_max = float(j['margin_max'])
                            )
                    jsnData = qrsCrearCategoriaCliente.toJSON()
            elif action == 'frmEditarCategoriaClientejsn':
                with transaction.atomic():    
                    strCategoriaCliente = request.POST['customer_cat']
                    jsnMargenCategoriaCliente = json.loads(request.POST['margin_cat'])[0]
                    qrsEditarCategoriaCliente = clsCategoriaClienteMdl.objects.get(
                        pk = request.POST['id']
                        )
                    qrsEditarCategoriaCliente.customer_cat = strCategoriaCliente
                    qrsEditarCategoriaCliente.save()
                    qrsEditarMargenCategoriaCliente = clsMargenCategoriaClienteMdl.objects.filter(
                            customer_cat_id = qrsEditarCategoriaCliente.id
                            )
                    for i in jsnMargenCategoriaCliente:
                        qrsMargenCategoriaCliente = qrsEditarMargenCategoriaCliente.get(pk=i['id'])
                        qrsMargenCategoriaCliente.margin_min = float(i['margin_min'])
                        qrsMargenCategoriaCliente.margin_max = float(i['margin_max'])
                        qrsMargenCategoriaCliente.save()
            elif action == 'btnEliminarCategoriaClientejsn':
                qrsCategoriaCliente = clsCategoriaClienteMdl.objects.get(pk=request.POST['id'])
                if qrsCategoriaCliente.state == "AC":
                    qrsCategoriaCliente.state = "IN"
                    qrsCategoriaCliente.save()
                else:
                    qrsCategoriaCliente.state = "AC"
                    qrsCategoriaCliente.save()
            elif action == 'tblMargenCategoriaProducto':
                jsnData = {}
                qrsCategoriaProducto =clsCategoriaProductoMdl.objects.filter(state='AC')
                if len(qrsCategoriaProducto):
                    jsnData = []
                    for i in qrsCategoriaProducto:
                        dctJsn = i.toJSON()
                        dctJsn['margin_max'] = 0.00
                        dctJsn['margin_min'] = 0.00
                        jsnData.append(dctJsn)
                else:
                    jsnData['error'] = 'No existe(n) catergoría(s) de producto(s) creada(s), desea crear una?'    
            elif action == 'btnEditarMargenCategoriaClientejsn':
                jsnData = []
                qrsMargenCategoriaCliente =clsMargenCategoriaClienteMdl.objects.filter(
                    customer_cat = request.POST['id']
                )
                for i in qrsMargenCategoriaCliente:
                    dctJsn = i.toJSON()
                    dctJsn['product_cat'] = i.product_cat.product_cat
                    jsnData.append(dctJsn)
            elif action == 'tblCategoriaClientejsn':
                jsnData = []
                for i in clsCategoriaClienteMdl.objects.all():
                    jsnData.append(i.toJSON())
                for i in range(0, len(jsnData)):
                    jsnData[i]['n'] = i + 1
            elif action == 'tblZonaClientejsn':
                jsnData = []
                for i in clsZonaClienteMdl.objects.all():
                    jsnData.append(i.toJSON())
                for i in range(0, len(jsnData)):
                    jsnData[i]['n'] = i + 1
            elif action == 'slcBuscarZonaActivajsn':
                jsnData = []
                qrsZonaCliente = clsZonaClienteMdl.objects.filter(state='AC')
                for i in qrsZonaCliente:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.customer_zone
                    jsnData.append(dctJsn)
            elif action == 'frmCrearZonaClientejsn':
                with transaction.atomic():
                    frmCrearZonaCliente = clsCrearZonaClienteFrm(request.POST)
                    jsnData = frmCrearZonaCliente.save()
            elif action == 'frmEditarZonaClientejsn':
                qrsZonaCliente = clsZonaClienteMdl.objects.get(pk=int(request.POST['id']))
                qrsZonaCliente.customer_zone = request.POST['customer_zone']
                qrsZonaCliente.save()
            elif action == 'btnEliminarZonaCliente':
                qrsZonaCliente = clsZonaClienteMdl.objects.get(pk=request.POST['id'])
                if qrsZonaCliente.state == "AC":
                    qrsZonaCliente.state = "IN"
                    qrsZonaCliente.save()
                else:
                    qrsZonaCliente.state = "AC"
                    qrsZonaCliente.save()
            elif action == 'btnAbrirFormularioAsesorComercialjsn':
                jsnData = {}
                qrsUsuarios = User.objects.filter(is_superuser=False)
                qrsZonaCliente = clsZonaClienteMdl.objects.filter(state='AC')
                if not len(qrsUsuarios):
                    jsnData['error_user'] = 'No existe(n) usuario(s) creado(s), desea crear uno?'
                elif not len(qrsZonaCliente):
                    jsnData['error_zone'] = 'No existe(n) zona(s) de cliente(s) creada(s), desea crear una?'
            elif action == 'frmCrearAsesorComercialjsn':
                with transaction.atomic():
                    frmCrearAsesor = clsCrearAsesorComercialFrm(request.POST)
                    jsnData = frmCrearAsesor.save()
            elif action == 'frmEditarAsesorComercialjsn':
                qrsAsesorComercial = clsAsesorComercialMdl.objects.get(pk = request.POST['id'])
                frmCrearAsesorComercial = clsCrearAsesorComercialFrm(request.POST, instance=qrsAsesorComercial)
                jsnData = frmCrearAsesorComercial.save()
            elif action == 'slcBuscarAsesorComercialjsn':
                jsnData = []
                for i in clsAsesorComercialMdl.objects.all():
                    jsnData.append(i.toJSON())
                for i in range(0, len(jsnData)):
                    jsnData[i]['n'] = i + 1
            elif action == 'btnEliminarAsesorComercialjsn':
                qrsAsesorComercial = clsAsesorComercialMdl.objects.get(pk=request.POST['id'])
                if qrsAsesorComercial.state == "AC":
                    qrsAsesorComercial.state = "IN"
                    qrsAsesorComercial.save()
                else:
                    qrsAsesorComercial.state = "AC"
                    qrsAsesorComercial.save()
            elif action == 'btnExportarCatalogoClientes':
                qrsCategoriaCliente =  clsCategoriaClienteMdl.objects.filter(state='AC')
                if not qrsCategoriaCliente:
                    strMensaje = 'Para cargar archivo de clientes, debe crear categorías de clientes'
                    jsnData['msg'] = strMensaje
                qrsZonaCliente = clsZonaClienteMdl.objects.filter(state='AC')
                if not qrsZonaCliente:
                    strMensaje = 'Para cargar archivo de clientes, debe crear zonas de clientes'
                    jsnData['msg'] = strMensaje
                qrsAsesorComercial = clsAsesorComercialMdl.objects.filter(state='AC')
                if not qrsAsesorComercial:
                    strMensaje = 'Para cargar archivo de clientes, debe crear asesores comerciales'
                    jsnData['msg'] = strMensaje
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('comercial:crear_cliente')
        context['list_url'] = reverse_lazy("comercial:listar_clientes")
        context['frmZone'] = clsCrearZonaClienteFrm()
        context['frmAdvisor'] = clsCrearAsesorComercialFrm()
        return context

''' 6.3 Vista para exportar plantilla clientes'''
class clsExportarPlantillaClientesViw(APIView):

    def get(self, request):
        lstCeldasExcel = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1', 'M1', 'N1', 'O1', 'P1', 'Q1', 'R1']
        lstComentariosExcel = [
            'Digita NT si tu cliente es persona Natural, si tu cliente es persona Juridica digita JU (debes mantener las mayusculas)',
            'Según el tipo de identificación digita: CC para Cédula, NI para Nit, RU para Rut (debes mantener las mayusculas)',
            'Digita el número de identificación sin signos, en caso que sea NIT o RUT ingresa el digito de verificación al final sin espacios',
            'Ingresa el Nombre o razón social de tu cliente de acuerdo a la identificación que ingresaste',
            'Ingresa el nombre de la persona con quien tienes contacto directo',
            'Ingresa el número de celular o fijo de la persona con quien tienes contacto directo',
            'Ingresa el correo electronico de tu cliente, es indispensable que lleve el formato con la @, en caso que no lo tengas deja este campo vacio',
            'De acuerdo a ubicación de tu cliente digita el número del departamento que corresponda según la hoja de este archivo llamada "DEPARTAMENTOS", por ejemplo si es Bogotá digita 5',
            'De acuerdo al departamento que acabas de ingresar, digita el número que corresponda a la ciudad según la hoja de este archivo llamada "CIUDAD", por ejemplo si es Bogotá digita 167',
            'Como ya creaste las zonas antes de descargar esta plantilla, en este archivo se encuentra la hoja con el nombre "ZONAS", ahí puedes validar a que número de zona corresponde tu cliente y solo ingresas ese número (es el numero en la primer columna). Por ejemplo si la zona es norte y el numero que aparece al inicio es 1, digitas 1 en este campo',
            'Ingresa la dirección de tu cliente',
            'Para asignar un rango de horario de entrega a tu cliente por favor ingresa la hora de inicio Ej. 12:54 pm',
            'Para cerrar el rango de horario de entrega a tu cliente por favor ingresa la hora fin Ej. 3:54 pm',
            'Como ya creaste las categorias antes de descargar esta plantilla, en este archivo se encuentra la hoja con el nombre "CATEGORIA", ahí puedes validar a que número de categoría corresponde y solo ingresas ese número (es el numero en la primer columna). Por ejemplo la categoría se llama Mayoristas y el numero que aparece al inicio es 1, digitas 1 en este campo',
            'Como ya creaste las asesores comerciales antes de descargar esta plantilla, en este archivo se encuentra la hoja con el nombre "ASESOR", para asignar un asesor comercial a tu cliente podrás validar a que número corresponde y solo ingresas ese número (es el número en la primer columna)',
            'Si con tu cliente manejas crédito digita CR, si el te paga contraentrega o anticipado ingresa CO (ingresalo en mayusculas)',
            'Solo para el caso que ingresaste CR de crédito digita en número de días que das a tu cliente para el pago de las facturas, por ejemplo 30, si el cliente no tiene crédito deja este campo vacio',
            'Ingresa el monto de crédito que manejas con tu cliente, no incluyas puntos, si no tiene crédito deja este campo vacio'
        ]
        qrsDepartamentos = clsDepartamentosMdl.objects.all()
        srlDepartamentos = clsDepartamentosMdlSerializer(qrsDepartamentos, many=True)
        dtfDepartamentos = pd.DataFrame(srlDepartamentos.data)
        dtfDepartamentos = dtfDepartamentos.rename(columns={'id':'Código', 'department_name':'Departamento'})
        qrsCiudades = clsCiudadesMdl.objects.all()
        srlCiudades = clsCiudadesMdlSerializer(qrsCiudades, many=True)
        dtfCiudades = pd.DataFrame(srlCiudades.data)
        dtfCiudades = dtfCiudades.rename(columns={'id':'Código', 'city_name':'Ciudad'})
        qrsCategoriaCliente = clsCategoriaClienteMdl.objects.filter(state='AC')
        srlCategoriaCliente = clsCategoriaClienteMdlSerializer(qrsCategoriaCliente, many=True)
        dtfCategoriaCliente = pd.DataFrame(srlCategoriaCliente.data)
        dtfCategoriaCliente = dtfCategoriaCliente.rename(columns={'id':'Código', 'customer_cat':'Nombre categoría'})
        qrsZonaCliente = clsZonaClienteMdl.objects.filter(state='AC')
        srlZonaCliente = clsZonaClienteMdlSerializer(qrsZonaCliente, many=True)
        dtfZonaCliente = pd.DataFrame(srlZonaCliente.data)
        dtfZonaCliente = dtfZonaCliente.rename(columns={'id':'Código', 'customer_zone':'Nombre zona'})
        qrsAsesorComercial = clsAsesorComercialMdl.objects.filter(state='AC')
        srlAsesorComercial = CustomerAdvisorSerializer(qrsAsesorComercial, many=True)
        dtfAsesorComercial = pd.DataFrame(srlAsesorComercial.data)
        dtfAsesorComercial = dtfAsesorComercial.rename(columns={'id':'Código', 'advisor':'Nombre asesor'})
        dtfCatalogoClientes = pd.DataFrame(
            {
                'Tipo de persona':[],
                'Tipo de identificación':[],
                'Número de identificación':[],
                'Nombre cliente':[],
                'Nombre contacto':[],
                'Celular cliente':[],
                'Email':[],
                'Departamento':[],
                'Ciudad':[],
                'Zona':[],
                'Dirección':[],
                'Horario de entrega inicio':[],
                'Horario de entrega fin':[],
                'Categoría cliente':[],
                'Asesor comercial':[],
                'Método de pago':[],
                'Días de crédito':[],
                'Cupo de crédito':[],
            }, 
            index = [i for i in range (0, 0)]
            )
        lstNombresColumnasPlantilla = list(dtfCatalogoClientes.columns.values)
        lstTotalColumnas = [ i for i in range (1, len(lstNombresColumnasPlantilla) + 1) ]
        lstTipoDato = [
            'Alfabético', 
            'Alfabético', 
            'Numérico', 
            'AlfaNumérico',
            'AlfaNumérico',
            'Numérico', 
            'AlfaNumérico',
            'Numérico', 
            'Numérico', 
            'Numérico', 
            'AlfaNumérico',
            'AlfaNumérico',
            'AlfaNumérico',
            'Numérico', 
            'Numérico', 
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
            10, 
            50, 
            2,
            4,
            3,
            50,
            10,
            10,
            3, 
            3, 
            2, 
            5, 
            30
            ]
        lstCaracteresEspeciales = [
            'NO PERMITE', 
            'NO PERMITE', 
            'NO PERMITE', 
            'PERMITE Ñ',
            'PERMITE Ñ',
            'NO PERMITE',
            'PERMITE (@ .)', 
            'NO PERMITE', 
            'NO PERMITE', 
            'NO PERMITE', 
            'PERMITE Ñ', 
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
            'SI', 
            'SI', 
            'SI', 
            'SI', 
            'SI', 
            'SI', 
            'SI', 
            'SI', 
            'SI', 
            'NO',
            'NO'
            ]
        dtfInstructivoPlantilla = pd.DataFrame(
            {'Nº': lstTotalColumnas, 
            'NOMBRE CAMPO': lstNombresColumnasPlantilla, 
            'TIPO DE DATO': lstTipoDato,
            'LONGITUD MAX': lstLongitudMaxima,
            'CARACTERES ESPECIALES': lstCaracteresEspeciales,
            'OBSERVACIONES': lstObservaciones,
            'OBLIGATORIO': lstCampoObligatorio,
            },
            index = [i for i in range (0, len(lstTipoDato))]
            )
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="catalogo_clientes.xlsx"'
        with pd.ExcelWriter(response) as writer:
            dtfCatalogoClientes.to_excel(writer, sheet_name='PLANTILLA', index=False)
            dtfInstructivoPlantilla.to_excel(writer, sheet_name='INSTRUCTIVO', index=False)
            dtfDepartamentos.to_excel(writer, sheet_name='DEPARTAMENTOS', index=False)
            dtfCiudades.to_excel(writer, sheet_name='CIUDADES', index=False)
            dtfCategoriaCliente.to_excel(writer, sheet_name='CATEGORIAS', index=False)
            dtfZonaCliente.to_excel(writer, sheet_name='ZONAS', index=False)
            dtfAsesorComercial.to_excel(writer, sheet_name='ASESOR', index=False)
            fncAgregarAnchoColumna(writer, False, dtfCatalogoClientes, 'PLANTILLA')
            fncAgregarAnchoColumna(writer, True, dtfInstructivoPlantilla, 'INSTRUCTIVO')
            fncAgregarAnchoColumna(writer, True, dtfDepartamentos, 'DEPARTAMENTOS')
            fncAgregarAnchoColumna(writer, True, dtfCiudades, 'CIUDADES')
            fncAgregarAnchoColumna(writer, True, dtfCategoriaCliente, 'CATEGORIAS')
            fncAgregarAnchoColumna(writer, True, dtfZonaCliente, 'ZONAS')
            fncAgregarAnchoColumna(writer, True, dtfAsesorComercial, 'ASESOR')
            fncAgregarComentarioCeldas(writer, 'PLANTILLA', lstCeldasExcel, lstComentariosExcel)
        return response

''' 6.4 Vista para importar archivo clientes'''
class clsImportarCatalogoClientesViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_comercial/importar_catalogo_clientes.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lstNombresColumnas = [
            'Tipo de persona',
            'Tipo de identificación',
            'Número de identificación',
            'Nombre cliente',
            'Nombre contacto',
            'Celular cliente',
            'Email',
            'Departamento',
            'Ciudad',
            'Zona',
            'Dirección',
            'Horario de entrega inicio',
            'Horario de entrega fin',
            'Categoría cliente',
            'Asesor comercial',
            'Método de pago',
            'Días de crédito',
            'Cupo de crédito'
            ]
        tplValidaciones = (
            ((False,), (True, 2), (True, 1), (False,), (True, ('NT', 'JU'))),
            ((False,), (True, 2), (True, 1), (False,), (True, ('CC', 'NI', 'RU'))),
            ((True, 'identification', clsCatalogoClientesMdl), (True, 10), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, int), (True, 50), (True, 1), (False,)),
            ((True, 'mail'), (True, 100), (True, 1), (False,)),
            ((False,), (True, 3), (True, 1), (True, clsDepartamentosMdl)),
            ((False,), (False, ), (True, 1), (True, clsCiudadesMdl)),   
            ((False,), (True, 3), (True, 1), (True, clsZonaClienteMdl)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, time), (True, 10), (True, 1), (False,)),
            ((True, time), (True, 10), (True, 1), (False,)),
            ((False,), (True, 3), (True, 1), (True, clsCategoriaClienteMdl)),
            ((False,), (True, 3), (True, 1), (True, clsAsesorComercialMdl)),
            ((False,), (True, 2), (True, 1), (False,), (True, ('CR', 'CO'))),
            ((True, int), (True, 5), (False,), (False,)),
            ((True, float), (True, 30), (False, ), (False,)),
            )
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCargarArchivojsn':
                filCatalogoClientes = request.FILES['file']
                if str(filCatalogoClientes).endswith('.xlsx'):
                    dtfCatalogoClientes = pd.read_excel(filCatalogoClientes)
                    dtfCatalogoClientes = dtfCatalogoClientes.fillna(0)
                    lstValidarImportacion = [ fncValidarImportacionlst(dtfCatalogoClientes, i, j) for (i, j) in zip(lstNombresColumnas, tplValidaciones) ]
                    lstValidarImportacion = [ i for n in lstValidarImportacion for i in n ]
                    if len(lstValidarImportacion):
                        jsnClientes = dtfCatalogoClientes.to_json(orient="split")
                        jsnData['jsnClientes'] = jsnClientes
                        jsnData['lstValidarImportacion'] = lstValidarImportacion
                        jsnData['strErrorArchivo'] = 'El archivo presenta errores ¿desea descargarlos?'
                        response = JsonResponse(jsnData, safe=False)
                    else:
                        with transaction.atomic():
                            for i in (dtfCatalogoClientes.values.tolist()):
                                clsCatalogoClientesMdl.objects.create(
                                person_type = i[0],
                                id_type = i[1],
                                identification = int(i[2]),
                                business_name = i[3],
                                contact_name = i[4],
                                cel_number = int(i[5]),
                                email = i[6],
                                department_id = i[7],
                                city_id = i[8],
                                customer_zone_id = i[9],
                                delivery_address = i[10],
                                del_schedule_init = i[11],
                                del_schedule_end = i[12],
                                customer_cat_id = i[13],
                                commercial_advisor_id = i[14],
                                pay_method = i[15],
                                credit_days = int(i[16]),
                                credit_value = float(i[17]),
                                )
                        jsnData['success'] = '¡Se ha cargado el archivo a su base de datos con éxito!'
                        response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['error'] = 'Compruebe el formato del archivo'
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'btnArchivoErroresjsn':
                jsnCatalogoClientes = request.POST['jsnClientes']
                dtfCatalogoClientes = pd.read_json(jsnCatalogoClientes, orient='split')
                lstValidarImportacion = json.loads(request.POST['lstValidarImportacion'])
                lstErroresCeldas = list( dict.fromkeys([ i[1] for i in lstValidarImportacion ]) )
                dtfCatalogoClientes = fncAgregarErroresDataframedtf(dtfCatalogoClientes, lstValidarImportacion, lstErroresCeldas)
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="catalogo_clientes.xlsx"'
                with pd.ExcelWriter(response) as writer:
                    dtfCatalogoClientes.to_excel(writer, sheet_name='VALIDAR', index=False)
                    fncAgregarFormatoColumnasError(writer, lstValidarImportacion, 'VALIDAR', lstNombresColumnas)
                    fncAgregarAnchoColumna(writer, False, dtfCatalogoClientes, 'VALIDAR')
        except Exception as e:
            jsnData['error'] = str(e)
            response = JsonResponse(jsnData, safe=False)
        return response

''' 6.5 Vista para crear cliente'''
class clsCrearClienteViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = clsCatalogoClientesMdl
    form_class = clsCrearClienteFrm
    template_name = 'modulo_comercial/crear_cliente.html'
    success_url = reverse_lazy("comercial:listar_clientes")
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCrearClientejsn':
                with transaction.atomic():
                    frmCrearCliente = clsCrearClienteFrm(request.POST)
                    jsnData = frmCrearCliente.save()
            elif action == 'frmCrearCategoriaClientejsn':
                with transaction.atomic():
                    strCategoriaCliente = request.POST['customer_cat']
                    jsnMargenCategoriaCliente = json.loads(request.POST['margin_cat'])
                    qrsCategoriaCliente = clsCategoriaClienteMdl.objects.create(
                        customer_cat = strCategoriaCliente
                    )
                    for i in jsnMargenCategoriaCliente:
                        for j in i:
                            clsMargenCategoriaClienteMdl.objects.create(
                                customer_cat_id = qrsCategoriaCliente.id,
                                product_cat_id = j['id'],
                                margin_min = float(j['margin_min']),
                                margin_max = float(j['margin_max'])
                            )
                    jsnData = qrsCategoriaCliente.toJSON()
            elif action == 'frmCrearZonaClientejsn':
                with transaction.atomic():
                    frmCrearZonaCliente = clsCrearZonaClienteFrm(request.POST)
                    jsnData = frmCrearZonaCliente.save()
            elif action == 'frmCrearAsesorComercialjsn':
                with transaction.atomic():
                    frmCrearAsesorComercial = clsCrearAsesorComercialFrm(request.POST)
                    jsnData = frmCrearAsesorComercial.save()
            elif action == 'slcFiltrarCiudadesjsn':
                jsnData = [{'id': '', 'text': '------------'}]
                for i in clsCiudadesMdl.objects.filter(department_id=request.POST['intId']):
                    jsnData.append({'id': i.id, 'text': i.city_name})
            elif action == 'slcBuscarZonaClientejsn':
                jsnData = []
                qrsZonaCliente =clsZonaClienteMdl.objects.all()
                for i in qrsZonaCliente:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.customer_zone
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarCategoriaClientejsn':
                jsnData = []
                qrsCategoriaCliente =clsCategoriaClienteMdl.objects.all()
                for i in qrsCategoriaCliente:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.customer_cat
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarAsesorComercialjsn':
                jsnData = []
                qrsAsesorComercial =clsAsesorComercialMdl.objects.all()
                for i in qrsAsesorComercial:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.advisor
                    jsnData.append(dctJsn)
            elif action == 'tblMargenCategoriaProductojsn':
                jsnData = []
                qrsCategoriaProducto =clsCategoriaProductoMdl.objects.filter(state='AC')
                if len(qrsCategoriaProducto):
                    jsnData = []
                    for i in qrsCategoriaProducto:
                        dctJsn = i.toJSON()
                        dctJsn['margin_max'] = 0.00
                        dctJsn['margin_min'] = 0.00
                        jsnData.append(dctJsn)
                else:
                    jsnData['error'] = 'No existe(n) catergoría(s) de producto(s) creada(s), desea crear una?'    
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Cliente'
        context['create_url'] = reverse_lazy('comercial:crear_cliente')
        context['list_url'] = self.success_url
        context['action'] = 'frmCrearClientejsn'
        context['productCat'] = clsCategoriaProductoMdl.objects.all()
        context['frmClientCat'] = clsCrearCategoriaClienteFrm()
        context['frmZone'] = clsCrearZonaClienteFrm()
        context['frmAdvisor'] = clsCrearAsesorComercialFrm()
        return context

''' 6.6 Vista para listar e inactivar clientes'''
class clsListarCatalogoClientesViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = clsCatalogoClientesMdl
    template_name = 'modulo_comercial/listar_clientes.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'slcBuscarClientejsn':
                jsnData = []
                strCliente = request.POST['term'].strip()
                if len(strCliente):
                    qrsCatalogoClientes = clsCatalogoClientesMdl.objects.filter(Q(business_name__icontains=strCliente) | Q(identification__icontains=strCliente) | Q(cel_number__icontains=strCliente))[0:10]
                for i in qrsCatalogoClientes:
                    item = i.toJSON()
                    item['value'] = i.business_name
                    jsnData.append(item)
            elif action == 'btnEliminarClientejsn':
                qrsCatalogoClientes = clsCatalogoClientesMdl.objects.get(pk=request.POST['id'])
                if qrsCatalogoClientes.state == "AC":
                    qrsCatalogoClientes.state = "IN"
                    qrsCatalogoClientes.save()
                else:
                    qrsCatalogoClientes.state = "AC"
                    qrsCatalogoClientes.save()
                jsnData = qrsCatalogoClientes.toJSON()
            else:
                jsnData['error'] = 'Ha ocurrido un error'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla de Clientes'
        context['create_url'] = reverse_lazy('configuracion:crear_cliente')
        context['list_url'] = reverse_lazy('configuracion:listar_clientes')
        context['options_url'] = reverse_lazy('configuracion:opciones_cliente')
        return context

''' 6.7 Vista para editar cliente'''
class clsEditarClienteViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = clsCatalogoClientesMdl
    form_class = clsCrearClienteFrm
    template_name = 'modulo_comercial/crear_cliente.html'
    success_url = reverse_lazy("comercial:listar_clientes")
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmEditarClientejsn':
                frmEditarCliente = self.get_form()
                jsnData = frmEditarCliente.save()
            elif action == 'frmCrearCategoriaClientejsn':
                with transaction.atomic():
                    strCategoriaCliente = request.POST['customer_cat']
                    jsnMargenCategoriaCliente = json.loads(request.POST['margin_cat'])
                    qrsCategoriaCliente = clsCategoriaClienteMdl.objects.create(
                        customer_cat = strCategoriaCliente
                    )
                    for i in jsnMargenCategoriaCliente:
                        for j in i:
                            clsMargenCategoriaClienteMdl.objects.create(
                                customer_cat_id = qrsCategoriaCliente.id,
                                product_cat_id = j['id'],
                                margin_min = float(j['margin_min']),
                                margin_max = float(j['margin_max'])
                            )
                    jsnData = qrsCategoriaCliente.toJSON()
            elif action == 'frmCrearZonaClientejsn':
                with transaction.atomic():
                    frmCrearZonaCliente = clsCrearZonaClienteFrm(request.POST)
                    jsnData = frmCrearZonaCliente.save()
            elif action == 'frmCrearAsesorComercialjsn':
                with transaction.atomic():
                    frmCrearAsesorComercial = clsCrearAsesorComercialFrm(request.POST)
                    jsnData = frmCrearAsesorComercial.save()
            elif action == 'slcFiltrarCiudadesjsn':
                jsnData = [{'id': '', 'text': '------------'}]
                for i in clsCiudadesMdl.objects.filter(department_id=request.POST['intId']):
                    jsnData.append({'id': i.id, 'text': i.city_name})
            elif action == 'slcBuscarZonaClientejsn':
                jsnData = []
                qrsZonaCliente =clsZonaClienteMdl.objects.all()
                for i in qrsZonaCliente:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.customer_zone
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarCategoriaClientejsn':
                jsnData = []
                qrsCategoriaCliente =clsCategoriaClienteMdl.objects.all()
                for i in qrsCategoriaCliente:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.customer_cat
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarAsesorComercialjsn':
                jsnData = []
                qrsAsesorComercial =clsAsesorComercialMdl.objects.all()
                for i in qrsAsesorComercial:
                    dctJsn = i.toJSON()
                    dctJsn['text'] = i.advisor
                    jsnData.append(dctJsn)
            elif action == 'tblMargenCategoriaProductojsn':
                jsnData = []
                qrsCategoriaProducto =clsCategoriaProductoMdl.objects.filter(state='AC')
                if len(qrsCategoriaProducto):
                    jsnData = []
                    for i in qrsCategoriaProducto:
                        dctJsn = i.toJSON()
                        dctJsn['margin_max'] = 0.00
                        dctJsn['margin_min'] = 0.00
                        jsnData.append(dctJsn)
                else:
                    jsnData['error'] = 'No existe(n) catergoría(s) de producto(s) creada(s), desea crear una?'
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cliente'
        context['create_url'] = reverse_lazy('configuracion:crear_cliente')
        context['list_url'] = self.success_url
        context['action'] = 'frmEditarClientejsn'
        context['days_list'] = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        context['productCat'] = clsCategoriaProductoMdl.objects.all()
        context['frmClientCat'] = clsCrearCategoriaClienteFrm()
        context['frmZone'] = clsCrearZonaClienteFrm()
        context['frmAdvisor'] = clsCrearAsesorComercialFrm()
        return context

''' 6.8 Vista para exportar catálogo de clientes'''
class clsExportarCatalogoClientesViw(APIView):

    def get(self, request):
        qrsCatalogoClientes = clsCatalogoClientesMdl.objects.all()
        srlCatalogoClientes = clsCatalogoClientesMdlSerializer(qrsCatalogoClientes, many=True)
        dtfCatalogoClientes = pd.DataFrame(srlCatalogoClientes.data)
        dtfCatalogoClientes = dtfCatalogoClientes.rename(columns={
            'id':'Código',
            'date_creation': 'Fecha de creación',
            'date_update': 'Fecha de actualización',
            'person_type_display':'Tipo de persona',
            'id_type_display': 'Tipo de identificación',
            'identification': 'Número de identificación',
            'business_name':'Nombre cliente',
            'contact_name': 'Nombre contacto',
            'cel_number': 'Celular cliente',
            'email': 'Correo eléctronico',
            'department': 'Departamento',
            'city': 'Ciudad',
            'customer_zone': 'Zona',
            'delivery_address': 'Dirección',
            'del_schedule_init': 'Horario de entrega inicio',
            'del_schedule_end': 'Horario de entrega fin',
            'customer_cat': 'Categoría cliente',
            'commercial_advisor': 'Asesor comercial',
            'pay_method_display': 'Método de pago',
            'credit_days': 'Días de crédito',
            'credit_value': 'Cupo de crédito',
            'state_display': 'Estado'
            })
        lstNombresColumnas = [
            'Código',
            'Fecha de creación',
            'Fecha de actualización',
            'Tipo de persona',
            'Tipo de identificación',
            'Número de identificación',
            'Nombre cliente',
            'Nombre contacto',
            'Celular cliente',
            'Correo eléctronico',
            'Departamento',
            'Ciudad',
            'Zona',
            'Dirección',
            'Horario de entrega inicio',
            'Horario de entrega fin',
            'Categoría cliente',
            'Asesor comercial',
            'Método de pago',
            'Días de crédito',
            'Cupo de crédito',
            'Estado'
            ]
        dtfCatalogoClientes =dtfCatalogoClientes.reindex(columns=lstNombresColumnas)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="catalogo_clientes.xlsx"'
        with pd.ExcelWriter(response) as writer:
            dtfCatalogoClientes.to_excel(writer, sheet_name='CATALOGO_CLIENTES', index=False)
            fncAgregarAnchoColumna(writer, True, dtfCatalogoClientes, 'CATALOGO_CLIENTES')
        return response

#################################################################################################
# 7. CARTERA DE CLIENTES
#################################################################################################
''' 7.1 Vista para cartera clientes'''
class clsCarteraClientesViw(ListView):
    model = CustomerDebt
    template_name = 'modulo_comercial/ver_cartera_clientes.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in CustomerDebt.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla de cartera clientes'
        return context

#################################################################################################
# 8. TUBERÍA DE CLIENTES
#################################################################################################
''' 8.1 Vista para tubería clientes '''
class clsTuberiaClientesViw(ListView):
    model = CustomerDebt
    template_name = 'modulo_comercial/ver_tuberia_clientes.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in CustomerDebt.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla tubería de clientes'
        return context

#################################################################################################
# 9. PQR CLIENTES
#################################################################################################
''' 9.1 Vista para pqr clientes '''
class clsPqrClientesViw(ListView):
    model = CustomerDebt
    template_name = 'modulo_comercial/ver_pqr_clientes.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in CustomerDebt.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla PQR clientes'
        return context
