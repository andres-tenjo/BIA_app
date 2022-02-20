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

def modulo_logistica(request):
    return render(request, 'bia/modulo_logistica.html')

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
            if action == 'user':
                com =  clsPerfilEmpresaMdl.objects.all()
                if not com:
                    msg = 'Para continuar con la parametrización de usuarios debe parámetrizar el perfil de su empresa'
                    data['error'] = msg
            elif action == 'products':
                user =  User.objects.filter(is_superuser=False)
                if not user:
                    msg = 'Para continuar con la parametrización de Productos debe parámetrizar los usuarios'
                    data['error'] = msg
            elif action == 'suppliers':
                prod =  clsCatalogoProductosMdl.objects.filter(state='AC')
                if not prod:
                    msg = 'Para continuar con la parametrización de Proveedores debe parámetrizar los productos'
                    data['error'] = msg
            elif action == 'customers':
                supp =  clsCatalogoProveedoresMdl.objects.filter(state='AC')
                if not supp:
                    msg = 'Para continuar con la parametrización de Clientes debe parámetrizar los proveedores'
                    data['error'] = msg
            elif action == 'warehouse':
                cust =  clsCatalogoClientesMdl.objects.filter(state='AC')
                if not cust:
                    msg = 'Para continuar con la parametrización de Bodegas debe parámetrizar los clientes'
                    data['error'] = msg
            elif action == 'historico_movimientos':
                warehouse =  clsCatalogoBodegasMdl.objects.filter(state='AC')
                historico = clsHistoricoPedidosMdl.objects.all()
                if not warehouse:
                    msg = 'Para continuar con la parametrización del historico de movimientos debe parámetrizar las bodegas'
                    data['error'] = msg
                # elif len(historico):
                #     msg = 'Usted ya ha cargado un historico de movimientos, para cargar un nuevo historico genere un ticket de servicio'
                #     data['error'] = msg
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)