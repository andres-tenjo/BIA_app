# Python libraries
import json
from datetime import datetime, date, timedelta
import time
from pandas import pandas as pd

# Modelos BIA
from apps.Modelos.Several_func import *
from apps.Modelos.Update_Balances import *
from apps.Modelos.Parameters import *
from apps.Modelos.Information_Inactivation import *

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
from .resources import *
from apps.modulo_comercial.models import *
from apps.modulo_logistica.models import *
from apps.modulo_compras.models import *
from apps.functions_views import *
from .api.serializers import *


################################################################################################
############################### VISTAS DEL MODULO PARAMETRIZACIÓN ##############################
################################################################################################

#################################################################################################
# 1. PARAMETRIZACIÓN EMPRESA (CREAR Y EDITAR EMPRESA)
#################################################################################################
''' 1.1 Vista crear empresa'''
class clsCrearEmpresaViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = clsPerfilEmpresaMdl
    form_class = clsCrearEmpresaFrm
    template_name = 'modulo_configuracion/crear_empresa.html'
    success_url = reverse_lazy('configuracion:crear_empresa')
    url_redirect = success_url
    permission_required = 'bia_add_company'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'slcFiltrarCiudadesjsn':
                jsnData = [{'id': '', 'text': '----------'}]
                for i in clsCiudadesMdl.objects.filter(department_id=request.POST['intId']):
                    jsnData.append({'id': i.id, 'text': i.city_name})
            elif action == 'frmCrearEmpresajsn':
                frmCrearEmpresa = clsCrearEmpresaFrm(request.POST)
                jsnData = frmCrearEmpresa.save()
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
            
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = reverse_lazy("configuracion:vista_usuarios")
        context['title'] = 'Parametrizacion de empresa'
        context['action'] = 'frmCrearEmpresajsn'
        context['queryset'] = clsPerfilEmpresaMdl.objects.all()
        return context

''' 1.2 Vista editar empresa'''
class clsEditarEmpresaViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = clsPerfilEmpresaMdl
    form_class = clsCrearEmpresaFrm
    template_name = 'modulo_configuracion/editar_empresa.html'
    success_url = reverse_lazy('configuracion:crear_empresa')
    url_redirect = success_url
    permission_required = 'bia_change_company'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'slcFiltrarCiudadesjsn':
                jsnData = [{'id': '', 'text': '----------'}]
                for i in clsCiudadesMdl.objects.filter(department_id=request.POST['intId']):
                    jsnData.append({'id': i.id, 'text': i.city_name})
            elif action == 'jsnEditar':
                form = self.get_form()
                jsnData = form.save()
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = self.success_url
        context['title'] = 'Edición de perfil empresarial'
        context['action'] = 'jsnEditar'
        return context

#################################################################################################
# 2. PARAMETRIZACIÓN USUARIOS (MENÚ DE USUARIOS)
#################################################################################################
''' 2.1 Vista menú usuarios, grupos y permisos'''
class clsMenuUsuarioViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/user_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options_title'] = 'Crear grupos y permisos'
        context['options_url'] = reverse_lazy('usuarios:crear_grupos_usuarios')
        context['create_title'] = 'Crear usuario'
        context['create_url'] = reverse_lazy('usuarios:crear_usuarios')
        context['search_title'] = 'Buscar usuario'
        context['search_url'] = reverse_lazy('usuarios:listar_usuarios')
        return context

#################################################################################################
# 3. PARAMETRIZACIÓN CATÁLOGO DE PRODUCTOS (MENÚ, OPCIONES CATALOGO, CRUD, IMPORTAR Y EXPORTAR)
#################################################################################################
''' 3.1 Vista menú catálogo de productos'''
class clsMenuCatalogoProductosViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/catalogo_productos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options_title'] = 'Opciones de catálogo'
        context['options_url'] = reverse_lazy('configuracion:opciones_producto')
        context['create_title'] = 'Crear producto'
        context['create_url'] = reverse_lazy('configuracion:crear_producto')
        context['search_title'] = 'Ver productos'
        context['search_url'] = reverse_lazy('configuracion:listar_productos')
        return context

''' 3.2 Vista opciones producto'''
class clsOpcionesCatalogoProductoViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/opciones_catalogo_productos.html'

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
        context['create_url'] = reverse_lazy('configuracion:crear_producto')
        context['list_url'] = reverse_lazy("configuracion:listar_productos")
        context['frmProductCat'] = clsCrearCategoriaProductoFrm()
        context['frmProductSub'] = clsCrearSubcategoriaProductoFrm()
        context['frmUdcProd'] = clsCrearUnidadCompraFrm()
        context['frmUdvProd'] = clsCrearUnidadVentaFrm()
        return context

