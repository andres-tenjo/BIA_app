from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from apps.home.views import Home
from apps.usuario.views import clsLoginViw, clsLogoutViw

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/',  admin.site.urls),
    # Home
    path('', login_required(Home.as_view()), name='home'),
    # Login Logout
    path('accounts/login/', clsLoginViw.as_view(), name='login'),
    path('logout/', clsLogoutViw.as_view(), name='logout'),
    # Apps
    path('', include('apps.home.urls')),
    path('usuarios/',include(('apps.usuario.urls','usuarios'))),
    path('comercial/',include(('apps.modulo_comercial.urls','comercial'))),
    path('compras/',include(('apps.modulo_compras.urls','compras'))),
    path('logistica/',include(('apps.modulo_logistica.urls','logistica'))),
    path('indicadores/',include(('apps.modulo_indicadores.urls','indicadores'))),
    path('reportes/',include(('apps.modulo_reportes.urls','reportes'))),
    path('configuracion/',include(('apps.modulo_configuracion.urls','configuracion'))),
    path('planeacion/',include(('apps.planeacion.urls','planeacion')))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)