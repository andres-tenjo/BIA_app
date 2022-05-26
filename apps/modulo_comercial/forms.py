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

    class Meta:
        model = clsPedidosMdl
        exclude = ['user_update', 'user_creation', 'update_date', 'condition', 'creation_date']
        widgets = {
            'identification': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 80%',
                    'id': 'identification'
                    }
                ),
            'delivery_date': DateInput(
                attrs={
                    'autocomplete': 'off',
                    'type': 'date',
                    'class': 'form-control',
                    'id': 'deliver_date',
                    }
                ),
            'city': Select(
                attrs={
                    'class': 'form-control selectCity',
                    'style': 'width: 100%',
                    'id': 'city'
                    }
                ),
            'customer_zone': Select(
                attrs={
                    'class': 'form-control selectCity',
                    'style': 'width: 100%',
                    'id': 'customer_zone'
                    }
                ),
            'delivery_address': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'delivery_address',
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
                    'id': 'observations',
                    'rows':'1'
                }
            ),
            'store': Select(
                attrs={
                    'class': 'form-control select',
                    'style': 'width: 100%',
                    'id': 'store',
                }
            ),
        }
    
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

''' Formulario detalle de pedido '''
class clsCrearPedidoDetalleFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = clsDetallePedidosMdl
        exclude = ['doc_number']
        widgets = {
            'product_code': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'id': 'product_code',
                }
            ),
            'quantity': NumberInput(
                attrs={
                    'class': 'form-control touchNumber',
                    'placeholder': 'Ej. 20',
                    'id': 'quantity',
                    'type': 'number'
                }
            ),
            'unit_price': NumberInput(
                attrs={
                    'class': 'form-control touchPrice',
                    'id': 'unit_price',
                    'type': 'number',
                    'readonly': "true"
                }
            ),
            'subtotal': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'subtotal_producto',
                    'readonly': "true"
                }
            ),
            'iva': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'iva_producto',
                    'readonly': "true"
                }
            ),
            'total': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'total_producto',
                    'readonly': "true"
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

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
        exclude = ['user_update', 'user_creation', 'update_date', 'condition', 'creation_date']
        widgets = {
            'identification': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 80%',
                    'id': 'identification'
                    }
                ),
            'city': Select(
                attrs={
                    'class': 'form-control select',
                    'style': 'width: 100%',
                    'id': 'city'
                    }
                ),
            'store': Select(
                attrs={
                    'class': 'form-control select',
                    'style': 'width: 100%',
                    'id': 'store',
                    }
                ),
            'freight': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'freight',
                }
            ),
            'general_obs': Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'general_obs',
                    'rows':'1'
                }
            ),
            'follow_up_date': DateInput(
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'type': 'date',
                    'class': 'form-control',
                    'id': 'follow_up_date',
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
            'total': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'total',
                    'readonly': "true"
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

''' Formulario detalle de cotización '''
class clsCotizacionComercialDetalleFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = clsDetalleCotizacionesMdl
        exclude = ['doc_number']
        widgets = {
            'product_code': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'id': 'product_code',
                }
            ),
            'quantity': NumberInput(
                attrs={
                    'class': 'form-control touchNumber',
                    'placeholder': 'Ej. 20',
                    'id': 'quantity',
                    'type': 'number'
                }
            ),
            'lead_time': NumberInput(
                attrs={
                    'class': 'form-control touchNumber',
                    'placeholder': 'Ej. 20',
                    'id': 'lead_time',
                    'type': 'number'
                }
            ),
            'unit_price': NumberInput(
                attrs={
                    'class': 'form-control touchPrice',
                    'id': 'unit_price',
                    'type': 'number'
                }
            ),
            'due_date': DateInput(
                attrs={
                    'autocomplete': 'off',
                    'type': 'date',
                    'class': 'form-control',
                    'id': 'due_date'
                },
                format='%Y-%m-%d'
            ),
            'observations': Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'observations',
                    'rows':'1'
                }
            ),   
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

###############################################
# 3. AGENDA DE LLAMADAS
###############################################
''' Formulario agendar llamada'''
class clsAgendarLlamadaFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['identification'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsActividadesComercialMdl
        exclude = ['user_update', 'user_creation', 'update_date', 'task', 'condition']
        widgets = {
            'identification': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 80%',
                    'id': 'identification'
                }
            ),
            'task_date': DateInput(
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'type': 'date',
                    'class': 'form-control',
                    'id': 'task_date',
                },
                format='%Y-%m-%d'
            ),
            'start_hour': TextInput(
                attrs={
                    'autocomplete': 'off',
                    'type': 'time',
                    'class': 'form-control',
                    'id': 'start_hour',
                    'placeholder': 'Seleccione un horario'
                }
            ),
            'end_hour': TextInput(
                attrs={
                    'autocomplete': 'off',
                    'type': 'time',
                    'class': 'form-control',
                    'id': 'end_hour',
                    'placeholder': 'Seleccione un horario'
                }
            ),
            'customer_state': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'id': 'customer_state'
                }
            ),
            'objetive': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'id': 'objetive'
                }
            ),
            'observation': Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'observation',
                    'rows':'1'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

###############################################
# 3. PQR CLIENTES
###############################################
''' Formulario PQR clientes'''
