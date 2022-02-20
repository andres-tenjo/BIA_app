import json
from pandas import pandas as pd

from django.conf import settings
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.db.models import Q
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, FormView, View
from django.urls import reverse_lazy

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.mixins import IsSuperuserMixin, ValidatePermissionRequiredMixin
from .forms import *
from .models import *
from apps.modulo_comercial.models import *
from apps.modulo_logistica.models import *
from apps.modulo_compras.models import *
from apps.functions_views import *
from apps.Modelos.Several_func import *


# Planeación comercial
# Ajustes de inventario
''' Vista para planeación comercial'''
class clsPlaneacionComercialVista(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/ajustes_inventario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options_title'] = 'Establecer Indicadores'
        context['options_url'] = reverse_lazy('configuracion:importar_ajustes_inventario')
        context['create_title'] = 'Ver '
        context['create_url'] = reverse_lazy('configuracion:crear_ajuste_inventario')
        context['search_title'] = 'Ver historico'
        context['search_url'] = reverse_lazy('configuracion:listar_productos')
        return context


''' Vista ventana principal planificación comercial'''
class CommercialPlanningMainView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'planeacion/plan_com_main.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_data':
                if len(orders_data) < 2:
                    data['msg'] = orders_data['msg']
                else:
                    data['msg'] = orders_data['msg']
                    data['return'] = orders_data['return']
            else:
                data['error'] = 'No se encontraron resultados'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

''' Vista para importar historico pedidos'''
class OrdersImport(LoginRequiredMixin, TemplateView):
    template_name = 'planeacion/import_orders.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        colname_list = [
            'Tipo de persona', 'Tipo de identificación', 'Nombre proveedor', 'Email', 
            'Nombre contacto', 'Celular contacto', 'Nombre otro contacto', 'Costo de compra', 
            'Celular otro contacto', 'Departamento', 'Ciudad', 'Dirección', 
            'Código postal', 'Método de pago', 'Días de crédito', 'Cupo de crédito', 
            'Condiciones de compra', 'Cantidad mínima', 'Cantidad mínima de compra', 'Volumen mínimo', 
            'Volumen mínimo de compra', 'Valor mínimo', 'Valor mínimo de compra',
            ]
        val = (
            ((True, str), (True, 2), (True, 2), (False,)),
            ((True, str), (True, 2), (True, 2), (False,)),
            ((True, int), (True, 10), (True, 7), (False,)),
            ((True, str), (True, 50), (True, 6), (False,)),
            # correo
            ((True, str), (True, 50), (True, 10), (False,)),
            ((True, str), (True, 50), (True, 5), (False,)),
            ((True, int), (True, 10), (True, 7), (False,)),
            ((True, str), (True, 50), (False,), (False,)),
            ((True, int), (True, 10), (False,), (False,)),
            ((True, str), (True, 3), (True, 1), (True, clsDepartamentosMdl)),
            ((True, str), (True, 3), (True, 1), (True, clsCiudadesMdl)),
            ((True, str), (True, 50), (True, 5), (False,)),
            ((True, int), (True, 6), (True, 6), (False,)),
            ((True, str), (True, 2), (True, 2), (False,)),
            ((True, int), (True, 3), (False, ), (False,)),
            ((True, float), (True, 30), (False, ), (False,)),
            ((True, int), (True, 1), (False,), (False,)),
            ((True, int), (True, 1), (False,), (False,)),
            ((True, int), (True, 5), (False,), (False,)),
            ((True, int), (True, 1), (False,), (False,)),
            ((True, int), (True, 5), (False,), (False,)),
            ((True, int), (True, 1), (False,), (False,)),
            ((True, float), (True, 30), (False, ), (False,)),
            )
        data = {}
        try:
            action = request.POST['action']
            if action == 'upload':
                file_format = request.POST.get('file-format')
                new_file = request.FILES['file']
                if file_format == 'CSV':
                    if str(new_file).endswith('.csv'):
                        df_prod = pd.read_csv(new_file)
                        df_prod = df_prod.fillna(0)
                        validate = [ fncValidarImportacionlst(df_prod, i, j) for (i, j) in zip(colname_list, val) ]
                        validate = [ i for n in validate for i in n ]
                        if len(validate):
                            result = df_prod.to_json(orient="split")
                            data['df_prod'] = result
                            data['validate'] = validate
                            data['error_data'] = 'El archivo presenta errores, desea descargarlos?'
                            response = JsonResponse(data, safe=False)
                        else:
                            with transaction.atomic():
                                for product in (df_prod.values.tolist()):
                                    for j in product:
                                        if j != 0:
                                            p = clsCatalogoProductosMdl.objects.create(
                                            product_desc = product[0],
                                            presentation = product[1],
                                            product_cat_id = product[2],
                                            product_subcat_id = product[3],
                                            trademark = product[4],
                                            purchase_unit_id = product[5],
                                            quantity_pu = product[6],
                                            cost_pu = product[7],
                                            sales_unit_id = product[8],
                                            quantity_su = product[9],
                                            full_sale_price = float(product[10]),
                                            bar_code = int(product[11]),
                                            split = int(product[6]/product[9]),
                                            iva = float(product[12]),
                                            other_tax = float(product[13]),
                                            del_time = int(product[14]),
                                            product_dimention = int(product[15]),
                                            weight_udc = float(product[16]),
                                            width_udc = float(product[17]),
                                            high_udc = float(product[18]),
                                            length_udc = float(product[19]),
                                            orientation_udc = int(product[20]),
                                            stacking_udc = int(product[21]),
                                            weight_udv = float(product[22]),
                                            width_udv = float(product[23]),
                                            high_udv = float(product[24]),
                                            length_udv = float(product[25]),
                                            orientation_udv = int(product[26]),
                                            stacking_udv = int(product[27]),
                                            storage_conditions = int(product[28]),
                                            restriction_temperature = int(product[30]),
                                            )
                                            cr_c = [int(product[29])]
                                            if cr_c[0] != 0:
                                                for i in cr_c:
                                                    p.cross_contamination.add(i)
                                                    p.save()
                                            else:
                                                pass
                                        else:
                                            pass
                            data['success'] = 'Se ha cargado el archivo a su base de datos con éxito!'
                            response = JsonResponse(data, safe=False)
                    else:
                        mensaje = 'Compruebe el formato del archivo'
                        response = JsonResponse({'mensaje': mensaje})
                        response.status_code = 400
                elif  file_format == 'XLSX':
                    if str(new_file).endswith('.xlsx'):
                        df_supp = pd.read_excel(new_file)
                        df_supp = df_supp.fillna(0)
                        validate = [ fncValidarImportacionlst(df_supp, i, j) for (i, j) in zip(colname_list, val) ]
                        validate = [ i for n in validate for i in n ]
                        if len(validate):
                            result = df_supp.to_json(orient="split")
                            data['df_supp'] = result
                            data['validate'] = validate
                            data['error_data'] = 'El archivo presenta errores, desea descargarlos?'
                            response = JsonResponse(data, safe=False)
                        else:
                            with transaction.atomic():
                                for supplier in (df_supp.values.tolist()):
                                    for j in supplier:
                                        if j != 0:
                                            clsCatalogoProveedoresMdl.objects.create(
                                            person_type = supplier[0],
                                            id_type = supplier[1],
                                            identification = int(supplier[2]),
                                            supplier_name = supplier[3],
                                            email = supplier[4],
                                            contact_name = supplier[5],
                                            contact_cel = int(supplier[6]),
                                            other_contact_name = supplier[7],
                                            other_contact_cel = int(supplier[8]),
                                            department = supplier[9],
                                            city = supplier[10],
                                            supplier_address = supplier[11],
                                            postal_code = int(supplier[6]),
                                            pay_method = supplier[12],
                                            credit_days = int(supplier[13]),
                                            credit_limit = float(supplier[14]),
                                            purchase_conditions = supplier[15],
                                            min_quantity = supplier[16],
                                            min_purchase_quantity = int(supplier[17]),
                                            min_volume = supplier[18],
                                            min_purchase_vol = int(supplier[19]),
                                            min_value = supplier[20],
                                            min_purchase_value = float(supplier[21])
                                            )
                                        else:
                                            pass
                            data['success'] = 'Se ha cargado el archivo a su base de datos con éxito!'
                            response = JsonResponse(data, safe=False)
                    else:
                        data['error'] = 'Compruebe el formato del archivo'
                        response = JsonResponse(data, safe=False)
            elif action == 'download_errors':
                df_supp = request.POST['df_supp']
                df_supp = pd.read_json(df_supp, orient='split')
                validate = json.loads(request.POST['validate'])
                error_row = list( dict.fromkeys([ i[1] for i in validate ]) )
                df_supp = df_supp.assign(Validación='')
                for i in validate:
                    fncAgregarColumnaValidaciondtf(df_supp, i[1], fncAgregarErrorFilastr(df_supp, error_row))
                success_row = [ i for i in range(0, len(df_supp)) if i not in error_row ]
                for i in success_row:
                    fncAgregarColumnaValidaciondtf(df_supp, i, 'Correcto')
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="catalogo_productos.xlsx"'
                with pd.ExcelWriter(response) as writer:
                    df_supp.to_excel(writer, sheet_name='VALIDAR', index=False)
                    workbook = writer.book
                    plantilla = writer.sheets['VALIDAR']
                    e_type = workbook.add_format({
                        'bold': True,
                        'fg_color': '#f10a0a',
                        })
                    e_l_max = workbook.add_format({
                        'bold': True,
                        'fg_color': '#daf10a',
                        })
                    e_l_min = workbook.add_format({
                        'bold': True,
                        'fg_color': '#0011fa',
                        })
                    e_bbdd = workbook.add_format({
                        'bold': True,
                        'fg_color': '#0af130',
                        })
                    for i in validate:
                        if i[2] == 'Tipo de dato':
                            plantilla.write(i[1] + 1, colname_list.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_type)
                        elif i[2] == 'Longitud max':
                            plantilla.write(i[1]+ 1, colname_list.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_l_max)
                        elif i[2] == 'Longitud min':
                            plantilla.write(i[1]+ 1, colname_list.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_l_min)
                        elif i[2] == 'No existe en base de datos':
                            plantilla.write(i[1]+ 1, colname_list.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_bbdd)
                        else:
                            pass
        except Exception as e:
            data['error'] = str(e)
            response = JsonResponse(data, safe=False)
        return response

