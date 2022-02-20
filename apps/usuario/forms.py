from datetime import datetime

from django.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, Permission

from .models import *

class UserForm(ModelForm):
    password2 = CharField(label = 'Contraseña de Confirmación', required=False, widget = PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente su contraseña...',
            'id': 'password2',
            }
    ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True
        self.fields['user_permissions'].queryset = Permission.objects.filter(codename__icontains="bia")

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined', 'is_superuser', 'is_active', 'is_staff']
        widgets = {
            'first_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Gonzalo Andrés',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Tenjo Lancheros',
                }
            ),
            'username': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. andres.tenjo',
                }
            ),
            'email': EmailInput(
                attrs={
                    'class': 'form-control',
                    'name': 'email',
                    'placeholder': 'Ej. andres@empresa.com',
                }
            ),
            'password': PasswordInput(render_value=True,
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su contraseña',
                    'id': 'password'
                }
            ),
            'groups': SelectMultiple(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'multiple': 'multiple'
                }
            ),
            'user_permissions': SelectMultiple(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'id': 'user_permissions',
                    'multiple': 'multiple'
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                pwd2 = self.cleaned_data.get('password2')
                u = form.save(commit=False)
                if u.pk is None:
                    if len(pwd) < 6:
                        raise forms.ValidationError('La contraseña debe tener como mínimo 6 caracteres')
                    if pwd != pwd2:
                        raise forms.ValidationError('Contraseñas no coinciden!')
                    else:
                        u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        if pwd != pwd2:
                            raise forms.ValidationError('Contraseñas no coinciden!')
                        else:
                            u.set_password(pwd)    
                    else:
                        pass
                u.save()
                u.groups.clear()
                for group in self.cleaned_data['groups']:
                    u.groups.add(group)
                for perm in self.cleaned_data['user_permissions']:
                    u.user_permissions.add(perm)
            else: 
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class UserGroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['permissions']
        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Comerciales',
                    'autocomplete': 'off'
                }
            ),
            'com_permission': SelectMultiple(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'id': 'com_permission',
                    'multiple': 'multiple'
                }
            ),
            'pur_permission': SelectMultiple(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'id': 'pur_permission',
                    'multiple': 'multiple'
                }
            ),
            'log_permission': SelectMultiple(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'id': 'log_permission',
                    'multiple': 'multiple'
                }
            ),
            'adm_permission': SelectMultiple(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'id': 'adm_permission',
                    'multiple': 'multiple'
                }
            ),
            'commercial': CheckboxInput(
                attrs={
                    'id': 'commercial',
                    'value':'0'
                }
            ),
            'purchase': CheckboxInput(
                attrs={
                    'id': 'purchase',
                    'value':'0'
                }
            ),
            'logistics': CheckboxInput(
                attrs={
                    'id': 'logistics',
                    'value':'0'
                }
            ),
            'admin': CheckboxInput(
                attrs={
                    'id': 'admin',
                    'value':'0'
                }
            ),
            'all': CheckboxInput(
                attrs={
                    'id': 'all',
                    'value':'0'
                }
            )
        }
    
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
