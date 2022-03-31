from datetime import datetime, date

from django.forms import *

from apps.modulo_configuracion.models import *
from .models import *

# ''' Formulario ordenes de compra '''
# class OrderPurchaseForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['identification'].widget.attrs['autofocus'] = True

#     class Meta:
#         model = OrderPurchase
#         fields = '__all__'
#         exclude = ['user_update', 'user_creation']
#         widgets = {
#             'identification': Select(
#                 attrs={
#                     'class': 'form-control select2',
#                     'style': 'width: 80%',
#                     'id': 'identification'
#                 }
#             ),
#             'order_date': DateInput(
#                 attrs={
#                     'value': datetime.now().strftime('%Y-%m-%d'),
#                     'autocomplete': 'off',
#                     'class': 'form-control datetimepicker-input',
#                     'id': 'order_date',
#                     'readonly': True,
#                     'data-target': '#order_date',
#                     'data-toggle': 'datetimepicker'
#                 }
#             ),
#             'pay_method': Select(attrs={
#                 'class': 'form-control',
#                 'id': 'pay_method',
#                 'disabled': "true",
#             }),
#             'delivery_date': DateInput(
#                 attrs={
#                     'value': datetime.now().strftime('%Y-%m-%d'),
#                     'autocomplete': 'off',
#                     'class': 'form-control datetimepicker-input',
#                     'id': 'delivery_date',
#                     'data-target': '#delivery_date',
#                     'data-toggle': 'datetimepicker'
#                 }
#             ),
#             'delivery_address': TextInput(
#                 attrs={
#                     'class': 'form-control',
#                     'id': 'delivery_address'
#                 }
#             ),
#             'observations': Textarea(
#                 attrs={
#                     'class': 'form-control',
#                     'id': 'observations'
#                 }
#             ),
#             'urgency_level': Select(
#                 attrs={
#                     'class': 'form-control',
#                     'id': 'urgency_level'
#                 }
#             ),
#             'subtotal': TextInput(
#                 attrs={
#                     'readonly': True,
#                     'class': 'form-control',
#                 }
#             ),
#             'iva': TextInput(
#                 attrs={
#                     'readonly': True,
#                     'class': 'form-control'
#                 }
#             ),
#             'discount': TextInput(
#                 attrs={
#                     'readonly': True,
#                     'class': 'form-control'
#                 }
#             ),
#             'total': TextInput(
#                 attrs={
#                     'readonly': True,
#                     'class': 'form-control',
#                 }
#             ),
#         }

# ''' Formulario cotizaciones proveedores'''
# class SupplierQuoteForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['identification'].widget.attrs['autofocus'] = True

#     class Meta:
#         model = SupplierQuote
#         fields = '__all__'
#         exclude = ['user_update', 'user_creation']
#         widgets = {
#             'identification': Select(attrs={
#                 'class': 'form-control select2',
#                 'style': 'width: 80%',
#                 'id': 'identification'
#                 }
#             ),
#             'quote_date': DateInput(
#                 attrs={
#                     'value': datetime.now().strftime('%Y-%m-%d'),
#                     'autocomplete': 'off',
#                     'class': 'form-control datetimepicker-input',
#                     'id': 'quote_date',
#                     'data-target': '#quote_date',
#                     'data-toggle': 'datetimepicker'
#                 }
#             ),
#             'lead_time': NumberInput(
#                 attrs={
#                     'class': 'form-control',
#                     'id': 'lead_time',
#                 }
#             ),
#             'subtotal': TextInput(
#                 attrs={
#                     'readonly': True,
#                     'class': 'form-control'
#                 }
#             ),
#             'iva': TextInput(
#                 attrs={
#                     'readonly': True,
#                     'class': 'form-control'
#                 }
#             ),
#             'discount': TextInput(
#                 attrs={
#                     'readonly': True,
#                     'class': 'form-control'
#                 }
#             ),
#             'total': TextInput(
#                 attrs={
#                     'readonly': True,
#                     'class': 'form-control'
#                 }
#             ),
#             'observations': Textarea(
#                 attrs={
#                     'class': 'form-control'
#                 }
#             ),
#         }

# ''' Formulario evaluación de proveedores '''
# class EvaluationSuppliersForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['supplier'].widget.attrs['autofocus'] = True
    
#     class Meta:
#         model = EvaluationSuppliers
#         fields = '__all__'
#         exclude = ['user_update', 'user_creation']
#         widgets = {
#                 'supplier': Select(
#                     attrs={
#                         'class': 'form-control select2',
#                         'style': 'width: 100%',
#                         'id': 'supplier'
#                     }
#                 ),
#                 'evaluation_type': Select(
#                     attrs={
#                         'class': 'form-control select2',
#                         'style': 'width: 100%',
#                         'id': 'evaluation_type'
#                     }
#                 ),
#                 'buyer': TextInput(
#                     attrs={
#                         'class': 'form-control',
#                         'id': 'buyer'
#                     }
#                 ),
#                 'general_score': TextInput(
#                     attrs={
#                         'class': 'form-control',
#                         'id': 'general_score'
#                     }
#                 ),
#                 'deliver_score': TextInput(
#                     attrs={
#                         'class': 'form-control',
#                         'id': 'deliver_score'
#                     }
#                 ),
#                 'quantity_score': TextInput(
#                     attrs={
#                         'class': 'form-control',
#                         'id': 'quantity_score'
#                     }
#                 ),
#                 'quality_score': TextInput(
#                     attrs={
#                         'class': 'form-control',
#                         'id': 'quality_score'
#                     }
#                 ),
#                 'products_score': TextInput(
#                     attrs={
#                         'class': 'form-control',
#                         'id': 'products_score'
#                     }
#                 ),
#                 'price_score': TextInput(
#                     attrs={
#                         'class': 'form-control',
#                         'id': 'price_score'
#                     }
#                 ),
#                 'pay_score': TextInput(
#                     attrs={
#                         'class': 'form-control',
#                         'id': 'pay_score'
#                     }
#                 ),
#                 'demand_score': TextInput(
#                     attrs={
#                         'class': 'form-control',
#                         'id': 'demand_score'
#                     }
#                 ),
#                 'doc_score': TextInput(
#                     attrs={
#                         'class': 'form-control',
#                         'id': 'doc_score'
#                     }
#                 ),
#                 'obs': Textarea(
#                     attrs={
#                         'class': 'form-control',
#                         'id': 'obs'
#                     }
#                 ),
#                 'state': Select(
#                       attrs={
#                         'class': 'form-control',
#                         'style': 'width: 100%',
#                         'id': 'state'
#                     }
#                 ),
#             }

# ''' Formulario pago de clientes '''
# class SuppliersPaymentsForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['cartera'].widget.attrs['autofocus'] = True
    
#     class Meta:
#         model = SuppliersPayments
#         fields = '__all__'
#         exclude = ['user_update', 'user_creation']
#         widgets = {
#                 'cartera': Select(
#                     attrs={
#                         'class': 'form-control select2',
#                         'style': 'width: 100%',
#                         'id': 'cartera'
#                     }
#                 ),
#                 'payment': TextInput(
#                     attrs={
#                         'class': 'form-control',
#                         'id': 'payment'
#                     }
#                 ),
#                 'obs': Textarea(
#                     attrs={
#                         'class': 'form-control',
#                         'id': 'obs'
#                     }
#                 ),
#             }
    
#     def save(self, commit=True):
#         data = {}
#         form = super()
#         try:
#             if form.is_valid():
#                 instance = form.save()
#             else:
#                 data['error'] = form.errors
#         except Exception as e:
#             data['error'] = str(e)
#         return data