''' 3.3 Vista para exportar plantilla de subcategorías de producto'''
class clsExportarPlantillaSubcategoríaProductoViw(APIView):

    def get(self, request):
        lstCeldasExcel = ['A1', 'B1']
        lstComentariosExcel = [
            'Ingresa el nombre de la subcategoría de producto',
            'Las unidades de venta ya las creaste, en la hoja de este archivo llamada "CATEGORIA_PRODUCTO" las encontrarás, digita el número que aparece en la primer columna, por ejemplo: primer columna 1, segunda columna Alimentos, si es alimentos digitas el 1',
        ]
        qrsCategoriaProducto = clsCategoriaProductoMdl.objects.filter(state='AC')
        srlCategoriaProducto = clsCategoriaProductoMdlSerializer(qrsCategoriaProducto, many=True)
        dtfCategoriaProducto = pd.DataFrame(srlCategoriaProducto.data)
        dtfCategoriaProducto = dtfCategoriaProducto.rename(columns={'id':'Nº', 'product_cat':'Categoría'})
        dtfPlantillaSubcategoriaProductos = pd.DataFrame(
            {
                'Nombre subcategoría':[],
                'Categoría producto':[]
            }, 
            index = [i for i in range (0, 0)]
            )
        lstNombresColumnasPlantilla = list(dtfPlantillaSubcategoriaProductos.columns.values)
        lstTotalColumnas = [ i for i in range (1, len(lstNombresColumnasPlantilla) + 1) ]
        lstTipoDato = [
            'Alfabético', 
            'Numérico'
            ]
        lstLongitudMaxima = [
            100,
            3
            ]
        lstCaracteresEspeciales = [
            'PERMITE Ñ', 
            'NO PERMITE'
            ]
        lstObservaciones = [
            'Ingresa el nombre de la subcategoría de producto',
            'Ingrese el Nº de la categoría de producto a la que pertenece la subcategoría de la hoja "CATEGORÍA_PRODUCTO"',
            ]
        lstCampoObligatorio = [
            'SI', 
            'SI'
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
        response['Content-Disposition'] = 'attachment; filename="subcategorias_productos.xlsx"'
        with pd.ExcelWriter(response) as writer:
            dtfPlantillaSubcategoriaProductos.to_excel(writer, sheet_name='PLANTILLA', index=False)
            dtfInstructivoPlantilla.to_excel(writer, sheet_name='INSTRUCTIVO', index=False)
            dtfCategoriaProducto.to_excel(writer, sheet_name='CATEGORIA_PRODUCTO', index=False)
            fncAgregarAnchoColumna(writer, False, dtfPlantillaSubcategoriaProductos, 'PLANTILLA') 
            fncAgregarAnchoColumna(writer, True, dtfInstructivoPlantilla, 'INSTRUCTIVO')
            fncAgregarAnchoColumna(writer, True, dtfCategoriaProducto, 'CATEGORIA_PRODUCTO')
            fncAgregarComentarioCeldas(writer, 'PLANTILLA', lstCeldasExcel, lstComentariosExcel)
        return response

''' 3.4 Vista para importar archivo de subcategorias producto'''
class clsImportarSubcategoriaProductoViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/importar_subcategorias_producto.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lstNombresColumnas = [
            'Nombre subcategoría',
            'Categoría producto'
            ]
        tplValidaciones = (
            ((True, 'product_subcat', clsSubcategoriaProductoMdl), (True, 60), (True, 1), (False,)),
            ((False,), (True, 3), (True, 1), (True, clsCategoriaProductoMdl))
            )
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCargarArchivojsn':
                filSubcategoriasProducto = request.FILES['file']
                if str(filSubcategoriasProducto).endswith('.xlsx'):
                    dtfSubcategorias = pd.read_excel(filSubcategoriasProducto)
                    dtfSubcategorias = dtfSubcategorias.fillna(0)
                    lstValidarImportacion = [ fncValidarImportacionlst(dtfSubcategorias, i, j) for (i, j) in zip(lstNombresColumnas, tplValidaciones) ]
                    lstValidarImportacion = [ i for n in lstValidarImportacion for i in n ]
                    if len(lstValidarImportacion):
                        jsnSubcategoriaProducto = dtfSubcategorias.to_json(orient="split")
                        jsnData['jsnSubcategoriaProducto'] = jsnSubcategoriaProducto
                        jsnData['lstValidarImportacion'] = lstValidarImportacion
                        jsnData['strErrorArchivo'] = 'El archivo presenta errores, desea descargarlos?'
                        response = JsonResponse(jsnData, safe=False)
                    else:
                        with transaction.atomic():
                            for i in (dtfSubcategorias.values.tolist()):
                                clsSubcategoriaProductoMdl.objects.create(
                                product_subcat = i[0],
                                product_cat_id = int(i[1])
                                )
                        jsnData['success'] = '¡Se ha cargado el archivo a su base de datos con éxito!'
                        response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['error'] = 'Compruebe el formato del archivo'
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'btnArchivoErroresjsn':
                jsnSubcategoriaProducto = request.POST['jsnSubcategoriaProducto']
                dtfSubcategorias = pd.read_json(jsnSubcategoriaProducto, orient='split')
                lstValidarImportacion = json.loads(request.POST['lstValidarImportacion'])
                lstErroresCeldas = list( dict.fromkeys([ i[1] for i in lstValidarImportacion ]) )
                dtfSubcategorias = fncAgregarErroresDataframedtf(dtfSubcategorias, lstValidarImportacion, lstErroresCeldas)
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="subcategoria_productos.xlsx"'
                with pd.ExcelWriter(response) as writer:
                    dtfSubcategorias.to_excel(writer, sheet_name='VALIDAR', index=False)
                    fncAgregarFormatoColumnasError(writer, lstValidarImportacion, 'VALIDAR', lstNombresColumnas)
                    fncAgregarAnchoColumna(writer, False, dtfSubcategorias, 'VALIDAR')
        except Exception as e:
            jsnData['error'] = str(e)
            response = JsonResponse(jsnData, safe=False)
        return response

''' 3.5 Vista para exportar plantilla de productos'''
class clsExportarPlantillaProductosViw(APIView):

    def get(self, request):
        lstCeldasExcel = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1', 'M1', 'N1']
        lstComentariosExcel = [
            'Ingrersa el nombre y una descripción breve del producto por ejemplo: Coca cola pet x 12',
            'Este espacio solo permite el ingreso de números, digita el código de barras del producto',
            'Ingresa la marca de tu producto',
            'Como ya creaste las categorias antes de descargar esta plantilla, en este archivo se encuentra la hoja con el nombre "CATEGORIA" donde encontraras las que ya has creado, ahí puedes validar a que número corresponde y solo ingresas ese número (es el numero en la primer columna). Por ejemplo la categoria se llama Bebidas y el numero que aparece al inicio es 1, digitas 1 en este campo',
            'Como ya creaste las subcategorias antes de descargar esta plantilla, en este archivo se encuentra la hoja con el nombre "SUBCATEGORIA" allí encontraras las que ya has creado, podrás validar a que número corresponde y solo ingresas ese número (es el numero en la primer columna)',
            'Las unidades de compra ya las creaste, las encontrarás en la hoja llamada "UNIDAD_COMPRA", digita el número que aparece en la primer columna, por ejemplo: primer columna 1, segunda columna Canasta, si es una canasta digitas el 1',
            'Cuantas unidades componen tu unidad de compra, si tu compras al proveedor por canasta de 30 unidades, el valor que debes digitar será 30',
            'Ingresa el valor que pagas a tu proveedor por cada unidad de compra, por ejemplo: si compras por caja de 30 unidades, el valor por cada caja de 30 unidades, si tienes decimales solo ingresa 2 digitos. (Sin el signo $ y sin puntos',
            'Las unidades de venta ya las creaste, en la hoja de este archivo llamada "UNIDAD_VENTA" las encontrarás, digita el número que aparece en la primer columna, por ejemplo: primer columna 1, segunda columna Canasta, si es una canasta digitas el 1',
            'Ingresa la unidad en la que vendes a tus clientes este producto, por ejemplo: si compras por caja de 30 pero vendes por unidad, digitas 1',
            'Aquí digitas el precio de venta que das a tus clientes de acuerdo a tu unidad de venta, si vendes por caja de 30, será este valor, si es por unidad; 1, será el valor de Una unidad. No ingreses el signo pesos ni puntos, si requieres puedes ingresar dos decimales con la coma',
            'Ingresa en numero, el porcentaje de IVA que tiene este producto para la venta, no incluyas el signo %, por ejemplo si es 19%, solo ingresas 19, si no aplica dejas este campo vacio',
            'Si para la venta de tu producto debes incluir otro impuesto adicional al IVA, ingresa en numero el porcentaje del impuesto sin incluir el signo %, por ejemplo 4%, solo ingresas 4,  si no aplica dejas este campo vacio',
            'Ingresa en número de días el tiempo que tu proveedor se toma para entregarte el pedido una vez le envias la solicitud, por ejemplo 5 días, ingresas solo 5'
        ]
        qrsCategoriaProducto = clsCategoriaProductoMdl.objects.filter(state='AC')
        srlCategoriaProducto = clsCategoriaProductoMdlSerializer(qrsCategoriaProducto, many=True)
        dtfCategoriaProducto = pd.DataFrame(srlCategoriaProducto.data)
        dtfCategoriaProducto = dtfCategoriaProducto.rename(columns={'id':'Código', 'product_cat':'Categoría'})
        qrsSubcategoriaPorducto = clsSubcategoriaProductoMdl.objects.filter(state='AC')
        srlSubcategoriaProducto = ProductSubcategorySerializer(qrsSubcategoriaPorducto, many=True)
        dtfSubcategoria = pd.DataFrame(srlSubcategoriaProducto.data)
        dtfSubcategoria = dtfSubcategoria.rename(columns={'id':'Código', 'product_subcat':'Subcategoría'})
        dtfSubcategoria = dtfSubcategoria.drop(['product_cat'], axis=1)
        qrsUnidadCompra = clsUnidadCompraMdl.objects.filter(state='AC')
        srlUnidadCompra = clsUnidadCompraMdlSerializer(qrsUnidadCompra, many=True)
        dtfUnidadCompra = pd.DataFrame(srlUnidadCompra.data)
        dtfUnidadCompra = dtfUnidadCompra.rename(columns={'id':'Código', 'purchase_unit':'Unidad de compra'})
        qrsUnidadVenta = clsUnidadVentaMdl.objects.filter(state='AC')
        srlUnidadVenta = clsUnidadVentaMdlSerializer(qrsUnidadVenta, many=True)
        dtfUnidadVenta = pd.DataFrame(srlUnidadVenta.data)
        dtfUnidadVenta = dtfUnidadVenta.rename(columns={'id':'Código', 'sales_unit':'Unidad de venta'})
        dtfPlantillaProductos = pd.DataFrame(
            {
                'Descripción producto':[],
                'Código de barras':[],
                'Marca':[],
                'Categoría producto':[],
                'Subcategoría producto':[],
                'Unidad de compra':[],
                'Cantidad unidad de compra':[],
                'Precio de compra':[],
                'Unidad de venta':[],
                'Cantidad unidad de venta':[],
                'Precio de venta':[],
                'Iva':[],
                'Otros impuestos':[],
                'Tiempo de entrega proveedor':[],
            }, 
            index = [i for i in range (0, 0)]
            )
        lstNombresColumnasPlantilla = list(dtfPlantillaProductos.columns.values)
        lstTotalColumnas = [ i for i in range (1, len(lstNombresColumnasPlantilla) + 1) ]
        lstTipoDato = [
            'Alfabético', 
            'Numérico',  
            'AlfaNumérico',
            'Numérico', 
            'Numérico', 
            'Numérico', 
            'Numérico', 
            'Decimal', 
            'Numérico', 
            'Numérico', 
            'Decimal', 
            'Decimal', 
            'Decimal', 
            'Numérico'
            ]
        lstLongitudMaxima = [
            100,
            30, 
            100,
            2, 
            2, 
            2, 
            4,
            13, 
            2, 
            4, 
            13,
            2, 
            2, 
            2
            ]
        lstCaracteresEspeciales = [
            'PERMITE Ñ', 'NO PERMITE', 'PERMITE Ñ',
            'NO PERMITE', 'NO PERMITE', 'NO PERMITE', 'NO PERMITE',
            'PERMITE .', 'NO PERMITE', 'NO PERMITE', 'PERMITE .',
            'PERMITE .', 'PERMITE .', 'NO PERMITE'
            ]
        lstObservaciones = [
            'Ingrersa el nombre y una descripción breve del producto por ejemplo: Coca cola pet x 12',
            'Este espacio solo permite el ingreso de números, digita el código de barras del producto',
            'Ingresa la marca de tu producto',
            'Como ya creaste las categorias antes de descargar esta plantilla, en este archivo se encuentra la hoja con el nombre "CATEGORIA" donde encontraras las que ya has creado, ahí puedes validar a que número corresponde y solo ingresas ese número (es el numero en la primer columna). Por ejemplo la categoria se llama Bebidas y el numero que aparece al inicio es 1, digitas 1 en este campo',
            'Como ya creaste las subcategorias antes de descargar esta plantilla, en este archivo se encuentra la hoja con el nombre "SUBCATEGORIA" allí encontraras las que ya has creado, podrás validar a que número corresponde y solo ingresas ese número (es el numero en la primer columna)',
            'Las unidades de compra ya las creaste, las encontrarás en la hoja llamada "UNIDAD_COMPRA", digita el número que aparece en la primer columna, por ejemplo: primer columna 1, segunda columna Canasta, si es una canasta digitas el 1',
            'Cuantas unidades componen tu unidad de compra, si tu compras al proveedor por canasta de 30 unidades, el valor que debes digitar será 30',
            'Ingresa el valor que pagas a tu proveedor por cada unidad de compra, por ejemplo: si compras por caja de 30 unidades, el valor por cada caja de 30 unidades, si tienes decimales solo ingresa 2 digitos. (Sin el signo $ y sin puntos',
            'Las unidades de venta ya las creaste, en la hoja de este archivo llamada "UNIDAD_VENTA" las encontrarás, digita el número que aparece en la primer columna, por ejemplo: primer columna 1, segunda columna Canasta, si es una canasta digitas el 1',
            'Ingresa la unidad en la que vendes a tus clientes este producto, por ejemplo: si compras por caja de 30 pero vendes por unidad, digitas 1',
            'Aquí digitas el precio de venta que das a tus clientes de acuerdo a tu unidad de venta, si vendes por caja de 30, será este valor, si es por unidad; 1, será el valor de Una unidad. No ingreses el signo pesos ni puntos, si requieres puedes ingresar dos decimales con la coma',
            'Ingresa en numero, el porcentaje de IVA que tiene este producto para la venta, no incluyas el signo %, por ejemplo si es 19%, solo ingresas 19, si no aplica dejas este campo vacio',
            'Si para la venta de tu producto debes incluir otro impuesto adicional al IVA, ingresa en numero el porcentaje del impuesto sin incluir el signo %, por ejemplo 4%, solo ingresas 4,  si no aplica dejas este campo vacio',
            'Ingresa en número de días el tiempo que tu proveedor se toma para entregarte el pedido una vez le envias la solicitud, por ejemplo 5 días, ingresas solo 5'
            ]
        lstCampoObligatorio = [
            'SI', 'NO', 'SI',
            'SI', 'SI', 'SI', 'SI',
            'SI', 'SI', 'SI', 'SI',
            'NO', 'NO', 'SI'
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
        response['Content-Disposition'] = 'attachment; filename="catalogo_productos.xlsx"'
        with pd.ExcelWriter(response) as writer:
            dtfPlantillaProductos.to_excel(writer, sheet_name='PLANTILLA', index=False)
            dtfInstructivoPlantilla.to_excel(writer, sheet_name='INSTRUCTIVO', index=False)
            dtfCategoriaProducto.to_excel(writer, sheet_name='CATEGORIA', index=False)
            dtfSubcategoria.to_excel(writer, sheet_name='SUBCATEGORIA', index=False)
            dtfUnidadCompra.to_excel(writer, sheet_name='UNIDAD_COMPRA', index=False)
            dtfUnidadVenta.to_excel(writer, sheet_name='UNIDAD_VENTA', index=False)
            fncAgregarAnchoColumna(writer, False, dtfPlantillaProductos, 'PLANTILLA') 
            fncAgregarAnchoColumna(writer, True, dtfInstructivoPlantilla, 'INSTRUCTIVO')
            fncAgregarAnchoColumna(writer, True, dtfCategoriaProducto, 'CATEGORIA')
            fncAgregarAnchoColumna(writer, True, dtfSubcategoria, 'SUBCATEGORIA')
            fncAgregarAnchoColumna(writer, True, dtfUnidadCompra, 'UNIDAD_COMPRA')
            fncAgregarAnchoColumna(writer, True, dtfUnidadVenta, 'UNIDAD_VENTA')
            fncAgregarComentarioCeldas(writer, 'PLANTILLA', lstCeldasExcel, lstComentariosExcel)
        return response

''' 3.6 Vista para importar archivo de productos'''
class clsImportarCatalogoProductosViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/importar_catalogo_productos.html'
    
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
                                    del_time = int(i[13])
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
                                    del_time = int(i[13])
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

''' 3.7 Vista para crear producto'''
class clsCrearProductoViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = clsCatalogoProductosMdl
    form_class = clsCrearProductoFrm
    template_name = 'modulo_configuracion/crear_producto.html'
    success_url = reverse_lazy("configuracion:listar_productos")
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
        context['create_url'] = reverse_lazy('configuracion:crear_producto')
        context['list_url'] = self.success_url
        context['action'] = 'frmCrearProductojsn'
        context['frmProductCat'] = clsCrearCategoriaProductoFrm()
        context['frmProductSub'] = clsCrearSubcategoriaProductoFrm()
        context['frmUdcProd'] = clsCrearUnidadCompraFrm()
        context['frmUdvProd'] = clsCrearUnidadVentaFrm()
        return context

''' 3.8 Vista para listar e inactivar productos'''
class clsListarCatalogoProductosViw(LoginRequiredMixin, ListView):
    model = clsCatalogoProductosMdl
    template_name = 'modulo_configuracion/listar_productos.html'

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
                    # with transaction.atomic():
                    #     qrsAjusteInventario = clsEntradasAlmacenMdl()
                    #     qrsAjusteInventario.identification= clsCatalogoProveedoresMdl.objects.get(pk= 1)
                    #     qrsAjusteInventario.total_cost= dtfEntrada['total_cost'].sum()
                    #     qrsAjusteInventario.store= clsCatalogoBodegasMdl.objects.get(id= 1)
                    #     qrsAjusteInventario.crossing_doc= 'OC-01'
                    #     qrsAjusteInventario.condition= 'CA'
                    #     qrsAjusteInventario.save()
                    #     for i in dtfEntrada.to_records(index= False):
                    #         qrsDetalleAjuste = clsDetalleEntradaAlmacen()
                    #         qrsDetalleAjuste.doc_number = clsEntradasAlmacenMdl.objects.get(id= 4)
                    #         qrsDetalleAjuste.product_code = clsCatalogoProductosMdl.objects.get(id= i[0])                            
                    #         qrsDetalleAjuste.quantity = i[2]
                    #         qrsDetalleAjuste.unitary_cost= i[1]
                    #         qrsDetalleAjuste.total_cost= i[5]
                    #         qrsDetalleAjuste.batch = i[3]
                    #         qrsDetalleAjuste.expiration_date= datetime(2021, 3, 10)
                    #         qrsDetalleAjuste.state= i[4]
                    #         qrsDetalleAjuste.save()
                    bolEvaluacion= fncInactivarProductotpl(qrsCatalogoProductos.id)
                    if bolEvaluacion== True:
                        qrsCatalogoProductos.state = "IN"
                        qrsCatalogoProductos.save()
                    else:
                        print(bolEvaluacion)
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
        context['create_url'] = reverse_lazy('configuracion:crear_producto')
        context['list_url'] = reverse_lazy("configuracion:listar_productos")
        context['options_url'] = reverse_lazy('configuracion:opciones_producto')
        return context

''' 3.9 Vista para editar producto'''
class clsEditarProductoViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = clsCatalogoProductosMdl
    form_class = clsCrearProductoFrm
    template_name = 'modulo_configuracion/crear_producto.html'
    success_url = reverse_lazy("configuracion:listar_productos")
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

''' 3.10 Vista para exportar catálogo de productos'''
class clsExportarCatalogoProductosViw(APIView):

    def get(self, request):
        qrsCatalogoProductos = clsCatalogoProductosMdl.objects.all()
        srlCatalogoProductos = clsCatalogoProductosMdlSerializer(qrsCatalogoProductos, many=True)
        dtfCatalogoProductos = pd.DataFrame(srlCatalogoProductos.data)
        dtfCatalogoProductos = dtfCatalogoProductos.rename(columns={
            'id':'Código',
            'date_creation': 'Fecha de creación',
            'date_update': 'Fecha de actualización',
            'product_desc': 'Descripción producto',
            'bar_code':'Código de barras',
            'trademark': 'Marca',
            'product_cat':'Categoría',
            'product_subcat': 'Subcategoría producto',
            'purchase_unit': 'Unidad de compra',
            'quantity_pu': 'Cantidad unidad de compra',
            'cost_pu': 'Precio de compra',
            'sales_unit': 'Unidad de venta',
            'quantity_su': 'Cantidad unidad de venta',
            'full_sale_price': 'Precio de venta',
            'iva': 'Iva',
            'other_tax': 'Otros impuestos',
            'del_time': 'Tiempo de entrega proveedor',
            'state_display': 'Estado'
            })
        lstNombresColumnas = [
            'Código', 
            'Fecha de creación',
            'Fecha de actualización',
            'Descripción producto',
            'Código de barras',
            'Marca',
            'Categoría',
            'Subcategoría producto',
            'Unidad de compra',
            'Cantidad unidad de compra',
            'Precio de compra',
            'Unidad de venta',
            'Cantidad unidad de venta',
            'Precio de venta',
            'Iva',
            'Otros impuestos',
            'Tiempo de entrega proveedor',
            'Estado'
            ]
        dtfCatalogoProductos =dtfCatalogoProductos.reindex(columns=lstNombresColumnas)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="catalogo_productos.xlsx"'
        with pd.ExcelWriter(response) as writer:
            dtfCatalogoProductos.to_excel(writer, sheet_name='CATALOGO_PRODUCTOS', index=False)
            fncAgregarAnchoColumna(writer, True, dtfCatalogoProductos, 'CATALOGO_PRODUCTOS')
        return response

''' 3.11 Vista menú listas de precios'''
class clsMenuListasPreciosViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/lista_precios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options_title'] = 'Opciones'
        context['options_url'] = reverse_lazy('configuracion:carga_masiva_listas_precios')
        context['create_title'] = 'Crear lista de precios'
        context['create_url'] = reverse_lazy('configuracion:crear_lista_precios')
        context['search_title'] = 'Ver listas de precios'
        context['search_url'] = reverse_lazy('configuracion:ver_lista_precios')
        return context

''' 3.12 Vista para carga masiva de listas de precios'''
class clsCargaMasivaListasPreciosViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/carga_masiva_listas_precios.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lstNombresColumnas = [
            'Nombre subcategoría',
            'Categoría producto'
            ]
        tplValidaciones = (
            ((True, 'product_subcat', clsSubcategoriaProductoMdl), (True, 60), (True, 1), (False,)),
            ((False,), (True, 3), (True, 1), (True, clsCategoriaProductoMdl))
            )
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCargarArchivojsn':
                filSubcategoriasProducto = request.FILES['file']
                if str(filSubcategoriasProducto).endswith('.xlsx'):
                    dtfSubcategorias = pd.read_excel(filSubcategoriasProducto)
                    dtfSubcategorias = dtfSubcategorias.fillna(0)
                    lstValidarImportacion = [ fncValidarImportacionlst(dtfSubcategorias, i, j) for (i, j) in zip(lstNombresColumnas, tplValidaciones) ]
                    lstValidarImportacion = [ i for n in lstValidarImportacion for i in n ]
                    if len(lstValidarImportacion):
                        jsnSubcategoriaProducto = dtfSubcategorias.to_json(orient="split")
                        jsnData['jsnSubcategoriaProducto'] = jsnSubcategoriaProducto
                        jsnData['lstValidarImportacion'] = lstValidarImportacion
                        jsnData['strErrorArchivo'] = 'El archivo presenta errores, desea descargarlos?'
                        response = JsonResponse(jsnData, safe=False)
                    else:
                        with transaction.atomic():
                            for i in (dtfSubcategorias.values.tolist()):
                                clsSubcategoriaProductoMdl.objects.create(
                                product_subcat = i[0],
                                product_cat_id = int(i[1])
                                )
                        jsnData['success'] = '¡Se ha cargado el archivo a su base de datos con éxito!'
                        response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['error'] = 'Compruebe el formato del archivo'
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'btnArchivoErroresjsn':
                jsnSubcategoriaProducto = request.POST['jsnSubcategoriaProducto']
                dtfSubcategorias = pd.read_json(jsnSubcategoriaProducto, orient='split')
                lstValidarImportacion = json.loads(request.POST['lstValidarImportacion'])
                lstErroresCeldas = list( dict.fromkeys([ i[1] for i in lstValidarImportacion ]) )
                dtfSubcategorias = fncAgregarErroresDataframedtf(dtfSubcategorias, lstValidarImportacion, lstErroresCeldas)
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="subcategoria_productos.xlsx"'
                with pd.ExcelWriter(response) as writer:
                    dtfSubcategorias.to_excel(writer, sheet_name='VALIDAR', index=False)
                    fncAgregarFormatoColumnasError(writer, lstValidarImportacion, 'VALIDAR', lstNombresColumnas)
                    fncAgregarAnchoColumna(writer, False, dtfSubcategorias, 'VALIDAR')
        except Exception as e:
            jsnData['error'] = str(e)
            response = JsonResponse(jsnData, safe=False)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

''' 3.13 Vista para exportar plantilla de lista de precios'''
class clsExportarPlantillaListaPreciosViw(APIView):

    def get(self, request):
        lstCeldasExcel = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1', 'M1', 'N1']
        lstComentariosExcel = [
            'Ingrersa el nombre y una descripción breve del producto por ejemplo: Coca cola pet x 12',
            'Este espacio solo permite el ingreso de números, digita el código de barras del producto',
            'Ingresa la marca de tu producto',
            'Como ya creaste las categorias antes de descargar esta plantilla, en este archivo se encuentra la hoja con el nombre "CATEGORIA" donde encontraras las que ya has creado, ahí puedes validar a que número corresponde y solo ingresas ese número (es el numero en la primer columna). Por ejemplo la categoria se llama Bebidas y el numero que aparece al inicio es 1, digitas 1 en este campo',
            'Como ya creaste las subcategorias antes de descargar esta plantilla, en este archivo se encuentra la hoja con el nombre "SUBCATEGORIA" allí encontraras las que ya has creado, podrás validar a que número corresponde y solo ingresas ese número (es el numero en la primer columna)',
            'Las unidades de compra ya las creaste, las encontrarás en la hoja llamada "UNIDAD_COMPRA", digita el número que aparece en la primer columna, por ejemplo: primer columna 1, segunda columna Canasta, si es una canasta digitas el 1',
            'Cuantas unidades componen tu unidad de compra, si tu compras al proveedor por canasta de 30 unidades, el valor que debes digitar será 30',
            'Ingresa el valor que pagas a tu proveedor por cada unidad de compra, por ejemplo: si compras por caja de 30 unidades, el valor por cada caja de 30 unidades, si tienes decimales solo ingresa 2 digitos. (Sin el signo $ y sin puntos',
            'Las unidades de venta ya las creaste, en la hoja de este archivo llamada "UNIDAD_VENTA" las encontrarás, digita el número que aparece en la primer columna, por ejemplo: primer columna 1, segunda columna Canasta, si es una canasta digitas el 1',
            'Ingresa la unidad en la que vendes a tus clientes este producto, por ejemplo: si compras por caja de 30 pero vendes por unidad, digitas 1',
            'Aquí digitas el precio de venta que das a tus clientes de acuerdo a tu unidad de venta, si vendes por caja de 30, será este valor, si es por unidad; 1, será el valor de Una unidad. No ingreses el signo pesos ni puntos, si requieres puedes ingresar dos decimales con la coma',
            'Ingresa en numero, el porcentaje de IVA que tiene este producto para la venta, no incluyas el signo %, por ejemplo si es 19%, solo ingresas 19, si no aplica dejas este campo vacio',
            'Si para la venta de tu producto debes incluir otro impuesto adicional al IVA, ingresa en numero el porcentaje del impuesto sin incluir el signo %, por ejemplo 4%, solo ingresas 4,  si no aplica dejas este campo vacio',
            'Ingresa en número de días el tiempo que tu proveedor se toma para entregarte el pedido una vez le envias la solicitud, por ejemplo 5 días, ingresas solo 5'
        ]
        qrsCategoriaProducto = clsCategoriaProductoMdl.objects.filter(state='AC')
        srlCategoriaProducto = clsCategoriaProductoMdlSerializer(qrsCategoriaProducto, many=True)
        dtfCategoriaProducto = pd.DataFrame(srlCategoriaProducto.data)
        dtfCategoriaProducto = dtfCategoriaProducto.rename(columns={'id':'Código', 'product_cat':'Categoría'})
        qrsSubcategoriaPorducto = clsSubcategoriaProductoMdl.objects.filter(state='AC')
        srlSubcategoriaProducto = ProductSubcategorySerializer(qrsSubcategoriaPorducto, many=True)
        dtfSubcategoria = pd.DataFrame(srlSubcategoriaProducto.data)
        dtfSubcategoria = dtfSubcategoria.rename(columns={'id':'Código', 'product_subcat':'Subcategoría'})
        dtfSubcategoria = dtfSubcategoria.drop(['product_cat'], axis=1)
        qrsUnidadCompra = clsUnidadCompraMdl.objects.filter(state='AC')
        srlUnidadCompra = clsUnidadCompraMdlSerializer(qrsUnidadCompra, many=True)
        dtfUnidadCompra = pd.DataFrame(srlUnidadCompra.data)
        dtfUnidadCompra = dtfUnidadCompra.rename(columns={'id':'Código', 'purchase_unit':'Unidad de compra'})
        qrsUnidadVenta = clsUnidadVentaMdl.objects.filter(state='AC')
        srlUnidadVenta = clsUnidadVentaMdlSerializer(qrsUnidadVenta, many=True)
        dtfUnidadVenta = pd.DataFrame(srlUnidadVenta.data)
        dtfUnidadVenta = dtfUnidadVenta.rename(columns={'id':'Código', 'sales_unit':'Unidad de venta'})
        dtfPlantillaProductos = pd.DataFrame(
            {
                'Descripción producto':[],
                'Código de barras':[],
                'Marca':[],
                'Categoría producto':[],
                'Subcategoría producto':[],
                'Unidad de compra':[],
                'Cantidad unidad de compra':[],
                'Precio de compra':[],
                'Unidad de venta':[],
                'Cantidad unidad de venta':[],
                'Precio de venta':[],
                'Iva':[],
                'Otros impuestos':[],
                'Tiempo de entrega proveedor':[],
            }, 
            index = [i for i in range (0, 0)]
            )
        lstNombresColumnasPlantilla = list(dtfPlantillaProductos.columns.values)
        lstTotalColumnas = [ i for i in range (1, len(lstNombresColumnasPlantilla) + 1) ]
        lstTipoDato = [
            'Alfabético', 
            'Numérico',  
            'AlfaNumérico',
            'Numérico', 
            'Numérico', 
            'Numérico', 
            'Numérico', 
            'Decimal', 
            'Numérico', 
            'Numérico', 
            'Decimal', 
            'Decimal', 
            'Decimal', 
            'Numérico'
            ]
        lstLongitudMaxima = [
            100,
            30, 
            100,
            2, 
            2, 
            2, 
            4,
            13, 
            2, 
            4, 
            13,
            2, 
            2, 
            2
            ]
        lstCaracteresEspeciales = [
            'PERMITE Ñ', 'NO PERMITE', 'PERMITE Ñ',
            'NO PERMITE', 'NO PERMITE', 'NO PERMITE', 'NO PERMITE',
            'PERMITE .', 'NO PERMITE', 'NO PERMITE', 'PERMITE .',
            'PERMITE .', 'PERMITE .', 'NO PERMITE'
            ]
        lstObservaciones = [
            'Ingrersa el nombre y una descripción breve del producto por ejemplo: Coca cola pet x 12',
            'Este espacio solo permite el ingreso de números, digita el código de barras del producto',
            'Ingresa la marca de tu producto',
            'Como ya creaste las categorias antes de descargar esta plantilla, en este archivo se encuentra la hoja con el nombre "CATEGORIA" donde encontraras las que ya has creado, ahí puedes validar a que número corresponde y solo ingresas ese número (es el numero en la primer columna). Por ejemplo la categoria se llama Bebidas y el numero que aparece al inicio es 1, digitas 1 en este campo',
            'Como ya creaste las subcategorias antes de descargar esta plantilla, en este archivo se encuentra la hoja con el nombre "SUBCATEGORIA" allí encontraras las que ya has creado, podrás validar a que número corresponde y solo ingresas ese número (es el numero en la primer columna)',
            'Las unidades de compra ya las creaste, las encontrarás en la hoja llamada "UNIDAD_COMPRA", digita el número que aparece en la primer columna, por ejemplo: primer columna 1, segunda columna Canasta, si es una canasta digitas el 1',
            'Cuantas unidades componen tu unidad de compra, si tu compras al proveedor por canasta de 30 unidades, el valor que debes digitar será 30',
            'Ingresa el valor que pagas a tu proveedor por cada unidad de compra, por ejemplo: si compras por caja de 30 unidades, el valor por cada caja de 30 unidades, si tienes decimales solo ingresa 2 digitos. (Sin el signo $ y sin puntos',
            'Las unidades de venta ya las creaste, en la hoja de este archivo llamada "UNIDAD_VENTA" las encontrarás, digita el número que aparece en la primer columna, por ejemplo: primer columna 1, segunda columna Canasta, si es una canasta digitas el 1',
            'Ingresa la unidad en la que vendes a tus clientes este producto, por ejemplo: si compras por caja de 30 pero vendes por unidad, digitas 1',
            'Aquí digitas el precio de venta que das a tus clientes de acuerdo a tu unidad de venta, si vendes por caja de 30, será este valor, si es por unidad; 1, será el valor de Una unidad. No ingreses el signo pesos ni puntos, si requieres puedes ingresar dos decimales con la coma',
            'Ingresa en numero, el porcentaje de IVA que tiene este producto para la venta, no incluyas el signo %, por ejemplo si es 19%, solo ingresas 19, si no aplica dejas este campo vacio',
            'Si para la venta de tu producto debes incluir otro impuesto adicional al IVA, ingresa en numero el porcentaje del impuesto sin incluir el signo %, por ejemplo 4%, solo ingresas 4,  si no aplica dejas este campo vacio',
            'Ingresa en número de días el tiempo que tu proveedor se toma para entregarte el pedido una vez le envias la solicitud, por ejemplo 5 días, ingresas solo 5'
            ]
        lstCampoObligatorio = [
            'SI', 'NO', 'SI',
            'SI', 'SI', 'SI', 'SI',
            'SI', 'SI', 'SI', 'SI',
            'NO', 'NO', 'SI'
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
        response['Content-Disposition'] = 'attachment; filename="catalogo_productos.xlsx"'
        with pd.ExcelWriter(response) as writer:
            dtfPlantillaProductos.to_excel(writer, sheet_name='PLANTILLA', index=False)
            dtfInstructivoPlantilla.to_excel(writer, sheet_name='INSTRUCTIVO', index=False)
            dtfCategoriaProducto.to_excel(writer, sheet_name='CATEGORIA', index=False)
            dtfSubcategoria.to_excel(writer, sheet_name='SUBCATEGORIA', index=False)
            dtfUnidadCompra.to_excel(writer, sheet_name='UNIDAD_COMPRA', index=False)
            dtfUnidadVenta.to_excel(writer, sheet_name='UNIDAD_VENTA', index=False)
            fncAgregarAnchoColumna(writer, False, dtfPlantillaProductos, 'PLANTILLA') 
            fncAgregarAnchoColumna(writer, True, dtfInstructivoPlantilla, 'INSTRUCTIVO')
            fncAgregarAnchoColumna(writer, True, dtfCategoriaProducto, 'CATEGORIA')
            fncAgregarAnchoColumna(writer, True, dtfSubcategoria, 'SUBCATEGORIA')
            fncAgregarAnchoColumna(writer, True, dtfUnidadCompra, 'UNIDAD_COMPRA')
            fncAgregarAnchoColumna(writer, True, dtfUnidadVenta, 'UNIDAD_VENTA')
            fncAgregarComentarioCeldas(writer, 'PLANTILLA', lstCeldasExcel, lstComentariosExcel)
        return response

''' 3.14 Vista para crear lista de precios'''
class clsCrearListaPreciosViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = clsCatalogoProductosMdl
    form_class = clsCrearProductoFrm
    template_name = 'modulo_configuracion/crear_lista_precios.html'
    success_url = reverse_lazy("configuracion:ver_lista_precios")
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCrearProductojsn':
                frmCrearProducto = clsCrearProductoFrm(request.POST)
                jsnData = frmCrearProducto.save()
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear lista de precios'
        context['action'] = 'frmCrearListaPreciosjsn'
        
        return context

''' 3.15 Vista para ver lista de precios'''
class clsVerListaPreciosViw(LoginRequiredMixin, ListView):
    model = clsCatalogoProductosMdl
    template_name = 'modulo_configuracion/ver_lista_precios.html'

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
        context['create_url'] = reverse_lazy('configuracion:crear_producto')
        context['list_url'] = reverse_lazy("configuracion:listar_productos")
        context['options_url'] = reverse_lazy('configuracion:opciones_producto')
        return context

#################################################################################################
# 4. PARAMETRIZACIÓN CATÁLOGO DE PROVEEDORES (MENÚ, OPCIONES CATALOGO, CRUD, IMPORTAR Y EXPORTAR)
#################################################################################################
''' 4.1 Vista menú catálogo de proveedores'''
class clsMenuCatalogoProveedoresViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/catalogo_proveedores.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options_title'] = 'Opciones de catálogo'
        context['options_url'] = reverse_lazy('configuracion:opciones_proveedor')
        context['create_title'] = 'Crear proveedor'
        context['create_url'] = reverse_lazy('configuracion:crear_proveedor')
        context['search_title'] = 'Buscar proveedor'
        context['search_url'] = reverse_lazy('configuracion:listar_proveedores')
        return context

''' 4.2 Vista opciones proveedores'''
class clsOpcionesCatalogoProveedoresViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/opciones_catalogo_proveedores.html'

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

''' 4.3 Vista para exportar plantilla de proveedores'''
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

''' 4.4 Vista para importar archivo proveedores'''
class clsImportarCatalogoProveedoresViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/importar_catalogo_proveedores.html'
    
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

''' 4.5 Vista para crear proveedor'''
class clsCrearProveedorViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = clsCatalogoProveedoresMdl
    form_class = clsCrearProveedorFrm
    template_name = 'modulo_configuracion/crear_proveedor.html'
    success_url = reverse_lazy("configuracion:listar_proveedores")
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

''' 4.6 Vista para listar e inactivar proveedores'''
class clsListarCatalogoProveedoresViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = clsCatalogoProveedoresMdl
    template_name = 'modulo_configuracion/listar_proveedores.html'

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

''' 4.7 Vista para editar proveedor'''
class clsEditarProveedorViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = clsCatalogoProveedoresMdl
    form_class = clsCrearProveedorFrm
    template_name = 'modulo_configuracion/crear_proveedor.html'
    success_url = reverse_lazy("configuracion:listar_proveedores")
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

''' 4.8 Vista para exportar catálogo de proveedores'''
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
# 5. PARAMETRIZACIÓN CATÁLOGO DE CLIENTES (MENÚ, OPCIONES CATALOGO, CRUD, IMPORTAR Y EXPORTAR)
#################################################################################################
''' 5.1 Vista menú catálogo de clientes'''
class clsMenuCatalogoClientesViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/catalogo_clientes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options_title'] = 'Opciones de catálogo'
        context['options_url'] = reverse_lazy('configuracion:opciones_cliente')
        context['create_title'] = 'Crear cliente'
        context['create_url'] = reverse_lazy('configuracion:crear_cliente')
        context['search_title'] = 'Buscar cliente'
        context['search_url'] = reverse_lazy('configuracion:listar_clientes')
        return context

''' 5.2 Vista para opciones cliente'''
class clsOpcionesCatalogoClientesViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/opciones_catalogo_clientes.html'

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
        context['create_url'] = reverse_lazy('configuracion:crear_cliente')
        context['list_url'] = reverse_lazy("configuracion:listar_clientes")
        context['frmZone'] = clsCrearZonaClienteFrm()
        context['frmAdvisor'] = clsCrearAsesorComercialFrm()
        return context

''' 5.3 Vista para exportar plantilla clientes'''
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

''' 5.4 Vista para importar archivo clientes'''
class clsImportarCatalogoClientesViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/importar_catalogo_clientes.html'
    
    @method_decorator(csrf_exempt)
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

''' 5.5 Vista para crear cliente'''
class clsCrearClienteViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = clsCatalogoClientesMdl
    form_class = clsCrearClienteFrm
    template_name = 'modulo_configuracion/crear_cliente.html'
    success_url = reverse_lazy("configuracion:listar_clientes")
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
        context['create_url'] = reverse_lazy('configuracion:crear_cliente')
        context['list_url'] = self.success_url
        context['action'] = 'frmCrearClientejsn'
        context['days_list'] = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        context['productCat'] = clsCategoriaProductoMdl.objects.all()
        context['frmClientCat'] = clsCrearCategoriaClienteFrm()
        context['frmZone'] = clsCrearZonaClienteFrm()
        context['frmAdvisor'] = clsCrearAsesorComercialFrm()
        return context

''' 5.6 Vista para listar e inactivar clientes'''
class clsListarCatalogoClientesViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = clsCatalogoClientesMdl
    template_name = 'modulo_configuracion/listar_clientes.html'

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

''' 5.7 Vista para editar cliente'''
class clsEditarClienteViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = clsCatalogoClientesMdl
    form_class = clsCrearClienteFrm
    template_name = 'modulo_configuracion/crear_cliente.html'
    success_url = reverse_lazy("configuracion:listar_clientes")
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

''' 5.8 Vista para exportar catálogo de clientes'''
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

''' 5.9 Vista menú tiempos de entrega'''
class clsMenuTiemposEntregaViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/tiempos_entrega.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Asignar tiempos de entrega'
        context['create_url'] = reverse_lazy('configuracion:crear_tiempos_entrega')
        context['search_title'] = 'Ver tiempos de entrega'
        context['search_url'] = reverse_lazy('configuracion:ver_tiempos_entrega')
        return context

''' 5.10 Vista para asignar tiempos de entrega'''
class clsCrearTiempoEntregaViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = clsCatalogoProductosMdl
    form_class = clsCrearProductoFrm
    template_name = 'modulo_configuracion/crear_tiempo_entrega.html'
    success_url = reverse_lazy("configuracion:ver_tiempo_entrega")
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCrearProductojsn':
                frmCrearProducto = clsCrearProductoFrm(request.POST)
                jsnData = frmCrearProducto.save()
            else:
                jsnData['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear lista de precios'
        context['action'] = 'frmCrearListaPreciosjsn'
        
        return context

''' 5.11 Vista para ver tiempos de entrega'''
class clsVerTiempoEntregaViw(LoginRequiredMixin, ListView):
    model = clsCatalogoProductosMdl
    template_name = 'modulo_configuracion/ver_tiempos_entrega.html'

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
        context['create_url'] = reverse_lazy('configuracion:crear_producto')
        context['list_url'] = reverse_lazy("configuracion:listar_productos")
        context['options_url'] = reverse_lazy('configuracion:opciones_producto')
        return context

#################################################################################################
# 6. PARAMETRIZACIÓN CATÁLOGO DE BODEGAS (MENÚ, OPCIONES CATALOGO, CRUD Y EXPORTAR)
#################################################################################################
''' 6.1 Vista para la ventana catálogo de bodegas'''
class clsMenuCatalogoBodegasViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/catalogo_bodegas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_title'] = 'Crear bodega'
        context['create_url'] = reverse_lazy('configuracion:crear_bodega')
        context['search_title'] = 'Buscar bodega'
        context['search_url'] = reverse_lazy('configuracion:listar_bodegas')
        return context

''' 6.2 Vista para crear bodega'''
class clsCrearBodegaViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = clsCatalogoBodegasMdl
    form_class = clsCatalogoBodegasFrm
    template_name = 'modulo_configuracion/crear_bodega.html'
    success_url = reverse_lazy("configuracion:listar_bodegas")
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
        context['create_url'] = reverse_lazy('configuracion:crear_bodega')
        context['list_url'] = self.success_url
        context['action'] = 'frmCrearBodegajsn'
        return context

''' 6.3 Vista para listar e inactivar bodegas'''
class clsListarCatalogoBodegasViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = clsCatalogoBodegasMdl
    template_name = 'modulo_configuracion/listar_bodegas.html'

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
        context['create_url'] = reverse_lazy('configuracion:crear_bodega')
        context['list_url'] = reverse_lazy('configuracion:listar_bodegas')
        return context

''' 6.4 Vista para editar bodega'''
class clsEditarBodegaViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = clsCatalogoBodegasMdl
    form_class = clsCatalogoBodegasFrm
    template_name = 'modulo_configuracion/crear_bodega.html'
    success_url = reverse_lazy("configuracion:listar_bodegas")
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
        context['create_url'] = reverse_lazy('configuracion:crear_bodega')
        context['list_url'] = self.success_url
        context['action'] = 'frmEditarBodegajsn'
        return context

''' 6.5 Vista para exportar catálogo de bodegas'''
class clsExportarCatalogoBodegasViw(APIView):

    def get(self, request):
        qrsCatalogoBodegas = clsCatalogoBodegasMdl.objects.all()
        srlCatalogoBodegas = clsCatalogoBodegasSerializador(qrsCatalogoBodegas, many=True)
        dtfCatalogoBodegas = pd.DataFrame(srlCatalogoBodegas.data)
        dtfCatalogoBodegas = dtfCatalogoBodegas.rename(columns={
            'id':'Nº',
            'date_creation': 'Fecha de creación',
            'date_update': 'Fecha de actualización',
            'warehouse_name':'Nombre bodega',
            'department': 'Departamento',
            'city': 'Ciudad',
            'warehouse_address': 'Dirección bodega',
            'contact_name': 'Nombre contacto',
            'state_display': 'Estado'
            })
        lstNombresColumnas = [
            'Nº',
            'Fecha de creación',
            'Fecha de actualización',
            'Nombre bodega',
            'Departamento',
            'Ciudad',
            'Dirección bodega',
            'Nombre contacto',
            'Estado'
            ]
        dtfCatalogoBodegas =dtfCatalogoBodegas.reindex(columns=lstNombresColumnas)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="catalogo_bodegas.xlsx"'
        with pd.ExcelWriter(response) as writer:
            dtfCatalogoBodegas.to_excel(writer, sheet_name='CATALOGO_BODEGAS', index=False)
            fncAgregarAnchoColumna(writer, True, dtfCatalogoBodegas, 'CATALOGO_BODEGAS')
        return response

#################################################################################################
# 7. PARAMETRIZACIÓN HISTORICO DE MOVIMIENTOS (IMPORTAR Y EXPORTAR)
#################################################################################################
''' 7.1 Vista para exportar plantilla historico de movimientos'''
class clsExportarPlantillaHistoricoMovimientosViw(APIView):

    def get(self, request):
        lstCeldasPedidos = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1', 'M1', 'N1', 'O1']
        lstComentariosPedidos = [
            'Ingresa la fecha de creación de cada documento 17/05/22',
            'Por favor digita el número del documento creado en el sistema',
            'Según la hoja llamada CATALOGO_CLIENTES ingresa el número de la primer columna de tu cliente',
            'Si con tu cliente manejas crédito digita CR, si te paga contraentrega o anticipado ingresa CO (ingresalo en mayusculas)',
            'Ingresa la fecha en que se entrego la mercancia a tu cliente, ej. 17/05/2022',
            'Digita el número de la ciudad según la hoja de este archivo llamada "CIUDADES" por ejemplo si es Bogotá 167',
            'Ingresa el número de la primer columna del producto según la hoja de este archivo llamada "CATALOGO_PRODUCTOS"',
            'Digita la cantidad del producto que se relacionó de ese producto en el documento',
            'Ingresa el precio unitario de venta, puedes incluir dos decimales separados con una coma ","',
            'Ingresa el subtotal, en este caso es: el precio unitario por la cantidad, puedes incluir dos decimales',
            'Si tu producto tiene IVA por favor ingresa el valor en precio $, por ejemplo 500',
            'Por favor ingresa el descuento en valor $, por ejemplo 5000, puedes incluir decimales',
            'Ingresa el total por producto, (Subtotal + Iva - Descuento), puedes incluir dos decimales',
            'De donde salió el producto, ingresa el numero según la primera columna de la hoja  "CATALOGO_BODEGAS"',
            'De acuerdo al estado del pedido digita CU si esta cumplido o NC si no se ha cumplido (manten las mayusculas)'
        ]
        lstCeldasOrdenesCompra = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1']
        lstComentariosOrdenesCompra = [
            'Ingresa la fecha de creación de cada documento 17/05/22',
            'Por favor digita el número del documento creado en el sistema',
            'Según la hoja llamada CATALOGO_PROVEEDORES ingresa el número de la primer columna de tu proveedor',
            'Ingresa la fecha en que tu proveedor entregó la mercancia, ej. 17/05/2022',
            'Ingresa el número de la primer columna del producto según la hoja de este archivo llamada "CATALOGO_PRODUCTOS"',
            'Digita la cantidad del producto que se relacionó de ese producto en el documento',
            'Ingresa el precio unitario de compra, puedes incluir dos decimales separados con una coma ","',
            'Ingresa el Total, en este caso es: el precio unitario por la cantidad, puedes incluir dos decimales',
            'Donde llegó el producto, ingresa el numero según la primera columna de la hoja  "CATALOGO_BODEGAS"',
            'De acuerdo al estado de la orden digita AB si esta abierta o CU si esta cumplida, (manten las mayusculas)'
        ]
        lstCeldasEntradasAlmacen = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1']
        lstComentariosEntradasAlmacen = [
            'Ingresa la fecha de creación de cada documento 17/05/22',
            'Por favor digita el número del documento creado en el sistema',
            'Según la hoja llamada CATALOGO_PROVEEDORES ingresa el número de la primer columna de tu proveedor',
            'Ingresa el número de la primer columna del producto según la hoja de este archivo llamada "CATALOGO_PRODUCTOS"',
            'Digita la cantidad del producto que se relacionó de ese producto en el documento',
            'Ingresa el precio unitario de compra, puedes incluir dos decimales separados con una coma ","',
            'Ingresa el Total, en este caso es: el precio unitario por la cantidad, puedes incluir dos decimales',
            'Donde llegó el producto, ingresa el numero según la primera columna de la hoja  "CATALOGO_BODEGAS"',
            'Ingresa el N° del documento que valida el movimiento (Orden de compra, Pedido, Obsequio)',
            'De acuerdo al estado del ingreso, digita CA si esta causada o NC si no esta causada, (manten las mayusculas)',
            'Ingresa el lote del producto que entró, si son varios por cada lote es una fila',
            'Si aplica, ingresa la fecha de vencimiento de los productos recibidos, por cada fecha diferente es una fila'
        ]
        lstCeldasSalidasAlmacen = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1', 'M1']
        lstComentariosSalidasAlmacen = [
            'Ingresa la fecha de creación de cada documento 17/05/22',
            'Por favor digita el número del documento creado en el sistema',
            'Según la hoja llamada CATALOGO_CLIENTES ingresa el número de la primer columna de tu cliente',
            'Ingresa el número de la primer columna del producto según la hoja de este archivo llamada "CATALOGO_PRODUCTOS"',
            'Digita la cantidad del producto que se relacionó de ese producto en el documento',
            'Ingresa el precio unitario de venta, puedes incluir dos decimales separados con una coma ","',
            'Por favor ingresa el descuento en valor $, por ejemplo 5000, puedes incluir decimales',
            'Ingresa el Total, en este caso es: el precio unitario por la cantidad menos el descuento, puedes incluir dos decimales',
            'Donde salió el producto, ingresa el numero según la primera columna de la hoja  "CATALOGO_BODEGAS"',
            'Ingresa el N° del documento que valida el movimiento (Orden de compra, Pedido, Obsequio)',
            'De acuerdo al estado de la salida, digita CE si esta cerrada o AN si esta anulada, (manten las mayusculas)',
            'Ingresa el lote del producto que salió, si son varios lotes, por cada lote es una fila ',
            'Si aplica, ingresa la fecha de vencimiento de los productos recibidos, por cada fecha diferente es una fila'
        ]
        lstCeldaAjustesInventario = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
        lstComentariosAjustesInventarios = [
            'Ingresa la fecha de creación de cada documento 17/05/22',
            'Por favor digita el número del documento creado en el sistema',
            'Si el movimiento es una entrada digita EN, si es una salida ingresa SA (manten las mayusculas)',
            'Donde se movió el producto, ingresa el N° correspondiente de la hoja (primer columna): "CATALOGO_BODEGAS"',
            'Ingresa el número de la primer columna del producto según la hoja de este archivo llamada "CATALOGO_PRODUCTOS"',
            'Digita la cantidad del producto que se relacionó de ese producto en el documento',
            'Ingresa el Total, en este caso es: el costo unitario por la cantidad, puedes incluir dos decimales',
            'Ingresa el lote del producto que salió, si son varios lotes, por cada lote es una fila ',
            'Si aplica, ingresa la fecha de vencimiento de los productos recibidos, por cada fecha diferente es una fila'
        ]
        lstCeldaDevolucionesClientes = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
        lstComentariosDevolucionesClientes = [
            'Ingresa la fecha de creación de cada documento 17/05/22',
            'Por favor digita el número del documento creado en el sistema',
            'Según la hoja llamada CATALOGO_CLIENTES ingresa el número de la primer columna de tu cliente',
            'Ingresa el número de la primer columna del producto según la hoja de este archivo llamada "CATALOGO_PRODUCTOS"',
            'Digita la cantidad del producto que se relacionó de ese producto en el documento',
            'Donde ingresó el producto, digita el N° correspondiente de la hoja (primer columna): "CATALOGO_BODEGAS"',
            'Ingresa el lote del producto que salió, si son varios lotes, por cada lote es una fila ',
            'Si aplica, ingresa la fecha de vencimiento de los productos recibidos, por cada fecha diferente es una fila',
            'Ingresa el N° del documento que valida el movimiento (Orden de compra, Pedido, Obsequio, devolución)'
        ]
        lstCeldaDevolucionesProveedores = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
        lstComentariosDevolucionesProveedores = [
            'Ingresa la fecha de creación de cada documento 17/05/22',
            'Por favor digita el número del documento creado en el sistema',
            'Según la hoja llamada CATALOGO_PROVEEDORES ingresa el número de la primer columna de tu proveedor',
            'Ingresa el número de la primer columna del producto según la hoja de este archivo llamada "CATALOGO_PRODUCTOS"',
            'Digita la cantidad del producto que se relacionó de ese producto en el documento',
            'Donde ingresó el producto, digita el N° correspondiente de la hoja (primer columna): "CATALOGO_BODEGAS"',
            'Ingresa el lote del producto que salió, si son varios lotes, por cada lote es una fila ',
            'Si aplica, ingresa la fecha de vencimiento de los productos recibidos, por cada fecha diferente es una fila',
            'Ingresa el N° del documento que valida el movimiento (Orden de compra, Pedido, Obsequio, devolución)'
        ]
        lstCeldaObsequios = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1']
        lstComentariosObsequios = [
            'Ingresa la fecha de creación de cada documento 17/05/22',
            'Por favor digita el número del documento creado en el sistema',
            'Donde salió el producto, digita el N° correspondiente de la hoja (primer columna): "CATALOGO_BODEGAS"',
            'Ingresa el número de la primer columna del producto según la hoja de este archivo llamada "CATALOGO_PRODUCTOS"',
            'Digita la cantidad del producto que se relacionó de ese producto en el documento',
            'Ingresa el Total, en este caso es: el costo unitario por la cantidad, puedes incluir dos decimales',
            'Ingresa el lote del producto que salió, si son varios lotes, por cada lote es una fila ',
            'Si aplica, ingresa la fecha de vencimiento de los productos recibidos, por cada fecha diferente es una fila'
        ]
        lstCeldaTrasladosBodegas = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
        lstComentariosTrasladosBodegas = [
            'Ingresa la fecha de creación de cada documento 17/05/22',
            'Por favor digita el número del documento creado en el sistema',
            'Si el movimiento es una entrada digita EN, si es una salida ingresa SA (manten las mayusculas)',
            'Donde se movió el producto, ingresa el N° correspondiente de la hoja (primer columna): "CATALOGO_BODEGAS"',
            'Ingresa el número de la primer columna del producto según la hoja de este archivo llamada "CATALOGO_PRODUCTOS"',
            'Digita la cantidad del producto que se relacionó de ese producto en el documento',
            'Ingresa el Total, en este caso es: el costo unitario por la cantidad, puedes incluir dos decimales',
            'Ingresa el lote del producto que salió, si son varios lotes, por cada lote es una fila ',
            'Si aplica, ingresa la fecha de vencimiento de los productos recibidos, por cada fecha diferente es una fila'
        ]
        lstCeldaSaldoInicial = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1']
        lstSaldoInicial = [
            'Ingresa la fecha de creación de cada documento 17/05/22',
            'Ingresa el número de la primer columna del producto según la hoja de este archivo llamada "CATALOGO_PRODUCTOS"',
            'Donde esta el producto, digita el N° correspondiente de la hoja (primer columna): "CATALOGO_BODEGAS"',
            'Digita la cantidad del producto que esta en la bodega relacionada',
            'Ingresa el lote del producto que salió, si son varios lotes, por cada lote es una fila ',
            'Si aplica, ingresa la fecha de vencimiento de los productos recibidos, por cada fecha diferente es una fila'
        ]

        qrsProductos = clsCatalogoProductosMdl.objects.all()
        srlProductos = clsCatalogoProductosPlantillajson(qrsProductos, many=True)
        dtfProductos = pd.DataFrame(srlProductos.data)
        dtfProductos = dtfProductos.rename(columns={'id':'Código', 'product_desc':'Descripción producto'})
        qrsProveedores = clsCatalogoProveedoresMdl.objects.all()
        srlProveedores = clsCatalogoProveedoresPlantillajson(qrsProveedores, many=True)
        dtfProveedores = pd.DataFrame(srlProveedores.data)
        dtfProveedores = dtfProveedores.rename(columns={'id':'Código', 'identification':'Nº Identificación', 'supplier_name':'Nombre proveedor'})
        qrsClientes = clsCatalogoClientesMdl.objects.all()
        srlClientes = clsCatalogoClientesPlantillajson(qrsClientes, many=True)
        dtfClientes = pd.DataFrame(srlClientes.data)
        dtfClientes = dtfClientes.rename(columns={'id':'Código', 'identification':'Nº Identificación', 'business_name':'Nombre cliente'})
        qrsBodegas = clsCatalogoBodegasMdl.objects.all()
        srlBodegas = clsCatalogoBodegasPlantillajson(qrsBodegas, many=True)
        dtfBodegas = pd.DataFrame(srlBodegas.data)
        dtfBodegas = dtfBodegas.rename(columns={'id':'Código', 'warehouse_name':'Nombre bodega', 'contact_name':'Responsable'})
        qrsCiudad = clsCiudadesMdl.objects.all()
        srlCiudad = clsCiudadesMdlSerializer(qrsCiudad, many=True)
        dtfCiudad = pd.DataFrame(srlCiudad.data)
        dtfCiudad = dtfCiudad.rename(columns={'id':'Código', 'city_name':'Ciudad'})
        dtfHistoricoPedidos = pd.DataFrame(
            {
                'Fecha de creación':[],
                'Nº Documento':[],
                'Identificación cliente':[],
                'Método de pago':[],
                'Fecha de entrega':[],
                'Ciudad':[],
                'Código producto':[],
                'Cantidad':[],
                'Precio unitario':[],
                'Subtotal':[],
                'Iva':[],
                'Descuento':[],
                'Total':[],
                'Bodega':[],
                'Condición pedido':[],
            }, 
            index = [i for i in range (0, 0)]
            )
        dtfHistoricoOrdenesCompra = pd.DataFrame(
            {
                'Fecha de creación':[],
                'Nº Documento':[],
                'Identificación proveedor':[],
                'Fecha de entrega':[],
                'Código producto':[],
                'Cantidad':[],
                'Precio unitario':[],
                'Precio total':[],
                'Bodega':[],
                'Condición orden compra':[],
            }, 
            index = [i for i in range (0, 0)]
            )       
        dtfHistoricoEntradasAlmacen = pd.DataFrame(
            {
                'Fecha de creación':[],
                'Nº Documento':[],
                'Identificación proveedor':[],
                'Código producto':[],
                'Cantidad':[],
                'Precio unitario':[],
                'Precio total':[],
                'Bodega':[],
                'Documento cruce':[],
                'Condición entrada':[],
                'Lote':[],
                'Fecha de vencimiento':[],
            }, 
            index = [i for i in range (0, 0)]
            )      
        dtfHistoricoSalidasAlmacen = pd.DataFrame(
            {
                'Fecha de creación':[],
                'Nº Documento':[],
                'Identificación cliente':[],
                'Código producto':[],
                'Cantidad':[],
                'Precio unitario':[],
                'Descuento':[],
                'Precio total':[],
                'Bodega':[],
                'Documento cruce':[],
                'Condición salida':[],
                'Lote':[],
                'Fecha de vencimiento':[],
            }, 
            index = [i for i in range (0, 0)]
            )        
        dtfHistoricoAjustesInventario = pd.DataFrame(
            {
                'Fecha de creación':[],
                'Nº Documento':[],
                'Tipo de movimiento':[],
                'Bodega':[],
                'Código producto':[],
                'Cantidad':[],
                'Costo total':[],
                'Lote':[],
                'Fecha de vencimiento':[],
            }, 
            index = [i for i in range (0, 0)]
            )      
        dtfHistoricoDevolucionesClientes = pd.DataFrame(
            {
                'Fecha de creación':[],
                'Nº Documento':[],
                'Identificación cliente':[],
                'Código producto':[],
                'Cantidad':[],
                'Bodega':[],
                'Lote':[],
                'Fecha de vencimiento':[],
                'Documento cruce':[],
            }, 
            index = [i for i in range (0, 0)]
            )       
        dtfHistoricoDevolucionesProveedor = pd.DataFrame(
            {
                'Fecha de creación':[],
                'Nº Documento':[],
                'Identificación proveedor':[],
                'Código producto':[],
                'Cantidad':[],
                'Bodega':[],
                'Lote':[],
                'Fecha de vencimiento':[],
                'Documento cruce':[],
            }, 
            index = [i for i in range (0, 0)]
            )        
        dtfHistoricoObsequios = pd.DataFrame(
            {
                'Fecha de creación':[],
                'Nº Documento':[],
                'Bodega':[],
                'Código producto':[],
                'Cantidad':[],
                'Costo total':[],
                'Lote':[],
                'Fecha de vencimiento':[],
            }, 
            index = [i for i in range (0, 0)]
            )        
        dtfTrasladosBodegas = pd.DataFrame(
            {
                'Fecha de creación':[],
                'Nº Documento':[],
                'Tipo de movimiento':[],
                'Bodega':[],
                'Código producto':[],
                'Cantidad':[],
                'Costo total':[],
                'Lote':[],
                'Fecha de vencimiento':[],
            }, 
            index = [i for i in range (0, 0)]
            )       
        dtfSaldoInicial = pd.DataFrame(
            {
                'Fecha de creación':[],
                'Código producto':[],
                'Bodega':[],
                'Cantidad':[],
                'Lote':[],
                'Fecha de vencimiento':[],
            }, 
            index = [i for i in range (0, 0)]
            )
        lstNombresColumnas = [
            'Fecha de creación',
            'Nº Documento',
            'Identificación cliente',
            'Identificación proveedor',
            'Método de pago',
            'Fecha de entrega',
            'Ciudad',
            'Código producto',
            'Cantidad',
            'Precio unitario',
            'Precio total',
            'Subtotal',
            'Iva',
            'Descuento',
            'Total',
            'Costo total',
            'Bodega',
            'Condición pedido',
            'Condición orden compra',
            'Condición entrada',
            'Condición salida',
            'Documento cruce',
            'Lote',
            'Fecha de vencimiento',
            'Tipo de movimiento'
        ]
        lstTipoDato = [
            'Fecha', 
            'AlfaNumérico',
            'Numérico', 
            'Numérico', 
            'Alfabético',
            'Fecha',
            'Alfabético',
            'Numérico',
            'Numérico',
            'Decimal',
            'Decimal',
            'Decimal',
            'Decimal',
            'Decimal',
            'Decimal',
            'Decimal',
            'Numérico', 
            'Alfabético',
            'Alfabético',
            'Alfabético',
            'Alfabético',
            'AlfaNumérico',
            'AlfaNumérico',
            'Fecha',
            'Alfabético'
            ]
        lstMaximoDigitos = [
            10, 
            20,
            10,
            10,
            2,
            10,
            4,
            5,
            5,
            10,
            10,
            10,
            10,
            10,
            10,
            10,
            3,
            2,
            2,
            2,
            2,
            10,
            10,
            10,
            2
            ]
        lstCaracteresEspeciales = [
            'PERMITE /', 
            'NO PERMITE', 
            'NO PERMITE', 
            'NO PERMITE', 
            'NO PERMITE',
            'PERMITE /',
            'NO PERMITE',
            'NO PERMITE',
            'NO PERMITE',
            'PERMITE ,',
            'PERMITE ,',
            'PERMITE ,',
            'PERMITE ,',
            'PERMITE ,',
            'PERMITE ,',
            'PERMITE ,',
            'NO PERMITE',
            'NO PERMITE',
            'NO PERMITE',
            'NO PERMITE',
            'NO PERMITE',
            'NO PERMITE',
            'NO PERMITE',
            'PERMITE /',
            'NO PERMITE'
            ]
        lstObservaciones = [
            'Ingrese la fecha en que se creo este documento Ej. 17/05/22',
            'Ingrese el Nº de documento que se genero al crear este documento',
            'Ingrese el Nº del cliente de la hoja CATALOGO_CLIENTES', 
            'Ingrese el Nº del proveedor de la hoja CATALOGO_PROVEEDORES', 
            'CR = Crédito, CO = Contado',
            'Ingrese la fecha de entrega Ej. 17/05/22',
            'Ingrese el Nº de ciudad de la hoja CIUDADES', 
            'Ingrese el Nº del producto de la hoja CATALOGO_PRODUCTOS',
            'Ingrese la cantidad del producto que se genero en el documento',
            'Ingrese el precio unitario del producto',
            'Ingrese el precio total del producto (cantidad x precio unitario)',
            'Ingrese el subtotal (cantidad x precio o costo)',
            'Ingrese el valor en $ del iva (precio unitario * iva) si aplica',
            'Ingrese el descuento, si aplica',
            'Ingrese el total (subtotal + iva - descuento)',
            'Ingrese el costo total (subtotal + iva - descuento)',
            'Ingrese el Nº de bodega de la cual se registro este movimento de la hoja CATALOGO_BODEGAS',
            'CU = Cumplido, NC = No cumplido',
            'AB = Abierta, CU = Cumplida, CE = Cerrada',
            'CA = Causada, NC = No causada',
            'CE = Cerrada, AN = Anulada',
            'Ingrese el Nº de documento que confirma el movimiento (Orden de compra, Pedido, Obsequio)',
            'Ingrese el lote del producto',
            'Ingrese la fecha de vencimiento',
            'EN = Entrada, SA = Salida',
            ]
        lstCampoObligatorio = [
            'SI', 
            'SI', 
            'SI', 
            'SI',
            'NO',
            'SI', 
            'NO', 
            'SI', 
            'SI', 
            'NO', 
            'SI', 
            'NO', 
            'NO', 
            'NO', 
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
            'SI'
            ]
        dtfInstructivo = pd.DataFrame(
            {
                'NOMBRE CAMPO': lstNombresColumnas, 
                'TIPO DE DATO': lstTipoDato,
                'LONGITUD MAX': lstMaximoDigitos,
                'CARACTERES ESPECIALES': lstCaracteresEspeciales,
                'OBSERVACIONES': lstObservaciones,
                'OBLIGATORIO': lstCampoObligatorio,
                },
            index = [i for i in range (0, len(lstNombresColumnas))]
            )
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="historico_movimientos.xlsx"'
        with pd.ExcelWriter(response) as writer:
            dtfHistoricoPedidos.to_excel(writer, sheet_name='PLANTILLA_PEDIDOS', index=False)
            dtfHistoricoOrdenesCompra.to_excel(writer, sheet_name='PLANTILLA_ORDENES_COMPRA', index=False)
            dtfHistoricoEntradasAlmacen.to_excel(writer, sheet_name='PLANTILLA_ENTRADAS_ALMACEN', index=False)
            dtfHistoricoSalidasAlmacen.to_excel(writer, sheet_name='PLANTILLA_SALIDAS_ALMACEN', index=False)
            dtfHistoricoAjustesInventario.to_excel(writer, sheet_name='PLANTILLA_AJUSTES_INVENTARIO', index=False)
            dtfHistoricoDevolucionesClientes.to_excel(writer, sheet_name='PLANTILLA_DEVOLUCIONES_CLIENTES', index=False)
            dtfHistoricoDevolucionesProveedor.to_excel(writer, sheet_name='PLANTILLA_DEVOLUCIONES_PROV', index=False)
            dtfHistoricoObsequios.to_excel(writer, sheet_name='PLANTILLA_OBSEQUIOS', index=False)
            dtfTrasladosBodegas.to_excel(writer, sheet_name='PLANTILLA_TRASLADOS_BODEGAS', index=False)
            dtfSaldoInicial.to_excel(writer, sheet_name='PLANTILLA_SALDO_INICIAL', index=False)
            dtfInstructivo.to_excel(writer, sheet_name='INSTRUCTIVO', index=False)
            dtfProductos.to_excel(writer, sheet_name='CATALOGO_PRODUCTOS', index=False)
            dtfProveedores.to_excel(writer, sheet_name='CATALOGO_PROVEEDORES', index=False)
            dtfClientes.to_excel(writer, sheet_name='CATALOGO_CLIENTES', index=False)
            dtfBodegas.to_excel(writer, sheet_name='CATALOGO_BODEGAS', index=False)
            dtfCiudad.to_excel(writer, sheet_name='CIUDADES', index=False)
            fncAgregarAnchoColumna(writer, False, dtfHistoricoPedidos, 'PLANTILLA_PEDIDOS')
            fncAgregarAnchoColumna(writer, False, dtfHistoricoOrdenesCompra, 'PLANTILLA_ORDENES_COMPRA')
            fncAgregarAnchoColumna(writer, False, dtfHistoricoEntradasAlmacen, 'PLANTILLA_ENTRADAS_ALMACEN')
            fncAgregarAnchoColumna(writer, False, dtfHistoricoSalidasAlmacen, 'PLANTILLA_SALIDAS_ALMACEN')
            fncAgregarAnchoColumna(writer, False, dtfHistoricoAjustesInventario, 'PLANTILLA_AJUSTES_INVENTARIO')
            fncAgregarAnchoColumna(writer, False, dtfHistoricoDevolucionesClientes, 'PLANTILLA_DEVOLUCIONES_CLIENTES')
            fncAgregarAnchoColumna(writer, False, dtfHistoricoDevolucionesProveedor, 'PLANTILLA_DEVOLUCIONES_PROV')
            fncAgregarAnchoColumna(writer, False, dtfHistoricoObsequios, 'PLANTILLA_OBSEQUIOS')
            fncAgregarAnchoColumna(writer, False, dtfTrasladosBodegas, 'PLANTILLA_TRASLADOS_BODEGAS')
            fncAgregarAnchoColumna(writer, False, dtfSaldoInicial, 'PLANTILLA_SALDO_INICIAL')
            fncAgregarAnchoColumna(writer, True, dtfInstructivo, 'INSTRUCTIVO')
            fncAgregarAnchoColumna(writer, False, dtfProductos, 'CATALOGO_PRODUCTOS')
            fncAgregarAnchoColumna(writer, False, dtfProveedores, 'CATALOGO_PROVEEDORES')
            fncAgregarAnchoColumna(writer, False, dtfClientes, 'CATALOGO_CLIENTES')
            fncAgregarAnchoColumna(writer, False, dtfBodegas, 'CATALOGO_BODEGAS')
            fncAgregarAnchoColumna(writer, True, dtfCiudad, 'CIUDADES')
            fncAgregarComentarioCeldas(writer, 'PLANTILLA_PEDIDOS', lstCeldasPedidos, lstComentariosPedidos)
            fncAgregarComentarioCeldas(writer, 'PLANTILLA_ORDENES_COMPRA', lstCeldasOrdenesCompra, lstComentariosOrdenesCompra)
            fncAgregarComentarioCeldas(writer, 'PLANTILLA_ENTRADAS_ALMACEN', lstCeldasEntradasAlmacen, lstComentariosEntradasAlmacen)
            fncAgregarComentarioCeldas(writer, 'PLANTILLA_SALIDAS_ALMACEN', lstCeldasSalidasAlmacen, lstComentariosSalidasAlmacen)
            fncAgregarComentarioCeldas(writer, 'PLANTILLA_AJUSTES_INVENTARIO', lstCeldaAjustesInventario, lstComentariosAjustesInventarios)
            fncAgregarComentarioCeldas(writer, 'PLANTILLA_DEVOLUCIONES_CLIENTES', lstCeldaDevolucionesClientes, lstComentariosDevolucionesClientes)
            fncAgregarComentarioCeldas(writer, 'PLANTILLA_DEVOLUCIONES_PROV', lstCeldaDevolucionesProveedores, lstComentariosDevolucionesProveedores)
            fncAgregarComentarioCeldas(writer, 'PLANTILLA_OBSEQUIOS', lstCeldaObsequios, lstComentariosObsequios)
            fncAgregarComentarioCeldas(writer, 'PLANTILLA_TRASLADOS_BODEGAS', lstCeldaTrasladosBodegas, lstComentariosTrasladosBodegas)
            fncAgregarComentarioCeldas(writer, 'PLANTILLA_SALDO_INICIAL', lstCeldaSaldoInicial, lstSaldoInicial)

        return response

''' 7.2 Vista para importar historico de movimientos'''
class clsImportarHistoricoMovimientosViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/historico_movimientos.html'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lstHistoricoPedidos = [
            'Fecha de creación',
            'Nº Documento',
            'Identificación cliente',
            'Método de pago',
            'Fecha de entrega',
            'Ciudad',
            'Código producto',
            'Cantidad',
            'Precio unitario',
            'Subtotal',
            'Iva',
            'Descuento',
            'Total',
            'Bodega',
            'Condición pedido'
        ]
        tplHistoricoPedidos = (
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoClientesMdl)),
            ((False,), (True, 2), (False,), (False,), (True, ('CR', 'CO'))),
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            ((True, int), (True, 5), (False, ), (True, clsCiudadesMdl)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProductosMdl)),
            ((True, int), (True, 5), (False, ), (False,)),
            ((True, float), (True, 30), (False, ), (False,)),
            ((True, float), (True, 30), (False, ), (False,)),
            ((True, float), (True, 30), (False, ), (False,)),
            ((True, float), (True, 30), (False, ), (False,)),
            ((True, float), (True, 30), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoBodegasMdl)),
            ((False,), (True, 2), (True, 1), (False,), (True, ('CU', 'NC'))),
            )
        lstHistoricoOrdenesCompra = [
            'Fecha de creación',
            'Nº Documento',
            'Identificación proveedor',
            'Fecha de entrega',
            'Código producto',
            'Cantidad',
            'Precio unitario',
            'Precio total',
            'Bodega',
            'Condición orden compra'
        ]
        tplHistoricoOrdenesCompra = (
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProveedoresMdl)),
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProductosMdl)),
            ((True, int), (True, 5), (False,), (False,)),
            ((True, float), (True, 30), (False, ), (False,)),
            ((True, float), (True, 30), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoBodegasMdl)),
            ((False,), (True, 2), (True, 1), (False,), (True, ('AB', 'CU', 'CE'))),
            )
        lstHistoricoEntradasAlmacen = [
            'Fecha de creación',
            'Nº Documento',
            'Identificación proveedor',
            'Código producto',
            'Cantidad',
            'Precio unitario',
            'Precio total',
            'Bodega',
            'Documento cruce',
            'Condición entrada',
            'Lote',
            'Fecha de vencimiento'
        ]
        tplHistoricoEntradasAlmacen = (
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProveedoresMdl)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProductosMdl)),
            ((True, int), (True, 5), (False,), (False,)),
            ((True, float), (True, 30), (False, ), (False,)),
            ((True, float), (True, 30), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoBodegasMdl)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((False,), (True, 2), (False,), (False,), (True, ('CA', 'NC'))),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, Timestamp), (True, 20), (True, 1), (False,))
            )
        lstHistoricoSalidasAlmacen = [
            'Fecha de creación',
            'Nº Documento',
            'Identificación cliente',
            'Código producto',
            'Cantidad',
            'Precio unitario',
            'Descuento',
            'Precio total',
            'Bodega',
            'Documento cruce',
            'Condición salida',
            'Lote',
            'Fecha de vencimiento'
        ]
        tplHistoricoSalidasAlmacen = (
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoClientesMdl)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProductosMdl)),
            ((True, int), (True, 5), (False,), (False,)),
            ((True, float), (True, 30), (False, ), (False,)),
            ((True, float), (True, 30), (False, ), (False,)),
            ((True, float), (True, 30), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoBodegasMdl)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((False,), (True, 2), (False,), (False,), (True, ('CE', 'AN'))),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            )
        lstHistoricoAjustesInventario = [
            'Fecha de creación',
            'Nº Documento',
            'Tipo de movimiento',
            'Bodega',
            'Código producto',
            'Cantidad',
            'Costo total',
            'Lote',
            'Fecha de vencimiento'
        ]
        tplHistoricoAjustesInventario = (
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((False,), (True, 2), (True, 1), (False,), (True, ('EN', 'SA'))),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoBodegasMdl)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProductosMdl)),
            ((True, int), (True, 5), (True,1), (False,)),
            ((True, float), (True, 30), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            )
        lstHistoricoDevolucionesCliente = [
            'Fecha de creación',
            'Nº Documento',
            'Identificación cliente',
            'Código producto',
            'Cantidad',
            'Bodega',
            'Lote',
            'Fecha de vencimiento',
            'Documento cruce'
        ]
        tplHistoricoDevolucionesCliente = (
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoClientesMdl)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProductosMdl)),
            ((True, int), (True, 5), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoBodegasMdl)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            )
        lstHistoricoDevolucionesProveedor = [
            'Fecha de creación',
            'Nº Documento',
            'Identificación proveedor',
            'Código producto',
            'Cantidad',
            'Bodega',
            'Lote',
            'Fecha de vencimiento',
            'Documento cruce'
        ]
        tplHistoricoDevolucionesProveedor = (
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProveedoresMdl)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProductosMdl)),
            ((True, int), (True, 5), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoBodegasMdl)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            )
        lstHistoricoObsequios = [
            'Fecha de creación',
            'Nº Documento',
            'Bodega',
            'Código producto',
            'Cantidad',
            'Costo total',
            'Lote',
            'Fecha de vencimiento'
        ]
        tplHistoricoObsequios = (
            ((True, date), (True, 20), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoBodegasMdl)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProductosMdl)),
            ((True, int), (True, 5), (True, 1), (False,)),
            ((True, float), (True, 30), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, Timestamp), (True, 20), (True, 1), (False,))
            )
        lstHistoricoTrasladosBodegas = [
            'Fecha de creación',
            'Nº Documento',
            'Tipo de movimiento',
            'Bodega',
            'Código producto',
            'Cantidad',
            'Costo total',
            'Lote',
            'Fecha de vencimiento'
        ]
        tplHistoricoTrasladosBodegas = (
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((False,), (True, 2), (True, 1), (False,), (True, ('EN', 'SA'))),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoBodegasMdl)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProductosMdl)),
            ((True, int), (True, 5), (True, 1), (False,)),
            ((True, float), (True, 30), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, Timestamp), (True, 20), (True, 1), (False,))
            )
        lstHistoricoSaldoInicial = [
            'Fecha de creación',
            'Código producto',
            'Bodega',
            'Cantidad',
            'Lote',
            'Fecha de vencimiento'
        ]
        tplHistoricoSaldoInicial = (
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProductosMdl)),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoBodegasMdl)),
            ((True, int), (True, 5), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, Timestamp), (True, 20), (True, 1), (False,))
            )
        try:
            action = request.POST['action']
            data = {}
            if action == 'upload':
                new_file = request.FILES['file']
                if str(new_file).endswith('.xlsx'):
                    dtfHistoricoPedidos = pd.read_excel(new_file, 0)
                    dtfHistoricoPedidos = dtfHistoricoPedidos.fillna(0)
                    dtfHistoricoOrdenesCompra = pd.read_excel(new_file, 1)
                    dtfHistoricoOrdenesCompra = dtfHistoricoOrdenesCompra.fillna(0)
                    dtfHistoricoEntradasAlmacen = pd.read_excel(new_file, 2)
                    dtfHistoricoEntradasAlmacen = dtfHistoricoEntradasAlmacen.fillna(0)
                    dtfHistoricoSalidasAlmacen = pd.read_excel(new_file, 3)
                    dtfHistoricoSalidasAlmacen = dtfHistoricoSalidasAlmacen.fillna(0)
                    dtfHistoricoAjustesInventario = pd.read_excel(new_file, 4)
                    dtfHistoricoAjustesInventario = dtfHistoricoAjustesInventario.fillna(0)
                    dtfHistoricoDevolucionesCliente = pd.read_excel(new_file, 5)
                    dtfHistoricoDevolucionesCliente = dtfHistoricoDevolucionesCliente.fillna(0)
                    dtfHistoricoDevolucionesProveedor = pd.read_excel(new_file, 6)
                    dtfHistoricoDevolucionesProveedor = dtfHistoricoDevolucionesProveedor.fillna(0)
                    dtfHistoricoObsequios = pd.read_excel(new_file, 7)
                    dtfHistoricoObsequios = dtfHistoricoObsequios.fillna(0)
                    dtfHistoricoTrasladosBodegas = pd.read_excel(new_file, 8)
                    dtfHistoricoTrasladosBodegas = dtfHistoricoTrasladosBodegas.fillna(0)
                    dtfHistoricoSaldoInicial = pd.read_excel(new_file, 9)
                    dtfHistoricoSaldoInicial = dtfHistoricoSaldoInicial.fillna(0)
                    lstValidarPedidos = [ fncValidarImportacionlst(dtfHistoricoPedidos, i, j) for (i, j) in zip(lstHistoricoPedidos, tplHistoricoPedidos) ]
                    lstValidarPedidos = [ i for n in lstValidarPedidos for i in n ]
                    lstValidarOrdenesCompra = [ fncValidarImportacionlst(dtfHistoricoOrdenesCompra, i, j) for (i, j) in zip(lstHistoricoOrdenesCompra, tplHistoricoOrdenesCompra) ]
                    lstValidarOrdenesCompra = [ i for n in lstValidarOrdenesCompra for i in n ]
                    lstValidarEntradasAlmacen = [ fncValidarImportacionlst(dtfHistoricoEntradasAlmacen, i, j) for (i, j) in zip(lstHistoricoEntradasAlmacen, tplHistoricoEntradasAlmacen) ]
                    lstValidarEntradasAlmacen = [ i for n in lstValidarEntradasAlmacen for i in n ]
                    lstValidarSalidasAlmacen = [ fncValidarImportacionlst(dtfHistoricoSalidasAlmacen, i, j) for (i, j) in zip(lstHistoricoSalidasAlmacen, tplHistoricoSalidasAlmacen) ]
                    lstValidarSalidasAlmacen = [ i for n in lstValidarSalidasAlmacen for i in n ]
                    lstValidarAjustesInventario = [ fncValidarImportacionlst(dtfHistoricoAjustesInventario, i, j) for (i, j) in zip(lstHistoricoAjustesInventario, tplHistoricoAjustesInventario) ]
                    lstValidarAjustesInventario = [ i for n in lstValidarAjustesInventario for i in n ]
                    lstValidarDevolucionesCliente = [ fncValidarImportacionlst(dtfHistoricoDevolucionesCliente, i, j) for (i, j) in zip(lstHistoricoDevolucionesCliente, tplHistoricoDevolucionesCliente) ]
                    lstValidarDevolucionesCliente = [ i for n in lstValidarDevolucionesCliente for i in n ]
                    lstValidarDevolucionesProveedor = [ fncValidarImportacionlst(dtfHistoricoDevolucionesProveedor, i, j) for (i, j) in zip(lstHistoricoDevolucionesProveedor, tplHistoricoDevolucionesProveedor) ]
                    lstValidarDevolucionesProveedor = [ i for n in lstValidarDevolucionesProveedor for i in n ]
                    lstValidarObsequios = [ fncValidarImportacionlst(dtfHistoricoObsequios, i, j) for (i, j) in zip(lstHistoricoObsequios, tplHistoricoObsequios) ]
                    lstValidarObsequios = [ i for n in lstValidarObsequios for i in n ]
                    lstValidarTrasladosBodegas = [ fncValidarImportacionlst(dtfHistoricoTrasladosBodegas, i, j) for (i, j) in zip(lstHistoricoTrasladosBodegas, tplHistoricoTrasladosBodegas) ]
                    lstValidarTrasladosBodegas = [ i for n in lstValidarTrasladosBodegas for i in n ]
                    lstValidarSaldoInicial = [ fncValidarImportacionlst(dtfHistoricoSaldoInicial, i, j) for (i, j) in zip(lstHistoricoSaldoInicial, tplHistoricoSaldoInicial) ]
                    lstValidarSaldoInicial = [ i for n in lstValidarSaldoInicial for i in n ]
                    dctValidaciones = {}
                    if len(lstValidarPedidos):
                        dtfHistoricoPedidos.loc[:,'Fecha de creación'] = dtfHistoricoPedidos['Fecha de creación'].astype(str)
                        dtfHistoricoPedidos.loc[:,'Fecha de entrega'] = dtfHistoricoPedidos['Fecha de entrega'].astype(str)
                        dctValidaciones['dtfHistoricoPedidosError'] = dtfHistoricoPedidos.to_json(orient="split")
                        dctValidaciones['lstValidarPedidos'] = lstValidarPedidos
                    if len(lstValidarOrdenesCompra):
                        dtfHistoricoOrdenesCompra.loc[:,'Fecha de creación'] = dtfHistoricoOrdenesCompra['Fecha de creación'].astype(str)
                        dtfHistoricoOrdenesCompra.loc[:,'Fecha de entrega'] = dtfHistoricoOrdenesCompra['Fecha de entrega'].astype(str)
                        dctValidaciones['dtfHistoricoOrdenesCompraError'] = dtfHistoricoOrdenesCompra.to_json(orient="split")
                        dctValidaciones['lstValidarOrdenesCompra'] = lstValidarOrdenesCompra
                    if len(lstValidarEntradasAlmacen):
                        dtfHistoricoEntradasAlmacen.loc[:,'Fecha de creación'] = dtfHistoricoEntradasAlmacen['Fecha de creación'].astype(str)
                        dtfHistoricoEntradasAlmacen.loc[:,'Fecha de vencimiento'] = dtfHistoricoEntradasAlmacen['Fecha de vencimiento'].astype(str)
                        dctValidaciones['dtfHistoricoEntradasAlmacenError'] = dtfHistoricoEntradasAlmacen.to_json(orient="split")
                        dctValidaciones['lstValidarEntradasAlmacen'] = lstValidarEntradasAlmacen
                    if len(lstValidarSalidasAlmacen):
                        dtfHistoricoSalidasAlmacen.loc[:,'Fecha de creación'] = dtfHistoricoSalidasAlmacen['Fecha de creación'].astype(str)
                        dtfHistoricoSalidasAlmacen.loc[:,'Fecha de vencimiento'] = dtfHistoricoSalidasAlmacen['Fecha de vencimiento'].astype(str)
                        dctValidaciones['dtfHistoricoSalidasAlmacenError'] = dtfHistoricoSalidasAlmacen.to_json(orient="split")
                        dctValidaciones['lstValidarSalidasAlmacen'] = lstValidarSalidasAlmacen
                    if len(lstValidarAjustesInventario):
                        dtfHistoricoAjustesInventario.loc[:,'Fecha de creación'] = dtfHistoricoAjustesInventario['Fecha de creación'].astype(str)
                        dtfHistoricoAjustesInventario.loc[:,'Fecha de vencimiento'] = dtfHistoricoAjustesInventario['Fecha de vencimiento'].astype(str)
                        dctValidaciones['dtfHistoricoAjustesInventarioError'] = dtfHistoricoAjustesInventario.to_json(orient="split")
                        dctValidaciones['lstValidarAjustesInventario'] = lstValidarAjustesInventario
                    if len(lstValidarDevolucionesCliente):
                        dtfHistoricoDevolucionesCliente.loc[:,'Fecha de creación'] = dtfHistoricoDevolucionesCliente['Fecha de creación'].astype(str)
                        dtfHistoricoDevolucionesCliente.loc[:,'Fecha de vencimiento'] = dtfHistoricoDevolucionesCliente['Fecha de vencimiento'].astype(str)
                        dctValidaciones['dtfHistoricoDevolucionesClienteError'] = dtfHistoricoDevolucionesCliente.to_json(orient="split")
                        dctValidaciones['lstValidarDevolucionesCliente'] = lstValidarDevolucionesCliente
                    if len(lstValidarDevolucionesProveedor):
                        dtfHistoricoDevolucionesProveedor.loc[:,'Fecha de creación'] = dtfHistoricoDevolucionesProveedor['Fecha de creación'].astype(str)
                        dtfHistoricoDevolucionesProveedor.loc[:,'Fecha de vencimiento'] = dtfHistoricoDevolucionesProveedor['Fecha de vencimiento'].astype(str)
                        dctValidaciones['dtfHistoricoDevolucionesProveedorError'] = dtfHistoricoDevolucionesProveedor.to_json(orient="split")
                        dctValidaciones['lstValidarDevolucionesProveedor'] = lstValidarDevolucionesProveedor
                    if len(lstValidarObsequios):
                        dtfHistoricoObsequios.loc[:,'Fecha de creación'] = dtfHistoricoObsequios['Fecha de creación'].astype(str)
                        dtfHistoricoObsequios.loc[:,'Fecha de vencimiento'] = dtfHistoricoObsequios['Fecha de vencimiento'].astype(str)
                        dctValidaciones['dtfHistoricoObsequiosError'] = dtfHistoricoObsequios.to_json(orient="split")
                        dctValidaciones['lstValidarObsequios'] = lstValidarObsequios
                    if len(lstValidarTrasladosBodegas):
                        dtfHistoricoTrasladosBodegas.loc[:,'Fecha de creación'] = dtfHistoricoTrasladosBodegas['Fecha de creación'].astype(str)
                        dtfHistoricoTrasladosBodegas.loc[:,'Fecha de vencimiento'] = dtfHistoricoTrasladosBodegas['Fecha de vencimiento'].astype(str)
                        dctValidaciones['dtfHistoricoTrasladosBodegasError'] = dtfHistoricoTrasladosBodegas.to_json(orient="split")
                        dctValidaciones['lstValidarTrasladosBodegas'] = lstValidarTrasladosBodegas
                    if len(lstValidarSaldoInicial):
                        dtfHistoricoSaldoInicial.loc[:,'Fecha de creación'] = dtfHistoricoSaldoInicial['Fecha de creación'].astype(str)
                        dtfHistoricoSaldoInicial.loc[:,'Fecha de vencimiento'] = dtfHistoricoSaldoInicial['Fecha de vencimiento'].astype(str)
                        dctValidaciones['dtfHistoricoSaldoInicialError'] = dtfHistoricoSaldoInicial.to_json(orient="split")
                        dctValidaciones['lstValidarSaldoInicial'] = lstValidarSaldoInicial
                    if len(dctValidaciones):
                        data['dctValidaciones'] = dctValidaciones
                        data['strError'] = 'El archivo presenta errores, ¿desea descargarlos?'
                        response = JsonResponse(data, safe=False)
                    else:                       
                        # Validar continuidad periodos
                        dtfHistoricoSaldoInicial.rename(columns= {'Fecha de creación': 'creation_date', 'Código producto': 'product_code', 
                        'Bodega': 'store', 'Cantidad': 'quantity', 'Lote': 'batch', 'Fecha de vencimiento': 'expiration_date'}, inplace= True)
                        dtfHistoricoAjustesInventario.rename(columns= {'Fecha de creación': 'creation_date', 'Nº Documento': 'doc_number', 
                        'Tipo de movimiento': 'type', 'Bodega': 'store', 'Código producto': 'product_code', 'Cantidad': 'quantity', 
                        'Costo total': 'total_cost', 'Lote': 'batch', 'Fecha de vencimiento': 'expiration_date'}, inplace= True)
                        dtfHistoricoEntradasAlmacen.rename(columns= {'Fecha de creación': 'creation_date', 'Nº Documento': 'doc_number', 
                        'Identificación proveedor': 'identification', 'Código producto': 'product_code', 'Cantidad': 'quantity', 
                        'Precio unitario': 'unitary_cost', 'Precio total': 'total_cost', 'Bodega': 'store', 'Documento cruce': 'crossing_doc', 
                        'Condición entrada': 'condition', 'Lote': 'batch', 'Fecha de vencimiento': 'expiration_date'}, inplace= True)
                        dtfHistoricoDevolucionesCliente.rename(columns= {'Fecha de creación': 'creation_date', 'Nº Documento': 'doc_number', 
                        'Identificación cliente': 'identification', 'Código producto': 'product_code', 'Cantidad': 'quantity', 'Bodega': 'store', 
                        'Lote': 'batch', 'Fecha de vencimiento': 'expiration_date', 'Documento cruce': 'crossing_doc'}, inplace= True)
                        dtfHistoricoDevolucionesProveedor.rename(columns= {'Fecha de creación': 'creation_date', 'Nº Documento': 'doc_number', 
                        'Identificación proveedor': 'identification', 'Código producto': 'product_code', 'Cantidad': 'quantity', 
                        'Bodega': 'store', 'Lote': 'batch', 'Fecha de vencimiento': 'expiration_date', 'Documento cruce': 'crossing_doc'}, 
                        inplace= True)
                        dtfHistoricoSalidasAlmacen.rename(columns= {'Fecha de creación': 'creation_date', 'Nº Documento': 'doc_number', 
                        'Identificación cliente': 'identification', 'Código producto': 'product_code', 'Cantidad': 'quantity', 
                        'Precio unitario': 'unit_price', 'Descuento': 'discount', 'Precio total': 'total_price', 'Bodega': 'store', 
                        'Documento cruce': 'crossing_doc', 'Condición salida': 'condition', 'Lote': 'batch', 
                        'Fecha de vencimiento': 'expiration_date'}, inplace= True)
                        dtfHistoricoObsequios.rename(columns= {'Fecha de creación': 'creation_date', 'Nº Documento': 'doc_number', 
                        'Bodega': 'store', 'Código producto': 'product_code', 'Cantidad': 'quantity', 'Costo total': 'total_cost', 'Lote': 'batch',
                        'Fecha de vencimiento': 'expiration_date'}, inplace= True)
                        dtfHistoricoTrasladosBodegas.rename(columns= {'Fecha de creación': 'creation_date', 'Nº Documento': 'doc_number', 
                        'Tipo de movimiento': 'type', 'Bodega': 'store', 'Código producto': 'product_code', 'Cantidad': 'quantity', 
                        'Costo total': 'total_cost', 'Lote': 'batch', 'Fecha de vencimiento': 'expiration_date'}, inplace= True)
                        dtfHistoricoPedidos.rename(columns= {'Fecha de creación': 'creation_date', 'Cantidad': 'quantity'}, inplace= True)
                        dtfHistoricoOrdenesCompra.rename(columns= {'Fecha de creación': 'creation_date', 'Cantidad': 'quantity'}, inplace= True)
                        lstTablasDocumentos = [dtfHistoricoPedidos, dtfHistoricoOrdenesCompra, dtfHistoricoEntradasAlmacen, dtfHistoricoSalidasAlmacen]
                        lstContinuidadMeses = [ fncFechaConsecutivabol(i) for i in lstTablasDocumentos ]                        
                        lstIndicesContinuidad = [ lstContinuidadMeses.index(i) for i in lstContinuidadMeses if i == False ]
                        lstNombresDocumentos = ['Historico pedidos', 'Historico ordenes de compra', 'Historico entradas de almacén', 'Historico salidas de almacén']
                        if len(lstIndicesContinuidad):
                            lstBasesError = []
                            for i in lstIndicesContinuidad:
                                lstBasesError.append(lstNombresDocumentos[i])
                            data['error'] = f'Las bases de datos: { lstBasesError } no tienen continuidad'
                            response = JsonResponse(data, safe=False)
                        else:
                            # Validar tamaño de base de datos
                            lstOrganizarDatos = [
                            fncOrganizadtf(dtfHistoricoPedidos, 'creation_date', 'quantity', 'W', 'sum', bolAgrupaProd= False),
                            fncOrganizadtf(dtfHistoricoOrdenesCompra, 'creation_date', 'quantity', 'W', 'sum', bolAgrupaProd= False),
                            fncOrganizadtf(dtfHistoricoEntradasAlmacen, 'creation_date', 'quantity', 'W', 'sum', bolAgrupaProd= False),
                            fncOrganizadtf(dtfHistoricoSalidasAlmacen, 'creation_date', 'quantity', 'W', 'sum', bolAgrupaProd= False),
                            ]
                            lstRangosPeriodos = [ str(fncRangoPeriodosstr(i, 5, 12)) for i in lstOrganizarDatos ]
                            if ('Empty' in lstRangosPeriodos) | ('Incomplete' in lstRangosPeriodos):
                                data['error'] = 'La base de datos no cumple con el tamaño apropiado para el calculo de indicadores y politica de inventarios'
                                response = JsonResponse(data, safe=False)
                            else:
                                # Recortar tablas de datos que exceden el tamaño
                                lstTablasDocumentos = [ lstTablasDocumentos[i] if lstRangosPeriodos[i] != 'Bigger' else fncCortaCuadrodtf(lstTablasDocumentos[i], 
                                3 ) for i in range(0, len(lstTablasDocumentos))]
                                lstParaHistorico= [dtfHistoricoSaldoInicial, dtfHistoricoAjustesInventario, dtfHistoricoEntradasAlmacen, 
                                dtfHistoricoDevolucionesCliente, dtfHistoricoDevolucionesProveedor, dtfHistoricoSalidasAlmacen, dtfHistoricoObsequios, 
                                dtfHistoricoTrasladosBodegas]
                                fncMovimientosHistoricosProductosdtf(lstParaHistorico)
                                with transaction.atomic():
                                    for pedido in (lstTablasDocumentos[0].values.tolist()):
                                        clsHistoricoPedidosMdl.objects.create(
                                        date_creation = pedido[0].date(),
                                        doc_number = str(pedido[1]),
                                        identification_id = int(pedido[2]),
                                        pay_method = pedido[3],
                                        delivery_date = pedido[4].date(),
                                        city_id = int(pedido[5]),
                                        product_code_id = int(pedido[6]),
                                        quantity = int(pedido[7]),
                                        unit_price = float(pedido[8]),
                                        subtotal = float(pedido[9]),
                                        iva = float(pedido[10]),
                                        discount = float(pedido[11]),
                                        total = float(pedido[12]),
                                        store_id = int(pedido[13]),
                                        condition = pedido[14],
                                        )
                                    for orden_compra in (lstTablasDocumentos[1].values.tolist()):
                                        clsHistoricoOrdenesCompraMdl.objects.create(
                                        date_creation = orden_compra[0].date(),
                                        doc_number = str(orden_compra[1]),
                                        identification_id = int(orden_compra[2]),
                                        delivery_date = orden_compra[3].date(),
                                        product_code_id = int(orden_compra[4]),
                                        quantity = int(orden_compra[5]),
                                        unit_price = float(orden_compra[6]),
                                        total_price = float(orden_compra[7]),
                                        store_id = int(orden_compra[8]),
                                        condition = orden_compra[9],
                                        )
                                data['success'] = '¡Se ha cargado el archivo a su base de datos con éxito!'
                                response = JsonResponse(data, safe=False)
                else:
                    data['error'] = 'Compruebe el formato del archivo'
                    response = JsonResponse(data, safe=False)
            elif action == 'download_errors':
                dtfHistoricoPedidosError = None
                dtfHistoricoOrdenesCompraError = None
                dtfHistoricoEntradasAlmacenError = None
                dtfHistoricoSalidasAlmacenError = None
                dtfHistoricoAjustesInventarioError = None
                dtfHistoricoDevolucionesClienteError = None
                dtfHistoricoDevolucionesProveedorError = None
                dtfHistoricoObsequiosError = None
                dtfHistoricoTrasladosBodegasError = None
                dtfHistoricoSaldoInicialError = None
                dctValidaciones = json.loads(request.POST['dctValidaciones'])
                if 'dtfHistoricoPedidosError' in dctValidaciones:
                    dtfHistoricoPedidosError = pd.read_json(dctValidaciones['dtfHistoricoPedidosError'], orient='split')
                    lstValidarPedidos = dctValidaciones['lstValidarPedidos']
                    lstFilasPedidosError = list( dict.fromkeys([ i[1] for i in lstValidarPedidos ]) )
                    dtfHistoricoPedidosError = fncAgregarErroresDataframedtf(dtfHistoricoPedidosError, lstValidarPedidos, lstFilasPedidosError)
                if 'dtfHistoricoOrdenesCompraError' in dctValidaciones:
                    dtfHistoricoOrdenesCompraError = pd.read_json(dctValidaciones['dtfHistoricoOrdenesCompraError'], orient='split')
                    lstValidarOrdenesCompra = dctValidaciones['lstValidarOrdenesCompra']
                    lstFilasOrdenesCompraError = list( dict.fromkeys([ i[1] for i in lstValidarOrdenesCompra ]) )
                    dtfHistoricoOrdenesCompraError = fncAgregarErroresDataframedtf(dtfHistoricoOrdenesCompraError, lstValidarOrdenesCompra, lstFilasOrdenesCompraError)
                if 'dtfHistoricoEntradasAlmacenError' in dctValidaciones:
                    dtfHistoricoEntradasAlmacenError = pd.read_json(dctValidaciones['dtfHistoricoEntradasAlmacenError'], orient='split')
                    lstValidarEntradasAlmacen = dctValidaciones['lstValidarEntradasAlmacen']
                    lstFilasEntradasAlmacenError = list( dict.fromkeys([ i[1] for i in lstValidarEntradasAlmacen ]) )
                    dtfHistoricoEntradasAlmacenError = fncAgregarErroresDataframedtf(dtfHistoricoEntradasAlmacenError, lstValidarEntradasAlmacen, lstFilasEntradasAlmacenError)
                if 'dtfHistoricoSalidasAlmacenError' in dctValidaciones:
                    dtfHistoricoSalidasAlmacenError = pd.read_json(dctValidaciones['dtfHistoricoSalidasAlmacenError'], orient='split')
                    lstValidarSalidasAlmacen = dctValidaciones['lstValidarSalidasAlmacen']
                    lstFilasSalidasAlmacenError = list( dict.fromkeys([ i[1] for i in lstValidarSalidasAlmacen ]) )
                    dtfHistoricoSalidasAlmacenError = fncAgregarErroresDataframedtf(dtfHistoricoSalidasAlmacenError, lstValidarSalidasAlmacen, lstFilasSalidasAlmacenError)
                if 'dtfHistoricoAjustesInventarioError' in dctValidaciones:
                    dtfHistoricoAjustesInventarioError = pd.read_json(dctValidaciones['dtfHistoricoAjustesInventarioError'], orient='split')
                    lstValidarAjustesInventario = dctValidaciones['lstValidarAjustesInventario']
                    lstFilasAjustesInventarioError = list( dict.fromkeys([ i[1] for i in lstValidarAjustesInventario ]) )
                    dtfHistoricoAjustesInventarioError = fncAgregarErroresDataframedtf(dtfHistoricoAjustesInventarioError, lstValidarAjustesInventario, lstFilasAjustesInventarioError)
                if 'dtfHistoricoDevolucionesClienteError' in dctValidaciones:
                    dtfHistoricoDevolucionesClienteError = pd.read_json(dctValidaciones['dtfHistoricoDevolucionesClienteError'], orient='split')
                    lstValidarDevolucionesCliente = dctValidaciones['lstValidarDevolucionesCliente']
                    lstFilasDevolucionesClienteError = list( dict.fromkeys([ i[1] for i in lstValidarDevolucionesCliente ]) )
                    dtfHistoricoDevolucionesClienteError = fncAgregarErroresDataframedtf(dtfHistoricoDevolucionesClienteError, lstValidarDevolucionesCliente, lstFilasDevolucionesClienteError)
                if 'dtfHistoricoDevolucionesProveedorError' in dctValidaciones:
                    dtfHistoricoDevolucionesProveedorError = pd.read_json(dctValidaciones['dtfHistoricoDevolucionesProveedorError'], orient='split')
                    lstValidarDevolucionesProveedor = dctValidaciones['lstValidarDevolucionesProveedor']
                    lstFilasDevolucionesProveedorError = list( dict.fromkeys([ i[1] for i in lstValidarDevolucionesProveedor ]) )
                    dtfHistoricoDevolucionesProveedorError = fncAgregarErroresDataframedtf(dtfHistoricoDevolucionesProveedorError, lstValidarDevolucionesProveedor, lstFilasDevolucionesProveedorError)
                if 'dtfHistoricoObsequiosError' in dctValidaciones:
                    dtfHistoricoObsequiosError = pd.read_json(dctValidaciones['dtfHistoricoObsequiosError'], orient='split')
                    lstValidarObsequios = dctValidaciones['lstValidarObsequios']
                    lstFilasObsequiosError = list( dict.fromkeys([ i[1] for i in lstValidarObsequios ]) )
                    dtfHistoricoObsequiosError = fncAgregarErroresDataframedtf(dtfHistoricoObsequiosError, lstValidarObsequios, lstFilasObsequiosError)
                if 'dtfHistoricoTrasladosBodegasError' in dctValidaciones:
                    dtfHistoricoTrasladosBodegasError = pd.read_json(dctValidaciones['dtfHistoricoTrasladosBodegasError'], orient='split')
                    lstValidarTrasladosBodegas = dctValidaciones['lstValidarTrasladosBodegas']
                    lstFilasTrasladosBodegasError = list( dict.fromkeys([ i[1] for i in lstValidarTrasladosBodegas ]) )
                    dtfHistoricoTrasladosBodegasError = fncAgregarErroresDataframedtf(dtfHistoricoTrasladosBodegasError, lstValidarTrasladosBodegas, lstFilasTrasladosBodegasError)
                if 'dtfHistoricoSaldoInicialError' in dctValidaciones:
                    dtfHistoricoSaldoInicialError = pd.read_json(dctValidaciones['dtfHistoricoSaldoInicialError'], orient='split')
                    lstValidarSaldoInicial = dctValidaciones['lstValidarSaldoInicial']
                    lstFilasSaldoInicialError = list( dict.fromkeys([ i[1] for i in lstValidarSaldoInicial ]) )
                    dtfHistoricoSaldoInicialError = fncAgregarErroresDataframedtf(dtfHistoricoSaldoInicialError, lstValidarSaldoInicial, lstFilasSaldoInicialError)
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="errores_historico_pedidos.xlsx"'
                with pd.ExcelWriter(response) as writer:
                    if dtfHistoricoPedidosError is not None:
                        dtfHistoricoPedidosError.to_excel(writer, sheet_name='PEDIDOS_ERROR', index=False)
                        fncAgregarFormatoColumnasError(writer, lstValidarPedidos, 'PEDIDOS_ERROR', lstHistoricoPedidos)
                        fncAgregarAnchoColumna(writer, False, dtfHistoricoPedidosError, 'PEDIDOS_ERROR')
                    if dtfHistoricoOrdenesCompraError is not None:
                        dtfHistoricoOrdenesCompraError.to_excel(writer, sheet_name='ORDENES_COMPRA_ERROR', index=False)
                        fncAgregarFormatoColumnasError(writer, lstValidarOrdenesCompra, 'ORDENES_COMPRA_ERROR', lstHistoricoOrdenesCompra)
                        fncAgregarAnchoColumna(writer, False, dtfHistoricoOrdenesCompraError, 'ORDENES_COMPRA_ERROR')
                    if dtfHistoricoEntradasAlmacenError is not None:
                        dtfHistoricoEntradasAlmacenError.to_excel(writer, sheet_name='ENTRADAS_ALMACEN_ERROR', index=False)
                        fncAgregarFormatoColumnasError(writer, lstValidarEntradasAlmacen, 'ENTRADAS_ALMACEN_ERROR', lstHistoricoEntradasAlmacen)
                        fncAgregarAnchoColumna(writer, False, dtfHistoricoEntradasAlmacenError, 'ENTRADAS_ALMACEN_ERROR')
                    if dtfHistoricoSalidasAlmacenError is not None:
                        dtfHistoricoSalidasAlmacenError.to_excel(writer, sheet_name='SALIDAS_ALMACEN_ERROR', index=False)
                        fncAgregarFormatoColumnasError(writer, lstValidarSalidasAlmacen, 'SALIDAS_ALMACEN_ERROR', lstHistoricoSalidasAlmacen)
                        fncAgregarAnchoColumna(writer, False, dtfHistoricoSalidasAlmacenError, 'SALIDAS_ALMACEN_ERROR')
                    if dtfHistoricoAjustesInventarioError is not None:
                        dtfHistoricoAjustesInventarioError.to_excel(writer, sheet_name='AJUSTES_INVENTARIO_ERROR', index=False)
                        fncAgregarFormatoColumnasError(writer, lstValidarAjustesInventario, 'AJUSTES_INVENTARIO_ERROR', lstHistoricoAjustesInventario)
                        fncAgregarAnchoColumna(writer, False, dtfHistoricoAjustesInventarioError, 'AJUSTES_INVENTARIO_ERROR')
                    if dtfHistoricoDevolucionesClienteError is not None:
                        dtfHistoricoDevolucionesClienteError.to_excel(writer, sheet_name='DEVOLUCIONES_CLIENTE_ERROR', index=False)
                        fncAgregarFormatoColumnasError(writer, lstValidarDevolucionesCliente, 'DEVOLUCIONES_CLIENTE_ERROR', lstHistoricoDevolucionesCliente)
                        fncAgregarAnchoColumna(writer, False, dtfHistoricoDevolucionesClienteError, 'DEVOLUCIONES_CLIENTE_ERROR')
                    if dtfHistoricoDevolucionesProveedorError is not None:
                        dtfHistoricoDevolucionesProveedorError.to_excel(writer, sheet_name='DEVOLUCIONES_PROVEEDOR_ERROR', index=False)
                        fncAgregarFormatoColumnasError(writer, lstValidarDevolucionesProveedor, 'DEVOLUCIONES_PROVEEDOR_ERROR', lstHistoricoDevolucionesProveedor)
                        fncAgregarAnchoColumna(writer, False, dtfHistoricoDevolucionesProveedorError, 'DEVOLUCIONES_PROVEEDOR_ERROR')
                    if dtfHistoricoObsequiosError is not None:
                        dtfHistoricoObsequiosError.to_excel(writer, sheet_name='OBSEQUIOS_ERROR', index=False)
                        fncAgregarFormatoColumnasError(writer, lstValidarObsequios, 'OBSEQUIOS_ERROR', lstHistoricoObsequios)
                        fncAgregarAnchoColumna(writer, False, dtfHistoricoObsequiosError, 'OBSEQUIOS_ERROR')
                    if dtfHistoricoTrasladosBodegasError is not None:
                        dtfHistoricoTrasladosBodegasError.to_excel(writer, sheet_name='TRASLADOS_BODEGA_ERROR', index=False)
                        fncAgregarFormatoColumnasError(writer, lstValidarTrasladosBodegas, 'TRASLADOS_BODEGA_ERROR', lstHistoricoTrasladosBodegas)
                        fncAgregarAnchoColumna(writer, False, dtfHistoricoTrasladosBodegasError, 'TRASLADOS_BODEGA_ERROR')
                    if dtfHistoricoSaldoInicialError is not None:
                        dtfHistoricoSaldoInicialError.to_excel(writer, sheet_name='SALDO_INICIAL_ERROR', index=False)
                        fncAgregarFormatoColumnasError(writer, lstValidarSaldoInicial, 'SALDO_INICIAL_ERROR', lstHistoricoSaldoInicial)
                        fncAgregarAnchoColumna(writer, False, dtfHistoricoSaldoInicialError, 'SALDO_INICIAL_ERROR')
        except Exception as e:
            data['error'] = str(e)
            response = JsonResponse(data, safe=False)
        return response

