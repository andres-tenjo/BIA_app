from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from django.contrib.auth.models import UserManager
from biapp.settings import MEDIA_URL, STATIC_URL
from django.forms import model_to_dict
from crum import get_current_request

from apps.choices import *

class User(AbstractUser):
    image = models.ImageField('Imagen de Perfil', upload_to='users/%Y/%m/%d', blank = True, null = True)
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)
    

    class Meta:
        default_permissions = []
        permissions = (('bia_adm_users', 'Usuarios'),)
        ordering = ['is_active']
    
    def get_state(self):
        if self.is_active == True:
            return 'Activo'
        else:
            return 'Inactivo'

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/logo.png')

    def toJSON(self):
        item = model_to_dict(self, exclude=['password', 'groups', 'user_permissions'])
        if self.last_login:
            item['last_login'] = self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['full_name'] = self.get_full_name()
        item['image'] = self.get_image()
        item['is_active'] = self.get_state()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def __str__(self):
        return f'{self.first_name } {self.last_name}'
    
    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass
    
Group.add_to_class('commercial', models.BooleanField(verbose_name='Módulo comercial', null=True, blank=True, default=False))
Group.add_to_class('purchase', models.BooleanField(verbose_name='Módulo compras', null=True, blank=True, default=False))
Group.add_to_class('logistics', models.BooleanField(verbose_name='Módulo logística', null=True, blank=True, default=False))
Group.add_to_class('admin', models.BooleanField(verbose_name='Módulo administración', null=True, blank=True, default=False))
Group.add_to_class('all', models.BooleanField(verbose_name='Todos los módulos', null=True, blank=True, default=False))
Group.add_to_class('com_permission', models.ManyToManyField(Permission, verbose_name='Permisos comercial', related_name='com_permission', blank=True,))
Group.add_to_class('pur_permission', models.ManyToManyField(Permission, verbose_name='Permisos compras', related_name='pur_permission', blank=True,))
Group.add_to_class('log_permission', models.ManyToManyField(Permission, verbose_name='Permisos logística', related_name='log_permission', blank=True,))
Group.add_to_class('adm_permission', models.ManyToManyField(Permission, verbose_name='Permisos administración', related_name='adm_permission', blank=True,))
