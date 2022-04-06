from datetime import datetime, date

from django.forms import *

from apps.modulo_configuracion.models import *
from .models import *

###############################################
# 1. PEDIDOS
###############################################
''' Formulario pedidos'''
class clsPedidosFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identification'].widget.attrs['autofocus'] = True

#     class Meta:
#         model = clsPedidosMdl
#         fields = '__all__'
#         exclude = ['user_update', 'user_creation']
#         widgets = {
#             'identification': Select(
#                 attrs={
#                     'class': 'form-control select2',
#                     'style': 'width: 80%',
#                     'id': 'identification'
#                     }
#                 ),
#             'order_date': DateInput(
#                 attrs={
#                     'value': datetime.now().strftime('%Y-%m-%d'),
#                     'autocomplete': 'off',
#                     'class': 'form-control datetimepicker-input',
#                     'id': 'order_date',
#                     'data-target': '#order_date',
#                     'data-toggle': 'datetimepicker',
#                     'readonly': "true"
#                     }
#                 ),
#             'payment_method': Select(
#                 attrs={
#                     'class': 'form-control',
#                     'disabled': "true",
#                     'id': 'payment_method'
#                     }
#                 ),
#             'deliver_date': DateInput(
#                 attrs={
#                     'value': datetime.now().strftime('%Y-%m-%d'),
#                     'autocomplete': 'off',
#                     'class': 'form-control datetimepicker-input',
#                     'id': 'deliver_date',
#                     'data-target': '#deliver_date',
#                     'data-toggle': 'datetimepicker'
#                     }
#                 ),
#             'delivery_address': TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'id': 'delivery_address',
#                     'readonly': "true"
#                 }
#             ),
#             'subtotal': TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'id': 'subtotal',
#                     'readonly': "true"
#                 }
#             ),
#             'iva': TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'id': 'iva',
#                     'readonly': "true"
#                 }
#             ),
#             'discount': TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'id': 'discount',
#                     'readonly': "true"
#                 }
#             ),
#             'total': TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'id': 'total',
#                     'readonly': "true"
#                 }
#             ),
#             'observations': Textarea(
#                 attrs={
#                     'class': 'form-control',
#                     'id': 'observations'
#                 }
#             ),
#         }

###############################################
# 2. COTIZACIONES
###############################################
''' Formulario cotizaciones'''
class clsCotizacionComercialFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identification'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsCotizacionesMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation']
        widgets = {
            'identification': Select(attrs={
                'class': 'form-control select2',
                'style': 'width: 80%',
                'id': 'identification'
                }
            ),
            'quote_date': DateInput(
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'readonly': True,
                    'class': 'form-control datetimepicker-input',
                    'id': 'quote_date',
                    'data-target': '#quote_date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'subtotal': TextInput(
                attrs={
                    'readonly': True,
                    'id': 'subtotal',
                    'class': 'form-control',
                }
            ),
            'iva': TextInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True,
                    'id': 'iva'
                }
            ),
            'discount': TextInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control',
                    'id': 'discount'
                }
            ),
            'total': TextInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control',
                    'id': 'total'
                }
            ),
            'observations': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'observations'
                }
            ),
        }

###############################################
# 3. AGENDA DE LLAMADAS
###############################################
''' Formulario agendar llamada'''

###############################################
# 3. PQR CLIENTES
###############################################
''' Formulario PQR clientes'''
