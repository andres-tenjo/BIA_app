import json
import os
from datetime import datetime, date
from datetime import timedelta
from pandas import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, PageBreak, Spacer, Table, Image, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm 
from reportlab.lib import colors

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
#from weasyprint import HTML, CSS

from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, FormView, View
from django.urls import reverse_lazy

from apps.mixins import IsSuperuserMixin, ValidatePermissionRequiredMixin
from .forms import *
from apps.modulo_configuracion.models import *
from apps.planeacion.models import *
from apps.modulo_compras.models import *
from apps.modulo_configuracion.forms import *


'''Vista para la ventana promociones'''
class PromotionView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    #model = Promotions
    template_name = 'modulo_comercial/promociones.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Promotions.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in PromotionProducts.objects.filter(prom_id=request.POST['id']):
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

'''Vista para la ventana crear pedido'''
class CreateOrderView(CreateView):
    model = Orders
    form_class = OrderForm
    template_name = 'modulo_comercial/crear_pedido.html'
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
                print(catalogo)
                pedidos = OrdersDetail.objects.filter(state='CU')
                cust_base = pedidos.filter(customer_id=request.POST['id_cust'])
                cust_base = cust_base.to_dataframe()
                print(cust_base)
                cat_base = pedidos.filter(city=request.POST['city'], category_cust=request.POST['category_cust'])
                cat_base = cat_base.to_dataframe()
                print(cat_base)
                gen_base = pedidos.to_dataframe()
                print(gen_base)
                added = json.loads(request.POST['ids'])
                print(added)

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
                print(x)
                print(len(x))

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
                        order_prods = OrdersDetail()
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
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['frmCust'] = clsCrearClienteFrm()
        context['list_url'] = reverse_lazy('comercial:listar_pedidos')
        context['action'] = 'add'
        return context

# class SaleInvoicePdfView(View):

#     def get(self, request, *args, **kwargs):
#         try:
#             template = get_template('modulo_comercial/invoice.html')
#             context = {
#                 'sale': Orders.objects.get(pk=self.kwargs['pk']),
#                 'comp': {'name': 'CONVERGENCIA SOLUCIONES S.A.S', 'NIT': '900817889-2', 'address': 'Calle 158 # 96a 25'},
#                 'icon': '{}{}'.format(settings.STATIC_URL, 'img/home/logo.png')
#             }
#             print(context)
#             html = template.render(context)
#             css_url = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.5.3-dist/css/bootstrap.min.css')
#             print(css_url)
#             pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])
#             return HttpResponse(pdf, content_type='application/pdf')
#         except:
#             pass
#         return HttpResponseRedirect(reverse_lazy('comercial:listar_pedidos'))

'''Vista para la ventana listar pedidos'''
class SaleList(ListView):
    model = Orders
    template_name = 'modulo_comercial/listar_pedidos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Orders.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in OrdersDetail.objects.filter(order_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Listado de Ventas'
        return context

'''Vista para la ventana crear cotización'''
class CreateQuoteView(CreateView):
    model = Quotes
    form_class = QuoteForm
    template_name = 'modulo_comercial/cotizaciones.html'
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
        context['list_url'] = reverse_lazy('comercial:listar_cotizaciones')
        context['frmCust'] = clsCrearClienteFrm()
        context['action'] = 'add'
        return context

'''Vista para la ventana listar cotizaciones'''
class QuoteList(ListView):
    model = Quotes
    template_name = 'modulo_comercial/listar_cotizaciones.html'

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
        context['title_table'] = 'Listado de Cotizaciones'
        return context

'''Vista para la ventana listar productos'''
class ProductView(ListView):
    model = clsCatalogoProductosMdl
    template_name = 'modulo_comercial/productos.html'

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

''' Vista para la ventana listar ruta de visitas '''
class VisitsRouteView(TemplateView):
    template_name = 'modulo_comercial/ruta_visitas.html'

''' Vista para la ventana listar llamadas'''
class CallCustomerView(ListView):
    model = VisitsRoute
    template_name = 'modulo_comercial/listar_llamadas.html'

    def get_queryset(self):
        queryset = self.model.objects.all()
        return queryset

''' Vista para la ventana crear llamada '''
class CreateCallCustomerView(CreateView):
    model = VisitsRoute
    form_class = VisitsRouteForm
    template_name = 'modulo_comercial/agendar_llamadas.html'
    success_url = reverse_lazy('comercial:listar_llamadas')
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

''' Vista para la ventana catálogo de clientes'''
class clsMenuCatalogoClientesViw(TemplateView):
    template_name = 'modulo_comercial/cli_cat.html'

