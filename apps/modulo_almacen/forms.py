from datetime import datetime, date

from django.forms import *

from apps.modulo_configuracion.models import *
from .models import *

###############################################
# 1. ENTRADAS ALMACEN
###############################################
''' Formulario entradas de almacen '''
class clsEntradasAlmacenFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identification'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsEntradasAlmacenMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation']
        widgets = {
            'identification': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'identification'
                }
            ),
            'crossing_doc': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'crossing_doc'
                }
            ),
        }

###############################################
# 2. SALIDAS ALMACEN
###############################################
''' Formulario salidas de almacen '''
class clsSalidasAlmacenFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identification'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsSalidasAlmacenMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation']
        widgets = {
            'identification': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'id': 'identification'
                }
            ),
            'crossing_doc': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 80%',
                    'id': 'crossing_doc'
                }
            ),
            'subtotal': TextInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control'
                }
            ),
            'iva': TextInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control'
                }
            ),
            'discount': TextInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control'
                }
            ),
            'total': TextInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control'
                }
            ),
            'observations': Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
        }

###############################################
# 3. INVENTARIO
###############################################
''' Formulario inventario '''
class clsInventarioFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['inventory_type'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsSaldosInventarioMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation']
        widgets = {
            'inventory_type': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'inventory_type'
                }
            ),
            'warehouse': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'warehouse'
                }
            ),
        }