from django.shortcuts import render, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View,TemplateView,ListView,UpdateView,CreateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apps.usuario.models import User
from apps.modulo_configuracion.models import *
from apps.usuario.models import User

class Home(TemplateView):
    template_name = 'bia/home.html'

def notificaciones(request):
    return render(request, 'bia/notificaciones.html')

def perfil_usuario(request):
    return render(request, 'bia/perfil_usuarios.html')

def modulo_comercial(request):
    return render(request, 'bia/modulo_comercial.html')

def modulo_compras(request):
    return render(request, 'bia/modulo_compras.html')

def modulo_almacen(request):
    return render(request, 'bia/modulo_almacen.html')

def modulo_indicadores(request):
    return render(request, 'bia/modulo_indicadores.html')

def modulo_reportes(request):
    return render(request, 'bia/modulo_reportes.html')

''' Vista para opciones producto'''
class modulo_configuracion(LoginRequiredMixin, TemplateView):
    template_name = 'bia/modulo_configuracion.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'btnUsuariosPermisosjsn':
                qrsEmpresa =  clsPerfilEmpresaMdl.objects.all()
                if not qrsEmpresa:
                    msg = 'Para establecer usuarios y permisos debe parámetrizar el perfil de su empresa'
                    data['error'] = msg
                else:
                    data['success'] = 'success'
            elif action == 'btnCatalogoProductosjsn':
                qrsUsuarios =  User.objects.filter(is_superuser=False)
                if not qrsUsuarios:
                    msg = 'Para establecer su cátalogo de productos debe parámetrizar sus usuarios y permisos'
                    data['error'] = msg
            elif action == 'btnCatalogoProveedoresjsn':
                qrsProductos =  clsCatalogoProductosMdl.objects.filter(state='AC')
                if not qrsProductos:
                    msg = 'Para establecer su catálogo de Proveedores debe parámetrizar sus productos'
                    data['error'] = msg
            elif action == 'btnCatalogoBodegasjsn':
                qrsProveedores =  clsCatalogoProveedoresMdl.objects.filter(state='AC')
                if not qrsProveedores:
                    msg = 'Para establecer su catálogo de bodegas debe parámetrizar sus proveedores'
                    data['error'] = msg
            elif action == 'btnListasPreciosjsn':
                qrsBodegas =  clsCatalogoBodegasMdl.objects.filter(state='AC')
                if not qrsBodegas:
                    msg = 'Para establecer sus listas de precios debe parámetrizar sus bodegas'
                    data['error'] = msg
            elif action == 'btnCatalogoClientesjsn':
                qrsListasPrecios =  clsListaPreciosMdl.objects.filter(state='AC')
                if not qrsListasPrecios:
                    msg = 'Para establecer su catáloo de clientes debe parámetrizar sus listas de precios'
                    data['error'] = msg
            elif action == 'btnTiemposEntregajsn':
                qrsCatalogoClientes =  clsCatalogoClientesMdl.objects.filter(state='AC')
                if not qrsCatalogoClientes:
                    msg = 'Para establecer tiempos de entrega debe parámetrizar sus clientes'
                    data['error'] = msg
            elif action == 'btnHistoricoMovimientosjsn':
                qrsCatalogoClientes =  clsCatalogoClientesMdl.objects.filter(state='AC')
                if not qrsCatalogoClientes:
                    msg = 'Para establecer su histórico de movimientos debe parámetrizar sus clientes'
                    data['error'] = msg
                historico = clsHistoricoPedidosMdl.objects.all()
                # elif len(historico):
                #     msg = 'Usted ya ha cargado un historico de movimientos, para cargar un nuevo historico genere un ticket de servicio'
                #     data['error'] = msg
            elif action == 'btnAjusteInventariosjsn':
                qrsCatalogoClientes =  clsCatalogoClientesMdl.objects.filter(state='AC')
                if not qrsCatalogoClientes:
                    msg = 'Para establecer sus ajustes iniciales debe parámetrizar sus clientes'
                    data['error'] = msg
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)