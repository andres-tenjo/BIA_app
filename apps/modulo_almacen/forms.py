from datetime import datetime, date

from django.forms import *

from apps.modulo_configuracion.models import *
from .models import *

''' Formulario promociones '''
class WarehouseEntryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].widget.attrs['autofocus'] = True

    class Meta:
        model = WarehouseRevenue
        fields = '__all__'
        exclude = ['user_update', 'user_creation']
        widgets = {
            'supplier': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'supplier'
                }
            ),
            'order_purchase': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'order_purchase'
                }
            ),
            'product': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'product'
                }
            ),
            'udc': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'udc'
                }
            ),
            'order_quantity': NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'order_quantity'
                }
            ),
            'real_quantity': NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'real_quantity'
                }
            ),
            'lote': TextInput(
                attrs={
                'class': 'form-control',
                'id': 'lote'
                }
            ),
            'expiration_date': DateInput(
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'expiration_date',
                    'data-target': '#expiration_date',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'documentation': CheckboxInput(
                attrs={
                    'class': 'form-control',
                    'id': 'documentation',
                }
            ),
            'obs': Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'obs'
                }
            ),
        }

''' Formulario promociones '''
class InventoryCountForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['inventory_type'].widget.attrs['autofocus'] = True

    class Meta:
        model = InventoryCount
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

''' Formulario promociones '''
class WarehouseExitForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].widget.attrs['autofocus'] = True

    class Meta:
        model = WarehouseOutFlows
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

''' Formulario promociones '''
class InventoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['autofocus'] = True

    class Meta:
        model = Inventory
        fields = '__all__'
        exclude = ['user_update', 'user_creation']
        widgets = {
            'product': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'product'
                }
            ),
            'previous_balance': NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'previous_balance'
                }
            ),
            'warehouse_entry': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'warehouse_entry'
                }
            ),
            'warehouse_exit': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'warehouse_entry'
                }
            ),
            'inventory_balance': NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'inventory_balance'
                }
            ),
            'inventory_count': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'inventory_count'
                }
            ),
            'difference': NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'difference'
                }
            ),
            'indice_rotacion': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'indice_rotacion'
                }
            ),
        }