''' Vista ventana historico de plan comercial'''
class HistPlanningComView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = CommercialPlanning
    template_name = 'planeacion/hist_plan_comercial.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in CommercialPlanning.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

''' Vista para planificación comercial'''
class CommercialPlanningView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'planeacion/pronostico_listado.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Planificación comercial'
        context['form_plan'] = CommercialPlanningForm
        return context

    def post(self, request, *args, **kwargs):
        data = {}

        def total_orders():
            orders_list = []
            orders = Orders.objects.all()
            orders = orders.to_dataframe()
            orders['order_date'] = pd.to_datetime(orders['order_date'], format='%Y-%m-%d')
            orders['year'] = orders['order_date'].dt.year
            orders['month'] = orders['order_date'].dt.month
            orders['week'] = orders['order_date'].dt.isocalendar().week
            
            # Agrupando por semanas la base de pedidos
            orders_week = orders.groupby(['year', 'week'])['total'].sum().reset_index()
            orders_list.append(orders_week)
            orders_month = orders.groupby(['year', 'month'])['total'].sum().reset_index()
            orders_list.append(orders_month)
            total_week = len(orders_week)
            orders_list.append(total_week)
            return orders_list
        
        def get_planning():
            planning = []
            orders = total_orders()
            orders_month = orders[1]
            total_week = orders[2]
            
            #total_week = 0

            com_planning = CommercialPlanning.objects.all()
            com_planning = com_planning.to_dataframe()
            total_planning = len(com_planning)
            
            #total_planning = 0

            if total_week == 0 and total_planning == 0:
                msg = 'No cuenta con historico de ventas, por favor ingrese su meta monetaria'
                planning.append(msg)
                planning.append(total_week)
            elif total_week > 0 and total_planning == 0:
                msg = 'Por favor ingrese su meta monetaria y porcentual'
                planning.append(msg)
                planning.append(total_week)
            else:
                msg = 'Por favor ingrese su meta monetaria'
                planning.append(msg)
                last_sale = orders_month.iloc[-1]['total']
                last_sale = 12000000
                planning.append(last_sale)
                last_planning = com_planning.iloc[-1]['monetary_goal']
                planning.append(last_planning)
                planning.append(total_week)
            return planning

        def get_forecast():
            forecast = []
            orders = total_orders()
            #orders_week = orders[0]
            total_week = orders[2]
            total_week = 13
             
            if total_week > 12:
                msg = 'Se ha ejecutado el pronóstico de ventas exitosamente'
                forecast.append(msg)
                forecast_model = []
                forecast_table = Forecast.objects.all()
                #forecast_graph = data_graph
                forecast_model.append(forecast_table)
                forecast.append(forecast_model)
            else:
                msg = f'Para ejecutar esta función debe tener un minimo de 12 semanas de historico de ventas que garantice los mejores escenarios, usted tiene {total_week} semanas'
                forecast.append(msg)
            return forecast

        def category_forecast(category_df):
            l = []

            # Función para evaluar si existen 2 o más opciones por categoría
            def val_crit1(l):
                size = len(l)
                if size > 1:
                    return [True]
                else:
                    return [False]

            # Función para evaluar si cada categoria y tipo cuentan con los datos para ejecutar pronóstico
            def crit2(l):
                L= []
                def contar(i):
                    if len(i['week'])>= 12:
                        return True
                    else:
                        return False
                for i in l:
                    l1= []
                    for j in i:    
                        l1.append(contar(j))
                    L.append(l1)
                return L
            
            # Función para evaluar si cada categoria y tipo cuentan con los datos para ejecutar pronóstico
            def val_crit3(t):
                L= []
                for i in t:
                    if i[0][0] == True:
                        if sum(i[1]) > 0:
                            L.append(i[1])
                        else:
                            L.append([False])
                    else:
                        L.append([False])
                return(L)
            
            l.append(category_df)
            crit1 = [ val_crit1(i) for i in l ]
            crit2 = crit2(l)
            crits = [ (i, j) for (i, j) in zip(crit1, crit2) ]
            #crits = [([True], [True, False, False]), ([True], [True, False, False, False]), ([False], [False]), ([True], [False, False, False, False, False]), ([True], [False, False, False, False, False, False, False, False])]
            crit3 = val_crit3(crits)
            return crit3

        def city_forecast():
            val_city = []
            orders = Orders.objects.all()
            orders = orders.to_dataframe()
            orders['order_date'] = pd.to_datetime(orders['order_date'], format='%Y-%m-%d')
            orders['year'] = orders['order_date'].dt.year
            orders['week'] = orders['order_date'].dt.isocalendar().week
            customer = clsCatalogoClientesMdl.objects.all()                
            customer = customer.to_dataframe()
            orders = orders.merge(customer, how='left', on='customer')
            orders = orders.drop(['user_creation_x', 'date_creation_x', 'user_update_x', 'date_update_x','id_y', 'id_y', 'user_creation_y', 'date_creation_y', 'user_update_y', 'date_update_y'], axis=1)
            city_week = orders.groupby(['week', 'city'])['total'].sum().reset_index()
            city = city_week.drop_duplicates(subset=['city'])

            
            if len(city) > 1:
                city_group_week = [i for n, i in city_week.groupby(pd.Grouper(key='city'))]
                cat_for = category_forecast(city_group_week)
                
                if len(cat_for) > 1:
                    msg = 'Se ha generado el pronóstico exitosamente'
                    val_city.append(msg)
                    forecast_city = []
                    city_table = ForecastCity.objects.all()
                    for i in city_table:
                        forecast_city.append(i.toJSON())   
                        val_city.append(forecast_city)
                else:
                    msg = 'Se ha generado el pronóstico exitosamente'
                    val_city.append(msg)
                    forecast_city = []
                    city_table = ForecastCity.objects.all()
                    for i in city_table:
                        forecast_city.append(i.toJSON())
                        val_city.append(forecast_city)
            else:
                msg = 'Usted no puede ejecutar filtro por ciudad'
                val_city.append(msg)
            return val_city

            '''zone_week = orders.groupby(['week', 'zone'])['total'].sum().reset_index()
            zone = zone_week.drop_duplicates(subset=['zone'])
            if len(zone) > 1:
                zone_group_week = [i for n, i in zone_week.groupby(pd.Grouper(key='zone'))]
                l.append(zone_group_week)
            else:
                msg = 'Usted no puede ejecutar filtro por Zona'
                l.append(msg)

            advisor_week = orders.groupby(['week', 'advisor'])['total'].sum().reset_index()
            advisor = advisor_week.drop_duplicates(subset=['advisor'])
            if len(advisor) > 1:
                advisor_group_week = [i for n, i in advisor_week.groupby(pd.Grouper(key='advisor'))]
                l.append(advisor_group_week)
            else:
                msg = 'Usted no puede ejecutar filtro por asesor'
                l.append(msg)

            category_week = orders.groupby(['week', 'category'])['total'].sum().reset_index()
            category = category_week.drop_duplicates(subset=['category'])
            if len(category) > 1:
                category_group_week = [i for n, i in category_week.groupby(pd.Grouper(key='category'))]
                l.append(category_group_week)
            
            customer_week = orders.groupby(['week', 'customer'])['total'].sum().reset_index()
            customer = customer_week.drop_duplicates(subset=['customer'])
            if len(customer) > 1:
                customer_group_week = [i for n, i in customer_week.groupby(pd.Grouper(key='customer'))]
                l.append(customer_group_week)
                        
            if len(l):
                crit1 = [ val_crit1(i) for i in l ]
                crit2 = crit2(l)
                crits = [ (i, j) for (i, j) in zip(crit1, crit2) ]
                #crits = [([True], [True, False, False]), ([True], [True, False, False, False]), ([False], [False]), ([True], [False, False, False, False, False]), ([True], [False, False, False, False, False, False, False, False])]
                crit3 = val_crit3(crits)
            return(crit3)'''

        try:
            action = request.POST['action']
            if action == 'get_data':
                planning = get_planning()
                if len(planning) > 2:
                    data['msg'] = planning[0]
                    data['last_sale'] = planning[1]
                    data['last_planning'] = planning[2]
                    data['total_week'] = planning[3]
                else:
                    data['msg'] = planning[0]
                    data['total_week'] = planning[1]
            
            elif action == 'get_forecast':
                forecast = get_forecast()
                if len(forecast) == 1:
                    data['msg'] = forecast[0]
                else:
                    forecast_table = [ i.toJSON() for i in forecast[1][0] ]
                    data['msg'] = forecast[0]
                    data['forecast_table'] = forecast_table
                    #data['forecast_graf'] = forecast[1][1]

            elif action == 'get_forecast_city':
                city_forecast = city_forecast()
                if len(city_forecast) > 1:
                    data['msg'] = city_forecast[0]
                    data['table_city'] = city_forecast[1]
                else:
                    data['msg'] = city_forecast[0]

            elif action == 'forecast_zone':
                if len(crit3[1]) == 1:
                    data = 'No puede ejecutar este filtro'    
                    json.dumps(data)
                elif len(crit3[1]) > 1:
                    data = 'Ejecutar pronostico'
                    json.dumps(data)
            elif action == 'forecast_advisor':
                if len(crit3[2]) == 1:
                    data = 'No puede ejecutar este filtro'    
                    json.dumps(data)
                elif len(crit3[2]) > 1:
                    data = 'Ejecutar pronostico'
                    json.dumps(data)
            elif action == 'forecast_catcust':
                if len(crit3[3]) == 1:
                    data = 'No puede ejecutar este filtro'    
                    json.dumps(data)
                elif len(crit3[3]) > 1:
                    data = 'Ejecutar pronostico'
                    json.dumps(data)
            elif action == 'forecast_customer':
                if len(crit3[4]) == 1:
                    data = 'No puede ejecutar este filtro'    
                    json.dumps(data)
                elif len(crit3[4]) > 1:
                    data = 'Ejecutar pronostico'
                    json.dumps(data)
            else:
                data['error'] = 'No se encontraron resultados'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
 
