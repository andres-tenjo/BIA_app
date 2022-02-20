from datetime import datetime, date
from django.forms import *
from .models import *

# Planeación comercial
''' Formulario planeación comercial'''
class CommercialPlanningForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['monetary_goal'].widget.attrs['autofocus'] = True

    class Meta:
        model = CommercialPlanning
        exclude = ['date_creation', 'user_update', 'user_creation', 'date_update']
        widgets = {
            'monetary_goal': NumberInput(
                attrs={
                    'id': 'monetary_goal',
                    'class': 'form-control',
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

''' Formulario promociones'''
class PromoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Promotions
        fields = '__all__'
        exclude = ['user_update', 'user_creation']
        widgets = {
            'name': TextInput(attrs={
                'placeholder': 'Ingrese el nombre de la promoción',
                'class': 'form-control',
                'id': 'name'
            }),

            'desc': Textarea(
                attrs={
                    'placeholder': 'Ingrese la descripción de la promoción',
                    'class': 'form-control',
                    'id': 'desc'
                }
            ),
            'quantity': NumberInput(
                attrs={
                    'placeholder': 'Ingrese la cantidad disponible',
                    'class': 'form-control',
                    'id': 'quantity'
                }
            ),
            'obs': Textarea(
                attrs={
                    'placeholder': 'Ingrese las observaciones',
                    'class': 'form-control',
                    'id': 'obs'
                }
            ),
            'cons': Textarea(
                attrs={
                    'placeholder': 'Ingrese las consideraciones',
                    'class': 'form-control',
                    'id': 'cons'
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
        }