''' Vista para la ventana crear cliente'''
class CustomerCreateView(CreateView):
    model = clsCatalogoClientesMdl 
    form_class = clsCrearClienteFrm
    template_name = 'modulo_comercial/crear_cliente.html'
    success_url = reverse_lazy('comercial:listar_clientes')
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                with transaction.atomic():
                    frmClient = clsCrearClienteFrm(request.POST)
                    data = frmClient.save()
            elif action == 'customer_credit':
                with transaction.atomic():
                    cust = json.loads(request.POST['customer'])
                    customer = ClientCatal()
                    customer.id_type = cust['id_type']
                    customer.id_number = cust['id_number']
                    customer.customer = cust['cust_name']
                    customer.cel_number = cust['cust_cel']
                    customer.email = cust['cust_mail']
                    customer.category_id = cust['cust_category']
                    customer.city = cust['cust_city']
                    customer.zone_id = cust['cust_zone']
                    customer.address = cust['cust_address']
                    customer.del_schedule2 = cust['cust_schedule']
                    customer.pay_method = cust['cust_pay_method']
                    customer.advisor_id = cust['cust_advisor']
                    customer.state = cust['cust_state']
                    customer.save()
                    cust_credit = CustomerCredit()
                    cust_credit.customer_id = customer.id
                    cust_credit.credit_value = cust['credit_limit']
                    cust_credit.payment_type_id = cust['credit_type']

            elif action == 'create_category':
                with transaction.atomic():
                    frmClientCat = CategoryClientForm(request.POST)
                    data = frmClientCat.save()
            elif action == 'create_zone':
                with transaction.atomic():
                    frmZone = clsCrearZonaClienteFrm(request.POST)
                    data = frmZone.save()
            elif action == 'create_payment':
                with transaction.atomic():
                    frmPayment = PaymentTypeForm(request.POST)
                    data = frmPayment.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Cliente'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['frmClientCat'] = CategoryClientForm()
        context['frmZone'] = clsCrearZonaClienteFrm()
        context['frmPayment'] = PaymentTypeForm()
        context['frmCredit'] = CustomerCreditForm()
        return context



''' Vista para la ventana listar clientes'''
class CustomerListView(ListView):
    model = clsCatalogoClientesMdl
    template_name = 'modulo_comercial/listar_cliente.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in ClientCatal.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla de Clientes'
        context['create_url'] = reverse_lazy('comercial:crear_cliente')
        context['list_url'] = reverse_lazy('comercial:listar_clientes')
        return context

''' Vista para la ventana actualizar clientes'''
class CustomerUpdateView(UpdateView):
    model = clsCatalogoClientesMdl
    form_class = clsCrearClienteFrm
    template_name = 'modulo_comercial/crear_cliente.html'
    success_url = reverse_lazy('comercial:listar_cliente')
    url_redirect = success_url
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un Cliente'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

''' Vista para cargar clientes'''
class CatCliUploadView(TemplateView):
    template_name = 'modulo_comercial/cli_upload.html'

''' Vista para la ventana listar categoría cliente'''
class CategoryCustListView(ListView):
    model = clsCategoriaClienteMdl
    template_name = 'modulo_comercial/crear_cliente_cat.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in CategoryClient.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                cat = CategoryClient()
                cat.name = request.POST['name']
                cat.state = request.POST['state']
                cat.save()
            elif action == 'edit':
                cat = CategoryClient.objects.get(pk=request.POST['id'])
                cat.name = request.POST['name']
                cat.state = request.POST['state']
                cat.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla categoría de clientes'
        context['list_url'] = reverse_lazy('comercial:crear_cat_cliente')
        context['form'] = CategoryClientForm
        return context

''' Vista para la ventana CRUD zona cliente'''
class ZoneCliView(ListView):
    model = clsZonaClienteMdl
    template_name = 'modulo_comercial/crear_cliente_zona.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in clsZonaClienteMdl.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                zone = clsZonaClienteMdl()
                zone.name = request.POST['name']
                zone.state = request.POST['state']
                zone.save()
            elif action == 'edit':
                zone = clsZonaClienteMdl.objects.get(pk=request.POST['id'])
                zone.name = request.POST['name']
                zone.state = request.POST['state']
                zone.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla zonas de clientes'
        context['list_url'] = reverse_lazy('comercial:crear_zona_cliente')
        return context

''' Vista para la ventana CRUD asesor cliente'''
class AdvisorCliView(ListView):
    model = clsAsesorComercialMdl
    template_name = 'modulo_comercial/crear_cliente_asesor.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in clsAsesorComercialMdl.objects.all():
                    data.append(i.toJSON())
            elif action == 'add':
                advisor = clsAsesorComercialMdl()
                advisor.name = request.POST['name']
                advisor.zone = request.POST['zone']
                advisor.days_week = request.POST['days_week']
                advisor.activity = request.POST['activity']
                advisor.start_time = request.POST['start_time']
                advisor.end_time = request.POST['end_time']
                advisor.end_time = request.POST['end_time']
                advisor.lunch_start_time = request.POST['lunch_start_time']
                advisor.lunch_end_time = request.POST['lunch_end_time']
                advisor.break_start_time = request.POST['break_start_time']
                advisor.break_end_time = request.POST['break_end_time']
                advisor.break2_start_time = request.POST['break2_start_time']
                advisor.break2_end_time = request.POST['break2_end_time']
                advisor.state = request.POST['state']
                advisor.save()
            elif action == 'edit':
                advisor = clsAsesorComercialMdl.objects.get(pk=request.POST['id'])
                advisor.name = request.POST['name']
                advisor.zone = request.POST['zone']
                advisor.days_week = request.POST['days_week']
                advisor.activity = request.POST['activity']
                advisor.start_time = request.POST['start_time']
                advisor.end_time = request.POST['end_time']
                advisor.end_time = request.POST['end_time']
                advisor.lunch_start_time = request.POST['lunch_start_time']
                advisor.lunch_end_time = request.POST['lunch_end_time']
                advisor.break_start_time = request.POST['break_start_time']
                advisor.break_end_time = request.POST['break_end_time']
                advisor.break2_start_time = request.POST['break2_start_time']
                advisor.break2_end_time = request.POST['break2_end_time']
                advisor.state = request.POST['state']
                advisor.save()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla asesores de ventas'
        context['list_url'] = reverse_lazy('comercial:crear_asesor_cliente')
        return context