#################################################################################################
# 8. PARAMETRIZACIÓN AJUSTES DE INVENTARIO (MENÚ, IMPORTAR, EXPORTAR Y CREAR AJUSTE)
#################################################################################################
''' 8.1 Vista menú ajustes de inventario'''
class clsAjustesInventarioViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/ajustes_inventario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options_title'] = 'Carga masiva'
        context['options_url'] = reverse_lazy('configuracion:importar_ajustes_inventario')
        context['create_title'] = 'Crear ajuste de inventario'
        context['create_url'] = reverse_lazy('configuracion:crear_ajuste_inventario')
        return context

''' 8.2 Vista para exportar plantilla de ajustes de inventario'''
class clsExportarPlantillaAjustesInventarioViw(APIView):

    def get(self, request):
        lstCeldaAjustesInventario = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1']
        lstComentariosAjustesInventarios = [
            'Donde se movió el producto, ingresa el N° correspondiente de la hoja (primer columna): "CATALOGO_BODEGAS"',
            'Si el movimiento es una entrada digita EN, si es una salida ingresa SA (manten las mayusculas)',
            'Ingresa el número de la primer columna del producto según la hoja de este archivo llamada "CATALOGO_PRODUCTOS"',
            'Digita la cantidad que se relaciona de ese producto en el documento',
            'Ingresa el Total, en este caso es: el costo unitario por la cantidad, puedes incluir dos decimales',
            'Ingresa el lote del producto que salió, si son varios lotes, por cada lote es una fila ',
            'Si aplica, ingresa la fecha de vencimiento de los productos recibidos, por cada fecha diferente es una fila'
        ]
        qrsProductos = clsCatalogoProductosMdl.objects.all()
        srlProductos = clsCatalogoProductosPlantillajson(qrsProductos, many=True)
        dtfProductos = pd.DataFrame(srlProductos.data)
        dtfProductos = dtfProductos.rename(columns={'id':'Código', 'product_desc':'Descripción producto'})
        qrsBodegas = clsCatalogoBodegasMdl.objects.all()
        srlBodegas = clsCatalogoBodegasPlantillajson(qrsBodegas, many=True)
        dtfBodegas = pd.DataFrame(srlBodegas.data)
        dtfBodegas = dtfBodegas.rename(columns={'id':'Código', 'warehouse_name':'Nombre bodega', 'contact_name':'Responsable'})
        dtfHistoricoAjustesInventario = pd.DataFrame(
            {
                'Bodega':[],
                'Tipo de ajuste':[],
                'Código producto':[],
                'Cantidad':[],
                'Costo total':[],
                'Lote':[],
                'Fecha de vencimiento':[]
            }, 
            index = [i for i in range (0, 0)]
            )
        lstNombresColumnas = [
            'Bodega',
            'Tipo de ajuste',
            'Código producto',
            'Cantidad',
            'Costo total',
            'Lote',
            'Fecha de vencimiento'
        ]
        lstTipoDato = [
            'Numérico',
            'Alfabético',
            'Numérico',
            'Numérico',
            'Decimal',
            'AlfaNumérico',
            'Fecha',
            ]
        lstMaximoDigitos = [
            2,
            2,
            5,
            10,
            10,
            10,
            10
            ]
        lstCaracteresEspeciales = [
            'NO PERMITE', 
            'NO PERMITE', 
            'NO PERMITE', 
            'NO PERMITE',
            'PERMITE ,',
            'PERMITE /',
            'NO PERMITE',
            ]
        lstObservaciones = [
            'Ingresa el numero según la primera columna de la hoja "CATALOGO_BODEGAS"',
            'EN = Entrada, SA = Salida',
            'Ingrese el Nº del producto de la hoja CATALOGO_PRODUCTOS',
            'Ingrese la cantidad del producto que se ajustara',
            'Ingrese el costo total del producto (cantidad x precio unitario)',
            'Ingrese el lote del producto',
            'Ingrese la fecha de vencimiento',
            ]
        lstCampoObligatorio = [
            'SI', 
            'SI', 
            'SI', 
            'SI',
            'SI', 
            'SI', 
            'NO'
            ]
        dtfInstructivo = pd.DataFrame(
            {
                'NOMBRE CAMPO': lstNombresColumnas, 
                'TIPO DE DATO': lstTipoDato,
                'LONGITUD MAX': lstMaximoDigitos,
                'CARACTERES ESPECIALES': lstCaracteresEspeciales,
                'OBSERVACIONES': lstObservaciones,
                'OBLIGATORIO': lstCampoObligatorio,
                },
            index = [i for i in range (0, len(lstNombresColumnas))]
            )
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="ajustes_inventario.xlsx"'
        with pd.ExcelWriter(response) as writer:
            dtfHistoricoAjustesInventario.to_excel(writer, sheet_name='PLANTILLA_AJUSTES_INVENTARIO', index=False)
            dtfInstructivo.to_excel(writer, sheet_name='INSTRUCTIVO', index=False)
            dtfProductos.to_excel(writer, sheet_name='CATALOGO_PRODUCTOS', index=False)
            dtfBodegas.to_excel(writer, sheet_name='CATALOGO_BODEGAS', index=False)
            fncAgregarAnchoColumna(writer, False, dtfHistoricoAjustesInventario, 'PLANTILLA_AJUSTES_INVENTARIO')
            fncAgregarAnchoColumna(writer, True, dtfInstructivo, 'INSTRUCTIVO')
            fncAgregarAnchoColumna(writer, False, dtfProductos, 'CATALOGO_PRODUCTOS')
            fncAgregarAnchoColumna(writer, False, dtfBodegas, 'CATALOGO_BODEGAS')
            fncAgregarComentarioCeldas(writer, 'PLANTILLA_AJUSTES_INVENTARIO', lstCeldaAjustesInventario, lstComentariosAjustesInventarios)
        return response

