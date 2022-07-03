# Django libraries
from django.urls import path

# Apps functions
from .views import *
from apps.usuario.views import *
from apps.Modelos.Commercial_KPI import fncIndicadoresCierreMes, fncIndicadoresAlternos

urlpatterns = [
    ###############################################################
    # Planeación comercial
    ###############################################################
    path(
        'planeacion_comercial/', 
        clsMenuPlaneacionComercialViw.as_view(), 
        name='planeacion_comercial'
        ),
    # Planeación comercial - establecer indicadores
    path(
        'planeacion_comercial_indicadores/',
        clsPlaneacionComercialEstablecerIndicadoresViw.as_view(), 
        name='planeacion_comercial_indicadores'
        ),
    # Planeación comercial - historico
    path(
        'planeacion_comercial_historico/',
        clsPlaneacionComercialHistoricoViw.as_view(), 
        name='planeacion_comercial_historico'
        ),
    ###############################################################
    # Planeación compras
    ###############################################################
    path(
        'planeacion_compras/', 
        clsMenuPlaneacionComprasViw.as_view(), 
        name='planeacion_compras'
        ),
    # Planeación compras - establecer indicadores
    path(
        'planeacion_compras_indicadores/',
        clsPlaneacionComprasEstablecerIndicadoresViw.as_view(), 
        name='planeacion_compras_indicadores'
        ),
    # Planeación compras - historico
    path(
        'planeacion_compras_historico/',
        clsPlaneacionComprasHistoricoViw.as_view(), 
        name='planeacion_compras_historico'
        ),
    ###############################################################
    # Planeación almacén
    ###############################################################
    path(
        'planeacion_almacen/', 
        clsMenuPlaneacionAlmacenViw.as_view(), 
        name='planeacion_almacen'
        ),
    # Planeación almacen - establecer indicadores
    path(
        'planeacion_almacen_indicadores/',
        clsPlaneacionAlmacenEstablecerIndicadoresViw.as_view(), 
        name='planeacion_almacen_indicadores'
        ),
    # Planeación almacen - historico
    path(
        'planeacion_almacen_historico/',
        clsPlaneacionAlmacenHistoricoViw.as_view(), 
        name='planeacion_almacen_historico'
        ),
    ]

fncIndicadoresAlternos()
fncIndicadoresCierreMes()