''' Vista para la ventana cartera cliente'''
class CarteraCliView(ListView):
    model = CustomerDebt
    template_name = 'modulo_comercial/cartera_clientes.html'

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

''' Vista para la ventana historico de movimientos'''
def historico_mov_comercial(request):
    return render(request, 'modulo_comercial/historico_mov_comercial.html')

''' Vista para ventana de indicadores comerciales'''
class CommercialIndicatorsView(TemplateView):
    template_name = 'modulo_comercial/indicadores_comercial.html'


'''

class CreateProduct(CreateView):
    model = clsCatalogoProductosMdl
    form_class = ProductForm
    template_name = 'modulo_comercial/crear_producto.html'
    success_url = reverse_lazy("comercial:listar_productos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formulario de creación de producto'
        context['list_url'] = reverse_lazy('comercial:listar_productos')
        context['action'] = 'add'
        return context
    
    def post(self,request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

class UpdateProduct(UpdateView):
    model = clsCatalogoProductosMdl
    form_class = ProductForm
    template_name = 'modulo_comercial/crear_producto.html'
    success_url = reverse_lazy("comercial:listar_productos")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar producto'
        context['list_url'] = reverse_lazy('comercial:listar_productos')
        context['action'] = 'edit'
        return context
    
    def dispatch(self,request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    
class DeleteProduct(DeleteView):
    model = clsCatalogoProductosMdl
    template_name = 'modulo_comercial/eliminar_producto.html'
    success_url = reverse_lazy("comercial:listar_productos")

    def dispatch(self,request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar producto'
        context['list_url'] = reverse_lazy('comercial:listar_productos')
        return context

class Select2(TemplateView):
    template_name = 'modulo_comercial/select2.html'
     
    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_client_id':
                data = [{ 'id': '', 'text': '------------'}]
                for i in ClientCatal.objects.filter(category=request.POST['id']):
                    data.append({'id': i.id, 'text': i.name, 'data': i.category.toJSON()})
            elif action == 'autocomplete':
                data = []
                for i in CategoryClient.objects.filter(name__icontains=request.POST['term'])[0:10]:
                    item = i.toJSON()
                    item['text'] = i.name
                    data.append(item)
            else:
                data['error'] = 'No se encontraron resultados'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['title'] = 'Select Anidados'
        context['form'] = SelectForm
        return context


class ProductView(ListView):
    model = clsCatalogoProductosMdl
    template_name = 'modulo_comercial/productos.html'

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
            elif action == 'add':
                prod = clsCatalogoProductosMdl()
                prod.cod = request.POST['cod']
                prod.name = request.POST['name']
                prod.pres = request.POST['pres']
                prod.brand = request.POST['brand']
                prod.category_id = request.POST['category']
                prod.subcategory_id = request.POST['subcategory']
                prod.unit_price = request.POST['unit_price']
                prod.udc = request.POST['udc']
                prod.udv = request.POST['udv']
                prod.equiv = request.POST['equiv']
                prod.del_time = request.POST['del_time']
                prod.bar_code = request.POST['bar_code']
                prod.iva = request.POST['iva']
                prod.state = request.POST['state']
                prod.save()
            elif action == 'edit':
                prod = clsCatalogoProductosMdl.objects.get(pk=request.POST['id'])
                prod.cod = request.POST['cod']
                prod.name = request.POST['name']
                prod.pres = request.POST['pres']
                prod.brand = request.POST['brand']
                prod.category_id = request.POST['category']
                prod.subcategory_id = request.POST['subcategory']
                prod.unit_price = request.POST['unit_price']
                prod.udc = request.POST['udc']
                prod.udv = request.POST['udv']
                prod.equiv = request.POST['equiv']
                prod.del_time = request.POST['del_time']
                prod.bar_code = request.POST['bar_code']
                prod.iva = request.POST['iva']
                prod.state = request.POST['state']
                prod.save()
            elif action == 'delete':
                prod = clsCatalogoProductosMdl.objects.get(pk=request.POST['id'])
                prod.delete()
            else:
                data['error'] = 'Se presento un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado productos'
        context['create_url'] = reverse_lazy("comercial:crear_producto")
        context['form'] = ProductForm()
        context['create_modal_title'] = 'Crear de producto'
        return context
        '''