from datetime import datetime, date
from django.forms import *
from .models import *
from apps.choices import *

##########################################################
# 1. EMPRESA
##########################################################
''' Formulario empresa '''
class clsCrearEmpresaFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['person_type'].widget.attrs['autofocus'] = True
        self.fields['city'].queryset = clsCiudadesMdl.objects.all()

    class Meta:
        model = clsPerfilEmpresaMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation']
        widgets = {
            'person_type': Select(attrs={
                'class': 'form-control',
                'id': 'person_type'
                }
            ),
            'id_type': Select(attrs={
                'class': 'form-control',
                'id': 'id_type'
                }
            ),
            'id_number': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'NIT: incluya el digito de verificación sin espacios',
                    'name': 'id_number'
                }
            ),
            'company_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Convergencia soluciones SAS',
                'name': 'company_name'
                }
            ),
            'country': Select(attrs={
                'class': 'form-control select2',
                'name': 'country'
                }
            ),
            'department': Select(attrs={
                'class': 'form-control select2',
                'id': 'department'
                }
            ),
            'city': Select(attrs={
                'class': 'form-control select2',
                'id': 'city'
                }
            ),
            'postal_code': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 11001',
                    'name': 'postal_code'
                }
            ),
            'address': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Calle 158 96a 25',
                'name': 'address',
                }
            ),
            'email': EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. convergencia@bia.com.co',
                    'name': 'email',
                }
            ),
            'tel_number': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 6222254',
                    'name': 'tel_number'
                }
            ),
            'cel_number': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 3006652254',
                    'name': 'cel_number'
                }
            ),
            'main_activity_code': NumberInput(
                attrs={
                    'class': 'form-control',
                    'name': 'main_activity_code'
                }
            ),
            'second_activity_code': NumberInput(
                attrs={
                    'class': 'form-control',
                    'name': 'second_activity_code'
                }
            ),
            'contrib_type': Select(attrs={
                'class': 'form-control select2',
                'name': 'contrib_type'
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

##########################################################
# 2. CATÁLOGO PRODUCTOS
##########################################################
''' Formulario catalogo productos '''
class clsCrearProductoFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_desc'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsCatalogoProductosMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation', 'state']
        widgets = {
            'bar_code': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 770234567890',
                    'id': 'bar_code'
                }
            ),
            'product_desc': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'prod_name',
                    'placeholder': 'Ej. Aceite de oliva Don Pancho x 200 ml',
                }
            ),
            'trademark': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'prod_brand',
                    'placeholder': 'Ej. Don Pancho',
                }
            ),
            'product_cat': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 80%',
                    'id': 'prod_category',
                    'name': 'prod_category'
                }
            ),
            'product_subcat': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 80%',
                    'id': 'prod_subcategory'
                }
            ),
            'purchase_unit': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 80%',
                    'id': 'prod_udc'
                }
            ),
            'quantity_pu': NumberInput(
                attrs={
                    'class': 'form-control touchNumber',
                    'id': 'quantity_udc',
                    'placeholder': 'Ej. 12',
                    'type': 'number',
                    'step': '1',
                    'min': '1'
                }
            ),
            'cost_pu': TextInput(
                attrs={
                    'class': 'form-control touchPrice',
                    'id': 'price_udc',
                    'placeholder': 'Ej. 330000',
                    'min': '1',
                    'type': 'number',
                    'step': '0.01'
                }
            ),
            'sales_unit': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 80%',
                    'placeholder': 'Ej. Unidad',
                    'id': 'prod_udv'
                }
            ),
            'quantity_su': NumberInput(
                attrs={
                    'class': 'form-control touchNumber',
                    'placeholder': 'Ej. 1',
                    'id': 'quantity_udv',
                    'type': 'number',
                    'step': '1',
                    'min': '1'
                }
            ),
            'full_sale_price': TextInput(
                attrs={
                    'class': 'form-control touchPrice',
                    'placeholder': 'Ej. 30500',
                    'id': 'price_udv',
                    'min': '1',
                    'type': 'number',
                    'step': '0.01'
                }
            ),
            'iva': TextInput(
                attrs={
                    'class': 'form-control touchPerc',
                    'placeholder': 'Ej. 5',
                    'id': 'prod_iva',
                    'type': 'number',
                    'step': '0.01'
                }
            ),
            'other_tax': TextInput(
                attrs={
                    'class': 'form-control touchPerc',
                    'placeholder': 'Ej. 3',
                    'id': 'prod_other_tax',
                    'type': 'number',
                    'step': '0.01'
                 }
            ),
            'supplier_lead_time': TimeInput(
                attrs={
                    'class': 'form-control touchNumber',
                    'placeholder': 'Ej. 3',
                    'id': 'prod_supplier_lead_time',
                    'type': 'number',
                    'step': '1',
                    'min': '1'
                }
            )
        }
    
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                bar_code = self.cleaned_data['bar_code']          
                q_pu = self.cleaned_data['quantity_pu']
                q_su = self.cleaned_data['quantity_su']
                
                if q_pu != 0 and q_su != 0:
                    s = q_pu / q_su
                else:
                    s = 0
                p = form.save(commit=False)
                p.split = s
                p.save()
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