''' 8.3 Vista para importar ajustes de inventario'''
class clsImportarAjustesInventarioViw(LoginRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/importar_ajustes_inventario.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lstHistoricoAjustesInventario = [
            'Bodega',
            'Tipo de ajuste',
            'Código producto',
            'Cantidad',
            'Costo total',
            'Lote',
            'Fecha de vencimiento'
        ]
        tplHistoricoAjustesInventario = (
            ((False,), (True, 10), (True, 1), (True, clsCatalogoBodegasMdl)),
            ((False,), (True, 2), (True, 1), (False,), (True, ('EN', 'SA'))),
            ((False,), (True, 10), (True, 1), (True, clsCatalogoProductosMdl)),
            ((True, int), (True, 5), (True,1), (False,)),
            ((True, float), (True, 30), (True, 1), (False,)),
            ((False,), (True, 100), (True, 1), (False,)),
            ((True, Timestamp), (True, 20), (True, 1), (False,)),
            )
        try:
            action = request.POST['action']
            jsnData = {}
            if action == 'frmCargarArchivojsn':
                filAjustesInventario = request.FILES['file']
                if str(filAjustesInventario).endswith('.xlsx'):
                    dtfHistoricoAjustesInventario = pd.read_excel(filAjustesInventario)
                    dtfHistoricoAjustesInventario = dtfHistoricoAjustesInventario.fillna(0)
                    lstPruebaAjuste= [(fncValidaAjustebol(dtfHistoricoAjustesInventario.iloc[i]['Código producto'], 
                    dtfHistoricoAjustesInventario.iloc[i]['Bodega'], dtfHistoricoAjustesInventario.iloc[i]['Lote'], 
                    dtfHistoricoAjustesInventario.iloc[i]['Cantidad'], bolTipoAjuste= False), i)\
                        for i, val in enumerate(dtfHistoricoAjustesInventario['Código producto'].unique())\
                            if dtfHistoricoAjustesInventario.iloc[i]['Tipo de ajuste']== 'SA']
                    lstAjusteValida= [('Tipo de ajuste', i[1], 'No hay inventario en bodega para descontar unidades de ajuste',
                    dtfHistoricoAjustesInventario.iloc[i[1]]['Tipo de ajuste']) for i in lstPruebaAjuste if i[0]== False]
                    lstValidarAjustesInventario = [ fncValidarImportacionlst(dtfHistoricoAjustesInventario, i, j) for (i, j) in zip(lstHistoricoAjustesInventario, tplHistoricoAjustesInventario) ]
                    lstValidarAjustesInventario = [ i for n in lstValidarAjustesInventario for i in n ]
                    for i in lstAjusteValida: lstValidarAjustesInventario.append(i)
                    dctValidaciones = {}
                    if len(lstValidarAjustesInventario):
                        dtfHistoricoAjustesInventario.loc[:,'Fecha de vencimiento'] = dtfHistoricoAjustesInventario['Fecha de vencimiento'].astype(str)
                        dctValidaciones['dtfHistoricoAjustesInventarioError'] = dtfHistoricoAjustesInventario.to_json(orient="split")
                        dctValidaciones['lstValidarAjustesInventario'] = lstValidarAjustesInventario
                    if len(dctValidaciones):
                        jsnData['dctValidaciones'] = dctValidaciones
                        jsnData['strError'] = 'El archivo presenta errores, ¿desea descargarlos?'
                        response = JsonResponse(jsnData, safe=False)
                    else:
                        with transaction.atomic():
                            qrsAjusteInventario = clsAjusteInventarioMdl()           
                            qrsAjusteInventario.total_cost = float(dtfHistoricoAjustesInventario['Costo total'].sum())
                            qrsAjusteInventario.save()
                            for ajuste_inventario in (dtfHistoricoAjustesInventario.values.tolist()):
                                clsDetalleAjusteInventarioMdl.objects.create(
                                doc_number_id= qrsAjusteInventario.id,
                                store_id= int(ajuste_inventario[0]),
                                type= str(ajuste_inventario[1]),
                                product_code_id= int(ajuste_inventario[2]),
                                batch= str(ajuste_inventario[5]),
                                expiration_date= datetime.now()+ timedelta(weeks= 520) if ajuste_inventario[6]== 0.0\
                                    else datetime.strptime(str(ajuste_inventario[6]), '%Y-%m-%d %H:%M:%S'),
                                quantity= int(ajuste_inventario[3]),
                                unitary_cost= float(ajuste_inventario[4]/ int(ajuste_inventario[3])),
                                total_cost= float(ajuste_inventario[4])
                                )
                        dtfActualizaSaldo= dtfHistoricoAjustesInventario.rename(columns= {'Bodega': 'store_id', 'Tipo de ajuste': 'type',
                        'Código producto': 'product_code_id', 'Cantidad': 'quantity', 'Costo total': 'total_cost', 'Lote': 'batch',
                        'Fecha de vencimiento': 'expiration_date'})
                        strCatalogo= 'SELECT id, cost_pu, split FROM modulo_configuracion_clscatalogoproductosmdl WHERE id= %s'
                        lstConsulta= [fncConsultalst(strCatalogo, [i]) for i in dtfActualizaSaldo['product_code_id'].unique()]
                        lstDatos= [i[0] for i in lstConsulta]
                        intIdentificacion= fncConsultalst('SELECT id_number FROM modulo_configuracion_clsperfilempresamdl', [])[0][0]
                        strConsecutivo= fncConsultalst('SELECT doc_number FROM modulo_configuracion_clsajusteinventariomdl', 
                        [])[- 1][0]
                        datFechaCreacion= fncConsultalst('SELECT creation_date FROM modulo_configuracion_clsajusteinventariomdl', 
                        [])[- 1][0]
                        dtfCatalogo= pd.DataFrame(lstDatos, columns= ['product_code_id', 'cost_pu', 'split'])
                        dtfActualizaSaldo= dtfActualizaSaldo.merge(dtfCatalogo, how= 'left', on= 'product_code_id')
                        dtfActualizaSaldo= dtfActualizaSaldo.assign(doc_number= strConsecutivo, creation_date= datFechaCreacion, 
                        unitary_cost= dtfActualizaSaldo['cost_pu']/ dtfActualizaSaldo['split'], condition= 'EN', 
                        identification= intIdentificacion, user_id_id= request.user.id)
                        dtfActualizaSaldo.drop(['cost_pu', 'split'], axis= 1, inplace= True)
                        fncActualizaSaldo('Ajuste_De_Inventario', dtfActualizaSaldo)                                
                        jsnData['success'] = '¡Se ha cargado el archivo a su base de datos con éxito!'
                        response = JsonResponse(jsnData, safe=False)
                else:
                    jsnData['error'] = 'Compruebe el formato del archivo'
                    response = JsonResponse(jsnData, safe=False)
            elif action == 'btnArchivoErroresjsn':
                dtfHistoricoAjustesInventarioError = None
                dctValidaciones = json.loads(request.POST['dctValidaciones'])
                if 'dtfHistoricoAjustesInventarioError' in dctValidaciones:
                    dtfHistoricoAjustesInventarioError = pd.read_json(dctValidaciones['dtfHistoricoAjustesInventarioError'], orient='split')
                    lstValidarAjustesInventario = dctValidaciones['lstValidarAjustesInventario']
                    lstFilasAjustesInventarioError = list( dict.fromkeys([ i[1] for i in lstValidarAjustesInventario ]))
                    dtfHistoricoAjustesInventarioError = fncAgregarErroresDataframedtf(dtfHistoricoAjustesInventarioError, lstValidarAjustesInventario, lstFilasAjustesInventarioError)
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename="errores_historico_pedidos.xlsx"'
                with pd.ExcelWriter(response) as writer:
                    if dtfHistoricoAjustesInventarioError is not None:
                        dtfHistoricoAjustesInventarioError.to_excel(writer, sheet_name='AJUSTES_INVENTARIO_ERROR', index=False)
                        fncAgregarFormatoColumnasError(writer, lstValidarAjustesInventario, 'AJUSTES_INVENTARIO_ERROR', lstHistoricoAjustesInventario)
                        fncAgregarAnchoColumna(writer, False, dtfHistoricoAjustesInventarioError, 'AJUSTES_INVENTARIO_ERROR')
        except Exception as e:
            jsnData['error'] = str(e)
            response = JsonResponse(jsnData, safe=False)
        return response

''' 8.4 Vista para crear ajuste de inventario'''
class clsCrearAjusteInventarioViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    template_name = 'modulo_configuracion/crear_ajuste_inventario.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'jsnBuscarBodega':
                data = []
                jsnTerm = request.POST['term'].strip()
                if len(jsnTerm):
                    qrsBodega = clsCatalogoBodegasMdl.objects.filter(Q(warehouse_name__icontains=jsnTerm) | Q(contact_name__icontains=jsnTerm))[0:10]
                for i in qrsBodega:
                    item = i.toJSON()
                    item['text'] = i.warehouse_name
                    data.append(item)
            elif action == 'jsnBucarProducto':
                data = []
                jsnTerm = request.POST['term'].strip()
                if len(jsnTerm):
                    qrsProducto = clsCatalogoProductosMdl.objects.filter(Q(product_desc__icontains=jsnTerm) | Q(id__icontains=jsnTerm))[0:10]
                for i in qrsProducto:
                    item = i.toJSON()
                    item['text'] = i.product_desc
                    data.append(item)
            elif action == 'jsnValidarAjuste':
                dctVariables = json.loads(request.POST['dctVariables'])
                dctLstAjustesInventario = json.loads(request.POST['dctLstAjustesInventario'])
                qrsSaldosInventario = clsSaldosInventarioMdl.objects.all()
                if not qrsSaldosInventario:
                    dtfsaldosInventario = qrsSaldosInventario.to_dataframe()
                else:
                    srlSaldosInventario = clsSaldosInventarioMdlSerializador(qrsSaldosInventario, many=True)
                    dtfsaldosInventario = pd.DataFrame(srlSaldosInventario.data)
                bolAjuste = fncValidaAjustebol(
                    dctVariables['intIdProducto'],
                    dctVariables['intIdBodega'],
                    # dctVariables['strLote'],
                    '0',
                    int(dctVariables['intCantidad']),
                    bolTipoAjuste = True if dctVariables['strTipoAjusteId'] == 'EN' else False
                    )
                if bolAjuste == True:
                    if len(dctLstAjustesInventario):
                        dctVariables.pop('intCantidad', None)
                        dctVariables.pop('fltCostoUnitario', None)
                        dctVariables.pop('fltCostoTotalUnitario', None)
                        for i in dctLstAjustesInventario['lstAjustesInventario']:
                            i.pop('intCantidad', None)
                            i.pop('fltCostoUnitario', None)
                            i.pop('fltCostoTotalUnitario', None)
                            if dctVariables == i:
                                data['error'] = 'El producto ya existe en la tabla'
                                return JsonResponse(data, safe=False)
                    else:
                        pass
                elif bolAjuste == False:
                    data['error'] = 'No se puede realizar este movimiento'
                    return JsonResponse(data, safe=False)
            elif action == 'jsnGuardarAjuste':
                lstOrdenColumnas = [
                        'creation_date', 'doc_number', 'type', 'quantity', 
                        'batch', 'expiration_date', 'unitary_cost', 'total_cost', 'crossing_doc',
                        'condition', 'identification', 'product_code_id', 'store_id', 'user_id_id'
                        ]
                qrsclsPerfilEmpresaMdl = clsPerfilEmpresaMdl.objects.all()
                intIdentificacionusuario = [i.jsnObtenerIdentificacion() for i in qrsclsPerfilEmpresaMdl]
                dctLstAjustesInventario = json.loads(request.POST['dctLstAjustesInventario'])
                fltCostoTotalAjuste = dctLstAjustesInventario['fltCostoTotal']
                lstAjustesInventario = dctLstAjustesInventario['lstAjustesInventario']
                with transaction.atomic():
                    qrsAjusteInventario = clsAjusteInventarioMdl()
                    qrsAjusteInventario.total_cost = float(fltCostoTotalAjuste)
                    qrsAjusteInventario.save()
                    for i in lstAjustesInventario:
                        qrsDetalleAjuste = clsDetalleAjusteInventarioMdl()
                        qrsDetalleAjuste.doc_number_id = qrsAjusteInventario.id                        
                        qrsDetalleAjuste.store_id = i['intIdBodega']                        
                        qrsDetalleAjuste.type = i['strTipoAjusteId']
                        qrsDetalleAjuste.product_code_id = i['intIdProducto']                        
                        qrsDetalleAjuste.batch = i['strLote']
                        qrsDetalleAjuste.expiration_date = datetime.strptime(i['datFechaVencimiento'],"%d/%m/%Y")
                        qrsDetalleAjuste.quantity = int(i['intCantidad'])
                        qrsDetalleAjuste.unitary_cost = float(i['fltCostoUnitario'])
                        qrsDetalleAjuste.total_cost = float(i['fltCostoTotalUnitario'])
                        qrsDetalleAjuste.save()
                qrsAjusteInv = clsAjusteInventarioMdl.objects.filter(id=qrsAjusteInventario.id)
                srlAjusteInventario = clsAjusteInventarioMdlSerializador(qrsAjusteInv, many=True)
                dtfAjusteInventario = pd.DataFrame(srlAjusteInventario.data)
                dtfAjusteInventario = dtfAjusteInventario.rename(columns={'id':'id_ajuste', 'total_cost': 'cost_total', 'user_creation': 'user_id'})
                qrsDetalleAjusteInventario = clsDetalleAjusteInventarioMdl.objects.filter(doc_number_id=qrsAjusteInventario.id)
                srlDetalleAjusteInventario = clsDetalleAjusteInventarioMdlSerializador(qrsDetalleAjusteInventario, many=True)
                dtfDetalleAjusteInventario = pd.DataFrame(srlDetalleAjusteInventario.data)
                dtfDetalleAjusteInventario = dtfDetalleAjusteInventario.rename(columns={'doc_number':'id_ajuste'})
                dtfAjusteInventario = dtfAjusteInventario.merge(dtfDetalleAjusteInventario, on='id_ajuste', how='outer')
                dtfAjusteInventario = dtfAjusteInventario.drop(['id_ajuste', 'cost_total', 'id'], axis=1)
                dtfAjusteInventario = dtfAjusteInventario.assign(identification=intIdentificacionusuario[0]['id_number'], crossing_doc= '')
                dtfAjusteInventario.rename(columns= {'product_code': 'product_code_id', 'store': 'store_id', 'user_id': 'user_id_id'}, inplace= True)
                dtfAjusteInventario = dtfAjusteInventario.reindex(columns = lstOrdenColumnas)
                dtfAjusteInventario.at[0, 'batch']= '0'
                dtfAjusteInventario.at[0, 'expiration_date']= '0'
                strActualizarSaldo = fncActualizaSaldo('Ajuste_De_Inventario', dtfAjusteInventario)
                if strActualizarSaldo == 'se actualizó el histórico y la bodega':
                    data['msg'] = 'Se han actualizado el historico de movimientos y el saldo de inventarios'
                else:
                    data['error'] = 'No ha ingresado a ninguna opción'    
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear ajuste de inventario'
        context['form'] = clsAjustesInventarioFrm()
        context['action'] = 'add'
        return context

#################################################################################################
# VISTA PARA PRUEBAS
#################################################################################################
''' Vista para exportar plantilla de historico de movimientos'''
class clsExportarPlantillaPrueba(APIView):

    def get(self, request):
        lstConsultas = [clsEntradasAlmacenMdl, clsDetalleEntradaAlmacen,
                        clsDevolucionesClienteMdl, clsDetalleDevolucionesClienteMdl,
                        clsDevolucionesProveedorMdl, clsDetalleDevolucionesProveedorMdl,
                        clsSalidasAlmacenMdl, clsDetalleSalidasAlmacenMdl,
                        clsObsequiosMdl, clsDetalleObsequiosMdl,
                        clsTrasladosBodegasMdl, clsDetalleTrasladosBodegaMdl,
                    ]
        lstSerializadores = [clsEntradasAlmacenMdlSerializador, clsDetalleEntradaAlmacenSerializador,
                            clsDevolucionesClienteMdlSerializador, clsDetalleDevolucionesClienteMdlSerializador,
                            clsDevolucionesProveedorMdlSerializador, clsDetalleDevolucionesProveedorMdlSerializador,
                            clsSalidasAlmacenMdlSerializador, clsDetalleSalidasAlmacenMdlSerializador,
                            clsObsequiosMdlSerializador, clsDetalleObsequiosMdlSerializador,
                            clsTrasladosBodegasMdlSerializador, clsDetalleTrasladosBodegaMdlSerializador
                        ]
        lstClaves = ['id', 'doc_number', 'id', 'doc_number', 'id', 'doc_number', 'id', 'doc_number', 'id', 'doc_number', 'id', 'doc_number']
        lstNuevasClaves = ['id_entrada', 'id_entrada', 'id_devolucion', 'id_devolucion', 'id_devolucion', 'id_devolucion', 'id_salida', 'id_salida', 'id_obsequio', 'id_obsequio', 'id_traslado', 'id_traslado']
        lstOrdenColumnas1 = [
            'creation_date', 'doc_number', 'product_code', 'quantity', 
            'batch', 'expiration_date', 'unitary_cost', 'total_cost', 
            'crossing_doc', 'condition', 'store', 'identification', 'user_id'
            ]
        lstOrdenColumnas2 = [
            'creation_date', 'doc_number', 'product_code', 'quantity', 
            'batch', 'expiration_date', 'unitary_cost', 'total_cost', 
            'condition', 'store', 'identification', 'user_id'
            ]
        lstOrdenColumnas3 = [
            'creation_date', 'doc_number', 'type', 'product_code', 'quantity', 
            'batch', 'expiration_date', 'unitary_cost', 'total_cost', 
            'condition', 'store', 'identification', 'user_id'
            ]
        lstColumnasExcluir = ['user_update', 'update_date', 'total_cost']
        lstColumnasExcluirDevoluciones = ['user_update', 'update_date', 'returnin_type', 'total_cost']
        lstColumnasExcluirSalidas = ['user_creation', 'user_update', 'update_date', 'credit_state', 'taxes', 'discount', 'total_price', 'total_amount', 'total_cost', 'value_paid']
        lstColumnasExcluirDetalleSalidas = ['unit_price', 'taxes', 'discount', 'total_price', 'total_amount']
        lstDataFrames = fncRetornarListaDataFrame(lstConsultas, lstSerializadores, lstClaves, lstNuevasClaves)
        # Entradas de almacén
        if 'user_update' in lstDataFrames[0]:
            dtfEntradasAlmacen = lstDataFrames[0].drop(lstColumnasExcluir, axis=1)
            dtfEntradasAlmacen = dtfEntradasAlmacen.merge(lstDataFrames[1] + ['state'], on='id_entrada', how='outer')
        else:
            dtfEntradasAlmacen = lstDataFrames[0].merge(lstDataFrames[1], on='id_entrada', how='outer')
        dtfEntradasAlmacen = dtfEntradasAlmacen.drop(['id_entrada', 'id'], axis=1)
        dtfEntradasAlmacen = dtfEntradasAlmacen.rename(columns={'user_creation':'user_id'})
        dtfEntradasAlmacen = dtfEntradasAlmacen.reindex(columns = lstOrdenColumnas1)
        # Devoluciones cliente
        if 'user_update' in lstDataFrames[2]:
            dtfDevolucionesCliente = lstDataFrames[2].drop(lstColumnasExcluirDevoluciones, axis=1)
            dtfDevolucionesCliente = dtfDevolucionesCliente.merge(lstDataFrames[3], on='id_devolucion', how='outer')
        else:
            dtfDevolucionesCliente = lstDataFrames[2].merge(lstDataFrames[3], on='id_devolucion', how='outer')
        dtfDevolucionesCliente = dtfDevolucionesCliente.drop(['id_devolucion', 'id'], axis=1)
        dtfDevolucionesCliente = dtfDevolucionesCliente.rename(columns={'user_creation':'user_id'})
        dtfDevolucionesCliente = dtfDevolucionesCliente.reindex(columns = lstOrdenColumnas1)
        # Devoluciones proveedor
        if 'user_update' in lstDataFrames[4]:
            dtfDevolucionesProveedor = lstDataFrames[4].drop(lstColumnasExcluirDevoluciones, axis=1)
            dtfDevolucionesProveedor = dtfDevolucionesProveedor.merge(lstDataFrames[5], on='id_devolucion', how='outer')
        else:
            dtfDevolucionesProveedor = lstDataFrames[4].merge(lstDataFrames[5], on='id_devolucion', how='outer')
        dtfDevolucionesProveedor = dtfDevolucionesProveedor.drop(['id_devolucion', 'id'], axis=1)
        dtfDevolucionesProveedor = dtfDevolucionesProveedor.rename(columns={'user_creation':'user_id'})
        dtfDevolucionesProveedor = dtfDevolucionesProveedor.reindex(columns = lstOrdenColumnas1)
        
        # Salidas de almacén
        if 'user_update' in lstDataFrames[6]:
            dtfSalidasAlmacen = lstDataFrames[6].drop(lstColumnasExcluirSalidas, axis=1)
            dtfSalidasAlmacen = dtfSalidasAlmacen.merge(lstDataFrames[7], on='id_salida', how='outer')
        else:
            dtfSalidasAlmacen = lstDataFrames[6].merge(lstDataFrames[7], on='id_salida', how='outer')
        dtfSalidasAlmacen = dtfSalidasAlmacen.drop(['id_salida', 'id'], axis=1)
        dtfSalidasAlmacen = dtfSalidasAlmacen.rename(columns={'user_creation':'user_id'})
        dtfSalidasAlmacen = dtfSalidasAlmacen.reindex(columns = lstOrdenColumnas1)
        
        # Obsequios
        if 'user_update' in lstDataFrames[8]:
            dtfObsequios = lstDataFrames[8].drop(lstColumnasExcluir, axis=1)
            dtfObsequios = dtfObsequios.merge(lstDataFrames[9], on='id_obsequio', how='outer')
        else:
            dtfObsequios = lstDataFrames[8].merge(lstDataFrames[9], on='id_obsequio', how='outer')
        dtfObsequios = dtfObsequios.drop(['id_obsequio', 'id'], axis=1)
        dtfObsequios = dtfObsequios.rename(columns={'user_creation':'user_id'})
        dtfObsequios = dtfObsequios.reindex(columns = lstOrdenColumnas2)
        
        # Traslados
        if 'user_update' in lstDataFrames[10]:
            dtfTraslados = lstDataFrames[10].drop(lstColumnasExcluir, axis=1)
            dtfTraslados = dtfTraslados.merge(lstDataFrames[11], on='id_traslado', how='outer')
        else:
            dtfTraslados = lstDataFrames[10].merge(lstDataFrames[11], on='id_traslado', how='outer')
        dtfTraslados = dtfTraslados.drop(['id_traslado', 'id'], axis=1)
        dtfTraslados = dtfTraslados.rename(columns={'user_creation':'user_id'})
        dtfTraslados = dtfTraslados.reindex(columns = lstOrdenColumnas3)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="historico_movimientos.xlsx"'
        with pd.ExcelWriter(response) as writer:
            dtfEntradasAlmacen.to_excel(writer, sheet_name='ENTRADAS_ALMACEN', index=False)
            dtfDevolucionesCliente.to_excel(writer, sheet_name='DEVOLUCIONES_CLIENTE', index=False)
            dtfDevolucionesProveedor.to_excel(writer, sheet_name='DEVOLUCIONES_PROVEEDOR', index=False)
            dtfSalidasAlmacen.to_excel(writer, sheet_name='SALIDAS_ALMACEN', index=False)
            dtfObsequios.to_excel(writer, sheet_name='OBSEQUIOS', index=False)
            dtfTraslados.to_excel(writer, sheet_name='TRASLADOS_BODEGA', index=False)
        return response