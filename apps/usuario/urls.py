from django.urls import path
from apps.usuario.views import *

urlpatterns = [
    # Url crear grupos
    path(
        'crear_grupos_usuarios', 
        clsCrearGrupoViw.as_view(), 
        name='crear_grupos_usuarios'
        ),
    # Url editar grupos
    path(
        'editar_grupos/<int:pk>/',
        clsEditarGrupoViw.as_view(), 
        name = 'editar_grupos'
        ),
    # Url listar grupos
    path(
        'listar_grupos', 
        clsListarGrupoViw.as_view(), 
        name='listar_grupos'
        ),
    # Url crear usuarios
    path(
        'crear_usuarios', 
        clsCrearUsuarioViw.as_view(), 
        name='crear_usuarios'
        ),
    # Url editar usuarios
    path(
        'editar_usuarios/<int:pk>/',
        clsEditarUsuarioViw.as_view(), 
        name = 'editar_usuarios'
        ),
    # Url listar usuarios
    path(
        'listar_usuarios', 
        clsListarUsuarioViw.as_view(), 
        name='listar_usuarios'
        )
]