''' Formulario categoría productos '''
class clsCrearCategoriaProductoFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_cat'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsCategoriaProductoMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation', 'state']
        widgets = {
            'product_cat': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Alimentos',
                    'id': 'category_name',
                    'name': 'product_cat',
                    'tabindex':'-1'
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

''' Formulario subcategoría productos '''
class clsCrearSubcategoriaProductoFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product_subcat'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsSubcategoriaProductoMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation', 'state']
        widgets = {
            'product_subcat': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Aceites',
                    'id': 'subcategory_name'
                }
            ),
            'product_cat': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'id': 'product_category',
                    'name': 'product_category'
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

''' Formulario unidad de compra '''
class clsCrearUnidadCompraFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['purchase_unit'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsUnidadCompraMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation', 'state']
        widgets = {
            'purchase_unit': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Unidad, Caja, Paca',
                    'id': 'udc_name',
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

''' Formulario unidad de venta '''
class clsCrearUnidadVentaFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sales_unit'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsUnidadVentaMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation', 'state']
        widgets = {
            'sales_unit': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Unidad, Caja, Paca',
                    'id': 'udv_name',
                }
            ),
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



##########################################################
# 3. LISTA DE PRECIOS
##########################################################
''' Formulario lista de precios '''
class clsCrearListaPreciosFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['list_name'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsListaPreciosMdl
        exclude = ['user_update', 'user_creation', 'state']
        widgets = {
            'list_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Almacenes de cadena',
                    'id': 'list_name',
                }
            ),
            'store': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 100%',
                    'id': 'store',
                }
            ),
            'freight': TextInput(
                attrs={
                    'class': 'form-control touchPerc',
                    'placeholder': 'Ej. 20',
                    'id': 'freight',
                    'type': 'number',
                    'step': '0.01'
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
                instance = form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

''' Formulario detalle lista de precios '''
class clsCrearListaPreciosDetalleFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = clsDetalleListaPreciosMdl
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
                    'placeholder': 'Ej. 20',
                    'id': 'unit_price',
                    'type': 'number'
                }
            ),
            'observations': Textarea(
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
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

##########################################################
# 3. CATÁLOGO PROVEEDORES
##########################################################
''' Formulario catálogo de proveedores '''
class clsCrearProveedorFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['person_type'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsCatalogoProveedoresMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation', 'state']
        widgets = {
            'person_type': Select(
                attrs={
                'class': 'form-control select2',
                'id': 'person_type'
                }
            ),
            'id_type': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'id_type'
                }
            ),
            'identification': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 9008178892',
                    'id': 'identification'
                }
            ),
            'supplier_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Convergencia SAS',
                    'id': 'supplier_name'
                }
            ),
            'email': EmailInput(
                attrs={
                'class': 'form-control',
                'placeholder': 'Ej. usuario@empresa.com',
                'id': 'email'
                }
            ),
            'contact_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Jaime Garzón',
                    'id': 'contact_name'
                }
            ),
            'contact_cel': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 3001234567',
                    'id': 'contact_cel'
                }
            ),
            'other_contact_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Juan Rodriguez',
                    'id': 'other_contact_name'
                }
            ),
            'other_contact_cel': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 3117654321',
                    'id': 'other_contact_cel'
                }
            ),
            'department': Select(attrs={
                'class': 'form-control select2',
                'id': 'department'
                }
            ),
            'city': Select(attrs={
                'class': 'form-control select2',
                'id': 'city'
                }
            ),
            'supplier_address': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la dirección',
                    'id': 'supplier_address'
                }
            ),
            'postal_code': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 111010',
                    'id': 'postal_code'
                }
            ),
            'min_purchase_value': TextInput(
                attrs={
                    'class': 'form-control touchPrice',
                    'placeholder': 'Ej. 100000',
                    'id': 'min_purchase_value'
                }
            ),
            'logistic_condition': Select(
                attrs={
                'class': 'form-control select',
                'id': 'logistic_condition'
                }
            ),
            'pay_method': Select(
                attrs={
                'class': 'form-control select',
                'id': 'pay_method'
                }
            ),
            'credit_limit': NumberInput(
                attrs={
                    'class': 'form-control touchPrice',
                    'placeholder': 'Ej. 4500000',
                    'id': 'credit_limit'
                }
            ),
            'credit_days': NumberInput(
                attrs={
                    'class': 'form-control touchNumber',
                    'id': 'credit_days',
                    'placeholder': 'Ej. 30'
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

##########################################################
# 4. CATÁLOGO CLIENTES
##########################################################
''' Formulario catalogo clientes '''
class clsCrearClienteFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = clsCatalogoClientesMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation', 'state']
        widgets = {
            'person_type': Select(
                attrs={
                'class': 'form-control select',
                'id': 'person_type'
                }
            ),
            'id_type': Select(
                attrs={
                    'class': 'form-control select',
                    'placeholder': 'Seleccione una opción',
                    'id': 'id_type'
                }
            ),
            'identification': NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'identification',
                    'placeholder': 'Ej. 9008178892'
                }
            ),
            'business_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'business_name',
                    'placeholder': 'Convergencia soluciones SAS'
                }
            ),
            'contact_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Jaime Garzón',
                    'id': 'contact_name'
                }
            ),
            'cel_number': NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'cel_number',
                    'placeholder': '3006652254'
                }
            ),
            'email': EmailInput(
                attrs={
                    'class': 'form-control',
                    'id': 'email',
                    'placeholder': 'convergencia@convergencia.com'
                }
            ),
            'customer_cat': Select(
                attrs={
                    'class': 'form-control select2',
                    'style': 'width: 80%',
                    'id': 'customer_cat',
                }
            ),
            'department': Select(
                attrs={
                    'class': 'form-control select',
                    'style': 'width: 100%',
                    'id': 'department',
                }
            ),
            'city': Select(
                attrs={
                    'class': 'form-control select',
                    'style': 'width: 100%',
                    'id': 'city',
                }
            ),
            'customer_zone': Select(
                attrs={
                    'class': 'form-control select2',     
                    'style': 'width: 80%',               
                    'id': 'customer_zone',
                }
            ),
            'delivery_address': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'delivery_address',
                    'placeholder': 'Ingrese dirección'
                }
            ),
            'del_schedule_init': TextInput(
                attrs={
                    'autocomplete': 'off',
                    'type': 'time',
                    'class': 'form-control',
                    'id': 'del_schedule_init',
                    'placeholder': 'Seleccione un horario'
                }
            ),
            'del_schedule_end': TextInput(
                attrs={
                    'autocomplete': 'off',
                    'type': 'time',
                    'class': 'form-control',
                    'id': 'del_schedule_end',
                    'placeholder': 'Seleccione un horario'
                }
            ),
            'pay_method': Select(
                attrs={
                    'class': 'form-control select',
                    'id': 'pay_method'
                }
            ),
            'credit_days': NumberInput(
                attrs={
                    'class': 'form-control touchNumber',
                    'id': 'credit_days',
                }
            ),
            'credit_value': TextInput(
                attrs={
                    'class': 'form-control touchPrice',
                    'id': 'credit_value'
                }
            ),
            'commercial_advisor': Select(
                attrs={
                    'class': 'form-control select2',
                    'id': 'commercial_advisor',
                    'style': 'width: 80%'
                }
            ),
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

