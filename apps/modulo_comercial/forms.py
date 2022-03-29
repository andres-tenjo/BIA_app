from datetime import datetime, date

from django.forms import *

from apps.modulo_configuracion.models import *
from .models import *

''' Formulario pedidos'''
class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identification'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsPedidosMdl
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
                    'data-target': '#order_date',
                    'data-toggle': 'datetimepicker',
                    'readonly': "true"
                    }
                ),
            'payment_method': Select(
                attrs={
                    'class': 'form-control',
                    'disabled': "true",
                    'id': 'payment_method'
                    }
                ),
            'deliver_date': DateInput(
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'deliver_date',
                    'data-target': '#deliver_date',
                    'data-toggle': 'datetimepicker'
                    }
                ),
            'delivery_address': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'delivery_address',
                    'readonly': "true"
                }
            ),
            'subtotal': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'subtotal',
                    'readonly': "true"
                }
            ),
            'iva': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'iva',
                    'readonly': "true"
                }
            ),
            'discount': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'discount',
                    'readonly': "true"
                }
            ),
            'total': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'total',
                    'readonly': "true"
                }
            ),
            'observations': Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'observations'
                }
            ),
        }

''' Formulario cotizaciones'''
class QuoteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identification'].widget.attrs['autofocus'] = True

    class Meta:
        model = Quotes
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

''' Formulario pago de clientes'''
class CustomerPaymentsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control' 
        self.fields['cartera'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = CustomerPayments
        fields = '__all__'
        exclude = ['user_update', 'user_creation']
        widgets = {
                'cartera': Select(
                    attrs={
                        'class': 'form-control select2',
                        'style': 'width: 100%',
                        'id': 'cartera'
                    }
                ),
                'payment': NumberInput(
                    attrs={
                        'class': 'form-control',
                        'id': 'payment'
                    }
                ),
                'obs': Textarea(
                    attrs={
                        'class': 'form-control',
                        'id': 'obs'
                    }
                ),
            }

''' Formulario agendar llamada'''
class ScheduleCallForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control' 
        self.fields['customer'].widget.attrs['autofocus'] = True
    
    class Meta:
        model = ScheduleCall
        fields = '__all__'
        exclude = ['user_update', 'user_creation']
        widgets = {
                'customer': Select(
                    attrs={
                        'class': 'form-control select2',
                        'style': 'width: 100%',
                        'id': 'customer'
                    }
                ),
                'call_date': DateInput(
                    attrs={
                        'value': datetime.now().strftime('%Y-%m-%d'),
                        'autocomplete': 'off',
                        'class': 'form-control datetimepicker-input',
                        'id': 'call_date',
                        'data-target': '#call_date',
                        'data-toggle': 'datetimepicker'
                    }
                ),
                'start_call': DateInput(
                    attrs={
                        'value': datetime.now().strftime('%Y-%m-%d'),
                        'autocomplete': 'off',
                        'class': 'form-control datetimepicker-input',
                        'id': 'start_call',
                        'data-target': '#start_call',
                        'data-toggle': 'datetimepicker'
                    }
                ),
                'end_call': DateInput(
                    attrs={
                        'value': datetime.now().strftime('%Y-%m-%d'),
                        'autocomplete': 'off',
                        'class': 'form-control datetimepicker-input',
                        'id': 'end_call',
                        'data-target': '#end_call',
                        'data-toggle': 'datetimepicker'
                    }
                ),
                'call_time': DateInput(
                    attrs={
                        'value': datetime.now().strftime('%Y-%m-%d'),
                        'autocomplete': 'off',
                        'class': 'form-control datetimepicker-input',
                        'id': 'call_time',
                        'data-target': '#call_time',
                        'data-toggle': 'datetimepicker'
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
