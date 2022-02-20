# Python libraries
import json

# Django libraries
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group, Permission
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView, CreateView, ListView, UpdateView, TemplateView, RedirectView
from django.forms import model_to_dict
from django.db import transaction

# Django-rest libraries
from rest_framework.generics import ListAPIView

# Apps functions
import biapp.settings as setting
from biapp import settings
from .models import User
from .forms import *
from apps.mixins import ValidatePermissionRequiredMixin
from .api.serializers import *

Permission.__str__ = lambda self: '%s' % (self.name)

################################################################################################
############################### VISTAS PARAMETRIZACIÓN USUARIOS ##############################
################################################################################################

#################################################################################################
# 1. INGRESO Y SALIDA DEL SISTEMA
#################################################################################################
''' 1.1 Vista para el ingreso al sistema'''
class clsLoginViw(LoginView):
    template_name = 'usuarios/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

''' 1.2 Vista para salir del sistema'''
class clsLogoutViw(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

#################################################################################################
# 2. PARAMETRIZACIÓN DE GRUPOS (CREAR, EDITAR, LISTAR Y ELIMINAR)
#################################################################################################
''' 2.1 Vista para crear grupo'''
class clsCrearGrupoViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Group
    form_class = UserGroupForm
    template_name = 'usuarios/crear_grupo.html'
    success_url = reverse_lazy('usuarios:crear_grupos_usuarios')
    permission_required = 'add_group'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']     
            if action == 'frmCrearGrupojsn':
                lstPermisos = []
                bolTodosLosPermisos = False
                bolPermisosAdmin = False
                lstPermisosAdmin = None
                bolComercial = False
                lstPermisosComercial = None
                bolPermisosCompras = False
                lstPermisosCompras = None
                bolPermisosLogistica = False
                lstPermisosLogistica = None
                strNombreGrupo = request.POST['name']
                lstComercial = [ int(i) for i in request.POST.getlist('com_permission') ]
                lstCompras = [ int(i) for i in request.POST.getlist('pur_permission') ]
                lstLogistica = [ int(i) for i in request.POST.getlist('log_permission') ]
                lstAdministrador = [ int(i) for i in request.POST.getlist('adm_permission') ]
                if 'all' in request.POST:
                    for i in Permission.objects.filter(codename__icontains="bia"):
                        if i not in lstPermisos:
                            lstPermisos.append(i.id)
                    bolTodosLosPermisos = True
                if 'admin' in request.POST:
                    lstPermisosAdmin = []
                    for i in Permission.objects.filter(codename__icontains="bia_adm"):
                        if i not in lstPermisos:
                            lstPermisos.append(i.id)
                            lstPermisosAdmin.append(i) 
                    bolPermisosAdmin = True
                if 'commercial' in request.POST:
                    lstPermisosComercial = []
                    for i in Permission.objects.filter(codename__icontains="bia_com"):
                        if i not in lstPermisos:
                            lstPermisosComercial.append(i)
                            lstPermisos.append(i.id)
                    bolComercial = True
                if 'purchase' in request.POST:
                    lstPermisosCompras = []
                    for i in Permission.objects.filter(codename__icontains="bia_pur"):
                        if i not in lstPermisos:
                            lstPermisos.append(i.id)
                            lstPermisosCompras.append(i)
                    bolPermisosCompras = True
                if 'logistics' in request.POST:
                    lstPermisosLogistica = []
                    for i in Permission.objects.filter(codename__icontains="bia_log"):
                        if i not in lstPermisos:
                            lstPermisos.append(i.id)
                            lstPermisosLogistica.append(i)
                    bolPermisosLogistica = True
                if lstComercial:
                    lstPermisosComercial = []
                    for i in lstComercial:
                        lstPermisosComercial.append(i)
                        lstPermisos.append(i)    
                if lstCompras:
                    lstPermisosCompras = []
                    for i in lstCompras:
                        lstPermisos.append(i)
                        lstPermisosCompras.append(i)
                if lstLogistica:
                    lstPermisosLogistica = []
                    for i in lstLogistica:
                        lstPermisos.append(i)
                        lstPermisosLogistica.append(i)
                if lstAdministrador:
                    lstPermisosAdmin = []
                    for i in lstAdministrador:
                        lstPermisos.append(i)
                        lstPermisosAdmin.append(i) 
                if not len(lstPermisos):
                     jsnData['error'] = 'Debe seleccionar al menos un permiso para el grupo'
                else:
                    with transaction.atomic():
                        group = Group()
                        group.name = strNombreGrupo
                        group.commercial = bolComercial
                        group.purchase = bolPermisosCompras
                        group.logistics = bolPermisosLogistica
                        group.admin = bolPermisosAdmin
                        group.all = bolTodosLosPermisos
                        group.save()
                        if lstPermisosComercial is not None:
                            group.com_permission.set(lstPermisosComercial)
                        if lstPermisosCompras is not None:
                            group.pur_permission.set(lstPermisosCompras)
                        if lstPermisosLogistica is not None:
                            group.log_permission.set(lstPermisosLogistica)
                        if lstPermisosAdmin is not None:
                            group.adm_permission.set(lstPermisosAdmin)
                        group.permissions.set(lstPermisos)
            elif action == 'slcBuscarPermisosComercialjsn':
                jsnData = []
                qrsPermisos =  Permission.objects.filter(codename__icontains="bia_com")
                for i in qrsPermisos:
                    dctJsn = model_to_dict(i)
                    dctJsn['text'] = i.name
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarPermisosComprasjsn':
                jsnData = []
                qrsPermisos =  Permission.objects.filter(codename__icontains="bia_pur")
                for i in qrsPermisos:
                    dctJsn = model_to_dict(i)
                    dctJsn['text'] = i.name
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarPermisosLogisticajsn':
                jsnData = []
                qrsPermisos =  Permission.objects.filter(codename__icontains="bia_log")
                for i in qrsPermisos:
                    dctJsn = model_to_dict(i)
                    dctJsn['text'] = i.name
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarPermisosAdministradorjsn':
                jsnData = []
                qrsPermisos =  Permission.objects.filter(codename__icontains="bia_adm")
                for i in qrsPermisos:
                    dctJsn = model_to_dict(i)
                    dctJsn['text'] = i.name
                    jsnData.append(dctJsn)
        except Exception as e:
            if str(e) == 'UNIQUE constraint failed: auth_group.name':
                jsnData['error'] = 'El nombre de grupo que ingreso ya existe, por favor ingrese uno diferente'
            else:
                jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear grupos y permisos'
        context['user_create_url'] = reverse_lazy('usuarios:crear_usuarios')
        context['list_url'] = reverse_lazy('usuarios:listar_grupos')
        context['list_user_url'] = reverse_lazy('usuarios:listar_usuarios')
        context['action'] = 'frmCrearGrupojsn'
        return context

''' 2.2 Vista para editar grupo'''
class clsEditarGrupoViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Group
    form_class = UserGroupForm
    template_name = 'usuarios/editar_grupos.html'
    success_url = reverse_lazy('usuarios:crear_grupos_usuarios')
    url_redirect = success_url
    permission_required = 'change_group'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmEditarGrupojsn':
                lstPermisos = []
                bolTodosLosPermisos = False
                bolPermisosAdmin = False
                lstPermisosAdmin = None
                bolComercial = False
                lstPermisosComercial = None
                bolPermisosCompras = False
                lstPermisosCompras = None
                bolPermisosLogistica = False
                lstPermisosLogistica = None
                strNombreGrupo = request.POST['name']
                lstComercial = [ int(i) for i in request.POST.getlist('com_permission') ]
                lstCompras = [ int(i) for i in request.POST.getlist('pur_permission') ]
                lstLogistica = [ int(i) for i in request.POST.getlist('log_permission') ]
                lstAdministrador = [ int(i) for i in request.POST.getlist('adm_permission') ]
                if 'all' in request.POST:
                    for i in Permission.objects.filter(codename__icontains="bia"):
                        if i not in lstPermisos:
                            lstPermisos.append(i.id)
                    bolTodosLosPermisos = True
                if 'admin' in request.POST:
                    lstPermisosAdmin = []
                    for i in Permission.objects.filter(codename__icontains="bia_adm"):
                        if i not in lstPermisos:
                            lstPermisos.append(i.id)
                            lstPermisosAdmin.append(i) 
                    bolPermisosAdmin = True
                if 'commercial' in request.POST:
                    lstPermisosComercial = []
                    for i in Permission.objects.filter(codename__icontains="bia_com"):
                        if i not in lstPermisos:
                            lstPermisosComercial.append(i)
                            lstPermisos.append(i.id)
                    bolComercial = True
                if 'purchase' in request.POST:
                    lstPermisosCompras = []
                    for i in Permission.objects.filter(codename__icontains="bia_pur"):
                        if i not in lstPermisos:
                            lstPermisos.append(i.id)
                            lstPermisosCompras.append(i)
                    bolPermisosCompras = True
                if 'logistics' in request.POST:
                    lstPermisosLogistica = []
                    for i in Permission.objects.filter(codename__icontains="bia_log"):
                        if i not in lstPermisos:
                            lstPermisos.append(i.id)
                            lstPermisosLogistica.append(i)
                    bolPermisosLogistica = True
                if lstComercial:
                    lstPermisosComercial = []
                    for i in lstComercial:
                        lstPermisosComercial.append(i)
                        lstPermisos.append(i)    
                if lstCompras:
                    lstPermisosCompras = []
                    for i in lstCompras:
                        lstPermisos.append(i)
                        lstPermisosCompras.append(i)
                if lstLogistica:
                    lstPermisosLogistica = []
                    for i in lstLogistica:
                        lstPermisos.append(i)
                        lstPermisosLogistica.append(i)
                if lstAdministrador:
                    lstPermisosAdmin = []
                    for i in lstAdministrador:
                        lstPermisos.append(i)
                        lstPermisosAdmin.append(i) 
                if not len(lstPermisos):
                     jsnData['error'] = 'Debe seleccionar al menos un permiso para el grupo'
                else:
                    with transaction.atomic():
                        group = Group.objects.get(pk=self.object.id)
                        group.name = strNombreGrupo
                        group.permissions.clear()
                        group.com_permission.clear()
                        group.pur_permission.clear()
                        group.log_permission.clear()
                        group.adm_permission.clear()
                        group.commercial = bolComercial
                        group.purchase = bolPermisosCompras
                        group.logistics = bolPermisosLogistica
                        group.admin = bolPermisosAdmin
                        group.all = bolTodosLosPermisos
                        group.save()
                        if lstPermisosComercial is not None:
                            group.com_permission.set(lstPermisosComercial)
                        if lstPermisosCompras is not None:
                            group.pur_permission.set(lstPermisosCompras)
                        if lstPermisosLogistica is not None:
                            group.log_permission.set(lstPermisosLogistica)
                        if lstPermisosAdmin is not None:
                            group.adm_permission.set(lstPermisosAdmin)
                        group.permissions.set(lstPermisos)
            elif action == 'slcBuscarPermisosComercialjsn':
                jsnData = []
                qrsPermisos =  Permission.objects.filter(codename__icontains="bia_com")
                for i in qrsPermisos:
                    dctJsn = model_to_dict(i)
                    dctJsn['text'] = i.name
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarPermisosComprasjsn':
                jsnData = []
                qrsPermisos =  Permission.objects.filter(codename__icontains="bia_pur")
                for i in qrsPermisos:
                    dctJsn = model_to_dict(i)
                    dctJsn['text'] = i.name
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarPermisosLogisticajsn':
                jsnData = []
                qrsPermisos =  Permission.objects.filter(codename__icontains="bia_log")
                for i in qrsPermisos:
                    dctJsn = model_to_dict(i)
                    dctJsn['text'] = i.name
                    jsnData.append(dctJsn)
            elif action == 'slcBuscarPermisosAdministradorjsn':
                jsnData = []
                qrsPermisos =  Permission.objects.filter(codename__icontains="bia_adm")
                for i in qrsPermisos:
                    dctJsn = model_to_dict(i)
                    dctJsn['text'] = i.name
                    jsnData.append(dctJsn)
        except Exception as e:
            if str(e) == 'UNIQUE constraint failed: auth_group.name':
                jsnData['error'] = 'El nombre de grupo que ingreso ya existe, por favor ingrese uno diferente'
            else:
                jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar grupos y permisos'
        context['group_create_url'] = self.success_url
        context['user_create_url'] = reverse_lazy('usuarios:crear_usuarios')
        context['list_url'] = reverse_lazy('usuarios:listar_grupos')
        context['list_user_url'] = reverse_lazy('usuarios:listar_usuarios')
        context['action'] = 'frmEditarGrupojsn'
        return context

''' 2.3 Vista para listar y eliminar grupos'''
class clsListarGrupoViw(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/listar_grupos.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'btnEliminarGrupojsn':
                qrsGrupos = Group.objects.get(pk=request.POST['id'])
                qrsGrupos.delete()
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query_group'] = Group.objects.all()
        context['title_table'] = 'Grupos'
        context['create_url'] = reverse_lazy('usuarios:crear_grupos_usuarios')
        context['user_create_url'] = reverse_lazy('usuarios:crear_usuarios')
        context['list_user_url'] = reverse_lazy('usuarios:listar_usuarios')
        return context

#################################################################################################
# 3. PARAMETRIZACIÓN DE USUARIOS (CREAR, EDITAR, LISTAR Y ELIMINAR)
#################################################################################################
''' 3.1 Vista para crear usuario'''
class clsCrearUsuarioViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'usuarios/crear_usuario.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    permission_required = 'bia_add_user'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmCrearUsuariojsn':
                print('si')
                frmCrearUsuario = self.get_form()
                jsnData = frmCrearUsuario.save()
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear usuario'
        context['list_url'] = self.success_url
        context['group_create_url'] = reverse_lazy('usuarios:crear_grupos_usuarios')
        context['list_group_url'] = reverse_lazy('usuarios:listar_grupos')
        context['action'] = 'frmCrearUsuariojsn'
        return context

''' 3.2 Vista para editar usuario'''
class clsEditarUsuarioViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'usuarios/crear_usuario.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    permission_required = 'bia_change_user'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self,request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'frmEditarUsuariojsn':
                frmEditarUsuario = self.get_form()
                jsnData = frmEditarUsuario.save()
            else:
                jsnData['error'] = frmEditarUsuario.errors
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar usuario'
        context['list_url'] = self.success_url
        context['create_url'] = reverse_lazy('usuarios:listar_usuarios')
        context['action'] = 'frmEditarUsuariojsn'
        return context

''' 3.3 Vista para listar y eliminar usuarios'''
class clsListarUsuarioViw(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = User
    template_name = 'usuarios/listar_usuarios.html'
    permission_required = 'bia_view_user'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        jsnData = {}
        try:
            action = request.POST['action']
            if action == 'tblListarUsuariosjsn':
                jsnData = []
                for i in User.objects.filter(is_staff=False):
                    jsnData.append(i.toJSON())
                for i in range(0, len(jsnData)):
                    jsnData[i]['n'] = i + 1
            elif action == 'btnEliminarUsuariojsn':
                qrsUsuario = User.objects.get(pk=request.POST['id'])
                if qrsUsuario.is_active == False:
                    qrsUsuario.is_active = True
                    qrsUsuario.save()
                else:
                    qrsUsuario.is_active = False
                    qrsUsuario.save()
            else:
                jsnData['error'] = 'Ha ocurrido un error'
        except Exception as e:
            jsnData['error'] = str(e)
        return JsonResponse(jsnData, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_table'] = 'Tabla de usuarios'
        context['create_url'] = reverse_lazy('usuarios:crear_usuarios')
        context['group_create_url'] = reverse_lazy('usuarios:crear_grupos_usuarios')
        context['list_group_url'] = reverse_lazy('usuarios:listar_grupos')
        return context

