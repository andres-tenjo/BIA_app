from datetime import datetime, date

from django.forms import *

from apps.modulo_configuracion.models import *
from .models import *

##########################################################
# 1. ORDEN DE COMPRA
##########################################################
''' Formulario ordenes de compra '''
class clsOrdenCompraFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identification'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsOrdenesCompraMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation']
        widgets = {
            'identification': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 80%',
                    'id': 'identification'
                }
            ),
            'order_date': DateInput(
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'order_date',
                    'readonly': True,
                    'data-target': '#order_date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'pay_method': Select(attrs={
                'class': 'form-control',
                'id': 'pay_method',
                'disabled': "true",
            }),
            'delivery_date': DateInput(
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'delivery_date',
                    'data-target': '#delivery_date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'delivery_address': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'delivery_address'
                }
            ),
            'observations': Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'observations'
                }
            ),
            'urgency_level': Select(
                attrs={
                    'class': 'form-control',
                    'id': 'urgency_level'
                }
            ),
            'subtotal': TextInput(
                attrs={
                    'readonly': True,
                    'class': 'form-control',
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
                    'class': 'form-control',
                }
            ),
        }

##########################################################
# 2. NEGOCIACIÓN PROVEEDOR
##########################################################

##########################################################
# 3. EVALUACIÓN PROVEEDOR
##########################################################
''' Formulario evaluación de proveedores '''
class clsEvaluacionProveedorFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_purchase'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = clsEvaluacionProveedorMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation']
        widgets = {
                'order_purchase': Select(
                    attrs={
                        'class': 'form-control select2',
                        'style': 'width: 100%',
                        'id': 'order_purchase'
                    }
                ),
                'evaluation_type': Select(
                    attrs={
                        'class': 'form-control select2',
                        'style': 'width: 100%',
                        'id': 'evaluation_type'
                    }
                ),
                'buyer': TextInput(
                    attrs={
                        'class': 'form-control',
                        'id': 'buyer'
                    }
                ),
                'general_score': TextInput(
                    attrs={
                        'class': 'form-control',
                        'id': 'general_score'
                    }
                ),
                'deliver_score': TextInput(
                    attrs={
                        'class': 'form-control',
                        'id': 'deliver_score'
                    }
                ),
                'quantity_score': TextInput(
                    attrs={
                        'class': 'form-control',
                        'id': 'quantity_score'
                    }
                ),
                'quality_score': TextInput(
                    attrs={
                        'class': 'form-control',
                        'id': 'quality_score'
                    }
                ),
                'products_score': TextInput(
                    attrs={
                        'class': 'form-control',
                        'id': 'products_score'
                    }
                ),
                'price_score': TextInput(
                    attrs={
                        'class': 'form-control',
                        'id': 'price_score'
                    }
                ),
                'pay_score': TextInput(
                    attrs={
                        'class': 'form-control',
                        'id': 'pay_score'
                    }
                ),
                'demand_score': TextInput(
                    attrs={
                        'class': 'form-control',
                        'id': 'demand_score'
                    }
                ),
                'doc_score': TextInput(
                    attrs={
                        'class': 'form-control',
                        'id': 'doc_score'
                    }
                ),
                'obs': Textarea(
                    attrs={
                        'class': 'form-control',
                        'id': 'obs'
                    }
                ),
                'state': Select(
                      attrs={
                        'class': 'form-control',
                        'style': 'width: 100%',
                        'id': 'state'
                    }
                ),
            }