''' Formulario categoría clientes '''
class clsCrearCategoriaClienteFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = clsCategoriaClienteMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation', 'state']
        widgets = {
            'customer_cat': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'customer_cat',
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

''' Formulario zona clientes '''
class clsCrearZonaClienteFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer_zone'].widget.attrs['autofocus'] = True

    class Meta:
        model = clsZonaClienteMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation', 'state']
        widgets = {
            'customer_zone': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'customer_zone',
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

''' Formulario asesor comercial '''
class clsCrearAsesorComercialFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_superuser=False)

    class Meta:
        model = clsAsesorComercialMdl
        fields = '__all__'
        exclude = ['user_update', 'user_creation', 'state']
        widgets = {
            'advisor': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'advisor',
                    'placeholder': 'Nombre asesor comercial'
                }
            ),
            'user': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'user'
                }
            ),
            'zone': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'zone'
                }
            ),
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

##########################################################
# 5. CATÁLOGO BODEGAS
##########################################################
''' Formulario catalogo clientes '''
class clsCatalogoBodegasFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = clsCatalogoBodegasMdl
        exclude = ['user_update', 'user_creation', 'state']
        widgets = {
            'warehouse_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Bodega Norte',
                    'id': 'warehouse_name'
                }
            ),
            'department': Select(
                attrs={
                    'class': 'form-control select',
                    'style': 'width: 100%',
                    'id': 'department',
                }
            ),
            'city': Select(
                attrs={
                    'class': 'form-control select',
                    'style': 'width: 100%',
                    'id': 'city',
                }
            ),
            'warehouse_address': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'warehouse_address',
                    'placeholder': 'Ingrese dirección'
                }
            ),
            'contact_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. Jaime Garzón',
                    'id': 'contact_name'
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

