from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('notificaciones', login_required(notificaciones), name='notificaciones'),
    path('perfil_usuario', perfil_usuario, name='perfil_usuario'),
    path('modulo_comercial', modulo_comercial, name='modulo_comercial'),
    path('modulo_compras', modulo_compras, name='modulo_compras'),
    path('modulo_almacen', modulo_almacen, name='modulo_almacen'),
    path('modulo_reportes', modulo_reportes, name='modulo_reportes'),
    path('modulo_indicadores', modulo_indicadores, name='modulo_indicadores'),
    path('modulo_configuracion', modulo_configuracion.as_view(), name='modulo_configuracion'),
    ]