''' Vista para planificación de actividades comerciales'''
class CommercialPlanActivitiesView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'planeacion/plan_act_comercial.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

''' Vista ventana promociones'''
class PromotionsView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'planeacion/promociones.html'

''' Vista para creación de promociones'''
class CreatePromotionsView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Promotions
    form_class = PromoForm
    template_name = 'planeacion/crear_promocion.html'
    success_url = reverse_lazy("planeacion:listar_promociones")
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                ids_exclude = json.loads(request.POST['ids'])
                term = request.POST['term'].strip()
                if len(term):
                    prods = clsCatalogoProductosMdl.objects.filter(Q(name__icontains=term) | Q(cod__icontains=term) | Q(pres__icontains=term))[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    prom = json.loads(request.POST['prom'])
                    promotions = Promotions()
                    promotions.name = prom['name']
                    promotions.desc = prom['desc']
                    promotions.quantity = float(prom['quantity'])
                    promotions.cons = prom['cons']
                    promotions.obs = prom['obs']
                    promotions.expiration_date = prom['expiration_date']
                    promotions.save()
                    for i in prom['products']:
                        det_prom = PromotionProducts()
                        det_prom.prom_id = promotions.id
                        det_prom.product_id = i['id']
                        det_prom.und_venta_id = i['udc']['id']
                        det_prom.quantity = float(i['quantity_udv'])
                        det_prom.unit_price = float(i['price_udv'])
                        det_prom.prom_price = float(i['price_udc'])
                        det_prom.save()
                    data = {'id': promotions.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Promoción'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        return context

''' Vista ventana historico de plan comercial'''
class PromotionListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Promotions
    template_name = 'planeacion/listar_promociones.html'

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
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

''' Vista para novedades de ventas'''
class SalesNewsView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'planeacion/novedades_ventas.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# Tuberia de clientes

''' Vista ventana cartera de clientes'''
class CarteraCliView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = CustomerDebt
    template_name = 'planeacion/cartera_clientes.html'

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

# Indicadores comercial

# Módulo compras

# Planeación de compras
# Módulo comercial
''' Vista ventana principal planificación comercial'''
class PurchasePlanningMainView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'planeacion/plan_compras_main.html'

''' Vista ventana historico de plan comercial'''
class HistPlanningPurchView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = CommercialPlanning
    template_name = 'planeacion/hist_plan_compras.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in CommercialPlanning.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

''' Vista para planificación comercial'''
class PurchasePlanningView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'planeacion/plan_compras.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Planificación compras'
        context['form_plan'] = CommercialPlanningForm
        return context

    def post(self, request, *args, **kwargs):
        data = {}

        def total_orders():
            orders_list = []
            orders = Orders.objects.all()
            orders = orders.to_dataframe()
            orders['order_date'] = pd.to_datetime(orders['order_date'], format='%Y-%m-%d')
            orders['year'] = orders['order_date'].dt.year
            orders['month'] = orders['order_date'].dt.month
            orders['week'] = orders['order_date'].dt.isocalendar().week
            
            # Agrupando por semanas la base de pedidos
            orders_week = orders.groupby(['year', 'week'])['total'].sum().reset_index()
            orders_list.append(orders_week)
            orders_month = orders.groupby(['year', 'month'])['total'].sum().reset_index()
            orders_list.append(orders_month)
            total_week = len(orders_week)
            orders_list.append(total_week)
            return orders_list
        
        def get_planning():
            planning = []
            orders = total_orders()
            orders_month = orders[1]
            total_week = orders[2]
            
            #total_week = 0

            com_planning = CommercialPlanning.objects.all()
            com_planning = com_planning.to_dataframe()
            total_planning = len(com_planning)
            
            #total_planning = 0

            if total_week == 0 and total_planning == 0:
                msg = 'No cuenta con historico de ventas, por favor ingrese su meta monetaria'
                planning.append(msg)
                planning.append(total_week)
            elif total_week > 0 and total_planning == 0:
                msg = 'Por favor ingrese su meta monetaria y porcentual'
                planning.append(msg)
                planning.append(total_week)
            else:
                msg = 'Por favor ingrese su meta monetaria'
                planning.append(msg)
                last_sale = orders_month.iloc[-1]['total']
                last_sale = 12000000
                planning.append(last_sale)
                last_planning = com_planning.iloc[-1]['monetary_goal']
                planning.append(last_planning)
                planning.append(total_week)
            return planning

        def get_forecast():
            forecast = []
            orders = total_orders()
            #orders_week = orders[0]
            total_week = orders[2]
            total_week = 13
             
            if total_week > 12:
                msg = 'Se ha ejecutado el pronóstico de ventas exitosamente'
                forecast.append(msg)
                forecast_model = []
                forecast_table = Forecast.objects.all()
                #forecast_graph = data_graph
                forecast_model.append(forecast_table)
                forecast.append(forecast_model)
            else:
                msg = f'Para ejecutar esta función debe tener un minimo de 12 semanas de historico de ventas que garantice los mejores escenarios, usted tiene {total_week} semanas'
                forecast.append(msg)
            return forecast

        def category_forecast(category_df):
            l = []

            # Función para evaluar si existen 2 o más opciones por categoría
            def val_crit1(l):
                size = len(l)
                if size > 1:
                    return [True]
                else:
                    return [False]

            # Función para evaluar si cada categoria y tipo cuentan con los datos para ejecutar pronóstico
            def crit2(l):
                L= []
                def contar(i):
                    if len(i['week'])>= 12:
                        return True
                    else:
                        return False
                for i in l:
                    l1= []
                    for j in i:    
                        l1.append(contar(j))
                    L.append(l1)
                return L
            
            # Función para evaluar si cada categoria y tipo cuentan con los datos para ejecutar pronóstico
            def val_crit3(t):
                L= []
                for i in t:
                    if i[0][0] == True:
                        if sum(i[1]) > 0:
                            L.append(i[1])
                        else:
                            L.append([False])
                    else:
                        L.append([False])
                return(L)
            
            l.append(category_df)
            crit1 = [ val_crit1(i) for i in l ]
            crit2 = crit2(l)
            crits = [ (i, j) for (i, j) in zip(crit1, crit2) ]
            #crits = [([True], [True, False, False]), ([True], [True, False, False, False]), ([False], [False]), ([True], [False, False, False, False, False]), ([True], [False, False, False, False, False, False, False, False])]
            crit3 = val_crit3(crits)
            return crit3

        def city_forecast():
            val_city = []
            orders = Orders.objects.all()
            orders = orders.to_dataframe()
            orders['order_date'] = pd.to_datetime(orders['order_date'], format='%Y-%m-%d')
            orders['year'] = orders['order_date'].dt.year
            orders['week'] = orders['order_date'].dt.isocalendar().week
            customer = ClientCatal.objects.all()                
            customer = customer.to_dataframe()
            orders = orders.merge(customer, how='left', on='customer')
            orders = orders.drop(['user_creation_x', 'date_creation_x', 'user_update_x', 'date_update_x','id_y', 'id_y', 'user_creation_y', 'date_creation_y', 'user_update_y', 'date_update_y'], axis=1)
            city_week = orders.groupby(['week', 'city'])['total'].sum().reset_index()
            city = city_week.drop_duplicates(subset=['city'])

            
            if len(city) > 1:
                city_group_week = [i for n, i in city_week.groupby(pd.Grouper(key='city'))]
                cat_for = category_forecast(city_group_week)
                
                if len(cat_for) > 1:
                    msg = 'Se ha generado el pronóstico exitosamente'
                    val_city.append(msg)
                    forecast_city = []
                    city_table = ForecastCity.objects.all()
                    for i in city_table:
                        forecast_city.append(i.toJSON())   
                        val_city.append(forecast_city)
                else:
                    msg = 'Se ha generado el pronóstico exitosamente'
                    val_city.append(msg)
                    forecast_city = []
                    city_table = ForecastCity.objects.all()
                    for i in city_table:
                        forecast_city.append(i.toJSON())
                        val_city.append(forecast_city)
            else:
                msg = 'Usted no puede ejecutar filtro por ciudad'
                val_city.append(msg)
            return val_city

            '''zone_week = orders.groupby(['week', 'zone'])['total'].sum().reset_index()
            zone = zone_week.drop_duplicates(subset=['zone'])
            if len(zone) > 1:
                zone_group_week = [i for n, i in zone_week.groupby(pd.Grouper(key='zone'))]
                l.append(zone_group_week)
            else:
                msg = 'Usted no puede ejecutar filtro por Zona'
                l.append(msg)

            advisor_week = orders.groupby(['week', 'advisor'])['total'].sum().reset_index()
            advisor = advisor_week.drop_duplicates(subset=['advisor'])
            if len(advisor) > 1:
                advisor_group_week = [i for n, i in advisor_week.groupby(pd.Grouper(key='advisor'))]
                l.append(advisor_group_week)
            else:
                msg = 'Usted no puede ejecutar filtro por asesor'
                l.append(msg)

            category_week = orders.groupby(['week', 'category'])['total'].sum().reset_index()
            category = category_week.drop_duplicates(subset=['category'])
            if len(category) > 1:
                category_group_week = [i for n, i in category_week.groupby(pd.Grouper(key='category'))]
                l.append(category_group_week)
            
            customer_week = orders.groupby(['week', 'customer'])['total'].sum().reset_index()
            customer = customer_week.drop_duplicates(subset=['customer'])
            if len(customer) > 1:
                customer_group_week = [i for n, i in customer_week.groupby(pd.Grouper(key='customer'))]
                l.append(customer_group_week)
                        
            if len(l):
                crit1 = [ val_crit1(i) for i in l ]
                crit2 = crit2(l)
                crits = [ (i, j) for (i, j) in zip(crit1, crit2) ]
                #crits = [([True], [True, False, False]), ([True], [True, False, False, False]), ([False], [False]), ([True], [False, False, False, False, False]), ([True], [False, False, False, False, False, False, False, False])]
                crit3 = val_crit3(crits)
            return(crit3)'''

        try:
            action = request.POST['action']
            if action == 'get_data':
                planning = get_planning()
                if len(planning) > 2:
                    data['msg'] = planning[0]
                    data['last_sale'] = planning[1]
                    data['last_planning'] = planning[2]
                    data['total_week'] = planning[3]
                else:
                    data['msg'] = planning[0]
                    data['total_week'] = planning[1]
            
            elif action == 'get_forecast':
                forecast = get_forecast()
                if len(forecast) == 1:
                    data['msg'] = forecast[0]
                else:
                    forecast_table = [ i.toJSON() for i in forecast[1][0] ]
                    data['msg'] = forecast[0]
                    data['forecast_table'] = forecast_table
                    #data['forecast_graf'] = forecast[1][1]

            elif action == 'get_forecast_city':
                city_forecast = city_forecast()
                if len(city_forecast) > 1:
                    data['msg'] = city_forecast[0]
                    data['table_city'] = city_forecast[1]
                else:
                    data['msg'] = city_forecast[0]

            elif action == 'forecast_zone':
                if len(crit3[1]) == 1:
                    data = 'No puede ejecutar este filtro'    
                    json.dumps(data)
                elif len(crit3[1]) > 1:
                    data = 'Ejecutar pronostico'
                    json.dumps(data)
            elif action == 'forecast_advisor':
                if len(crit3[2]) == 1:
                    data = 'No puede ejecutar este filtro'    
                    json.dumps(data)
                elif len(crit3[2]) > 1:
                    data = 'Ejecutar pronostico'
                    json.dumps(data)
            elif action == 'forecast_catcust':
                if len(crit3[3]) == 1:
                    data = 'No puede ejecutar este filtro'    
                    json.dumps(data)
                elif len(crit3[3]) > 1:
                    data = 'Ejecutar pronostico'
                    json.dumps(data)
            elif action == 'forecast_customer':
                if len(crit3[4]) == 1:
                    data = 'No puede ejecutar este filtro'    
                    json.dumps(data)
                elif len(crit3[4]) > 1:
                    data = 'Ejecutar pronostico'
                    json.dumps(data)
            else:
                data['error'] = 'No se encontraron resultados'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

''' Vista para planificación de actividades compras'''
class PurchasePlanActivitiesView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'planeacion/plan_act_compras.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

''' Vista para novedades de compra'''
class PurchaseNewsView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'planeacion/novedades_compras.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

''' Vista ventana cartera de proveedores'''
class CarteraSuppView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = SupplierDebt
    template_name = 'planeacion/cartera_proveedores.html'

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

''' Vista para la ventana inventario'''
class InventoryListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Inventory
    template_name = 'planeacion/inventario.html'

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