##########################################################
# 6. AJUSTES INVENTARIO
##########################################################
''' Formulario ajustes inventario '''
class clsAjustesInventarioFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = clsDetalleAjusteInventarioMdl
        exclude = ['doc_number']
        widgets = {
            'store': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'store'
                }
            ),
            'type': Select(
                attrs={
                'class': 'form-control select2',
                'id': 'type'
                }
            ),
            'product_code': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'product_code'
                }
            ),
            'batch': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'batch'
                }
            ),
            'expiration_date': DateInput(
                attrs={
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'expiration_date',
                    'data-target': '#expiration_date',
                    'data-toggle': 'datetimepicker'
                    }
                ),
            'quantity': NumberInput(
                attrs={
                    'class': 'form-control touchNumber',
                    'id': 'quantity'
                }
            ),
            'total_cost': TextInput(
                attrs={
                    'class': 'form-control',
                    'readonly': 'true',
                    'id': 'total_cost'
                }
            ),
        }

##########################################################
# 7. TIEMPOS DE ENTREGA
##########################################################
''' Formulario ajustes inventario '''
class clsCrearTiempoEntregaFrm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = clsTiemposEntregaMdl
        exclude = ['user_update', 'user_creation', 'state']
        widgets = {
            'city': Select(
                attrs={
                'class': 'form-control',
                'style': 'width: 100%',
                'id': 'city'
                }
            ),
            'customer_zone': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'customer_zone'
                }
            ),
            'warehouse': Select(
                attrs={
                'class': 'form-control select2',
                'style': 'width: 100%',
                'id': 'warehouse'
                }
            ),
            'enlistment_time': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 20',
                    'id': 'enlistment_time',
                    'type': 'number',
                    'step': '0.1',
                    'value': '0'
                }
            ),
            'travel_time': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 20',
                    'id': 'travel_time',
                    'type': 'number',
                    'step': '0.1',
                    'value': '0'
                }
            ),
            'download_time': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej. 20',
                    'id': 'download_time',
                    'type': 'number',
                    'step': '0.1',
                    'value': '0'
                }
            ),
            'total_time': TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'total_time',
                    'type': 'text',
                    'readonly': 'true',
                    'step': '0.1',
                    'value': '0'
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