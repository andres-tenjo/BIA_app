# Pyhton libraries
from datetime import datetime, date
from crum import get_current_user
from django.conf import settings
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw

# Django libraries
from django_pandas.managers import DataFrameManager
from django.db import models
from django.db.models import Model, Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import model_to_dict
from django.contrib.auth.models import Permission
from django.core.files import File
from django.db.models.signals import post_save

# BIA files
from apps.choices import *
from apps.models import BaseModel
from apps.usuario.models import *

#################################################################################################
# 1. CIUDADES Y DEPARTAMENTOS
#################################################################################################
''' 1.1 Tabla departamentos'''
class clsDepartamentosMdl(BaseModel):
    department_name = models.CharField('Departamento', max_length=200, unique=True)
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Departamento'
        verbose_name_plural= 'Departamentos'
        ordering = ['id']
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

    def __str__ (self):
        return self.department_name

''' 1.2 Tabla ciudades'''
class clsCiudadesMdl(BaseModel):
    city_name = models.CharField('Ciudad', max_length=200)
    department = models.ForeignKey(clsDepartamentosMdl, on_delete=models.CASCADE)
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Ciudad'
        verbose_name_plural= 'Ciudades'
        ordering = ['id']
    
    def fncConsultaCiudades(self):
        item = model_to_dict(self, exclude=['department', 'user_creation', 'user_update', 'city_name'])
        item['text'] = self.city_name
        return item

    def toJSON(self):
        item = model_to_dict(self)
        item['department'] = self.department.toJSON()
        return item

    def fncDataCiudadesSlcjsn(self):
        item = model_to_dict(self, fields=['id', 'city_name'])
        return item

    def __str__ (self):
        return self.city_name

#################################################################################################
# 2. PERFIL EMPRESARIAL
#################################################################################################
''' 2.1 Tabla perfil empresa'''
class clsPerfilEmpresaMdl(BaseModel):
    person_type = models.CharField('Tipo de persona', max_length=200, choices=PERSON_TYPE)
    id_type = models.CharField('Tipo de identificación', max_length=200, choices=ID_TYPE)
    id_number = models.PositiveBigIntegerField('Identificación', unique=True)
    company_name = models.CharField('Nombre o razón social', max_length=200, unique=True)
    country = models.CharField('País', max_length=200, choices=COUNTRY, default='CO')
    department = models.ForeignKey(clsDepartamentosMdl, on_delete=models.CASCADE)
    city = models.ForeignKey(clsCiudadesMdl, on_delete=models.CASCADE)
    postal_code = models.PositiveBigIntegerField('Código postal', blank=True, null=True)
    address = models.CharField('Dirección principal', max_length=200)
    email = models.EmailField('Correo electrónico', max_length=200, blank=True, null=True)
    tel_number = models.PositiveBigIntegerField('Teléfono', blank=True, null=True)
    cel_number = models.PositiveBigIntegerField('Celular')
    main_activity_code = models.PositiveBigIntegerField('Actividad principal')
    second_activity_code = models.PositiveBigIntegerField('Actividad secundaría', blank=True, null=True)
    contrib_type = models.CharField('Tipo de contribuyente', max_length=200, choices=CONTRIB_TYPE)
    logo = models.ImageField('Logo empresa', upload_to='logo/%Y/%m/%d', blank = True, null = True)
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Información empresa'
        verbose_name_plural= 'Información empresas'
        ordering = ['id']
        default_permissions = []

    def get_logo(self):
        if self.logo:
            return '{}{}'.format(MEDIA_URL, self.logo)
        return '{}{}'.format(STATIC_URL, 'img/home/logo.png')

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsPerfilEmpresaMdl, self).save()
            
    def fncRetornarConsultaDocumentosjsn(self):
        item = model_to_dict(self, fields=['company_name', 'logo', 'id_type', 'id_number', 'address', 'cel_number', 'email'])
        item['id_type'] = {'id': self.id_type, 'name': self.get_id_type_display()}
        item['logo'] = self.get_logo()
        return item
    
    def toJSON(self):
        item = model_to_dict(self)
        item['person_type'] = {'id': self.person_type, 'name': self.get_person_type_display()}
        item['id_type'] = {'id': self.id_type, 'name': self.get_id_type_display()}
        item['contrib_type'] = {'id': self.contrib_type, 'name': self.get_contrib_type_display()}
        item['country'] = {'id': self.country, 'name': self.get_country_display()}
        item['department'] = self.department.toJSON()
        item['city'] = self.city.toJSON()
        item['logo'] = self.get_logo()
        return item

    def jsnObtenerIdentificacion(self):
        jsn = model_to_dict(self, fields=['id_number'])
        return jsn

    def __str__ (self):
        return str(self.id_number)

#################################################################################################
# 3. CATÁLOGO DE PRODUCTOS
#################################################################################################
''' 3.1 Tabla categoría de producto'''
class clsCategoriaProductoMdl(BaseModel):
    product_cat = models.CharField('Nombre categoría', max_length=50, unique=True)
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Categoria producto'
        verbose_name_plural= 'Categorias productos'
        ordering = ['state']
        default_permissions = []

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsCategoriaProductoMdl, self).save()
            
    def toJSON(self):
        item = model_to_dict(self, exclude=['user_creation', 'user_update'])
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__ (self):
        return self.product_cat

''' 3.2 Tabla subcategoría de producto'''
class clsSubcategoriaProductoMdl(BaseModel):
    product_subcat = models.CharField('Nombre subcategoría', max_length=50, unique=True)
    product_cat = models.ForeignKey(clsCategoriaProductoMdl, on_delete=models.CASCADE, verbose_name='Categoría de producto')
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Subcategoría producto'
        verbose_name_plural= 'Subcategorías productos'
        ordering = ['state']
        default_permissions = []
    
    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsSubcategoriaProductoMdl, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['product_cat'] = self.product_cat.toJSON()
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__ (self):
        return self.product_subcat

''' 3.3 Tabla unidad de compra de producto'''
class clsUnidadCompraMdl(BaseModel):
    purchase_unit = models.CharField('Unidad de compra', max_length=150, unique=True)
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Unidad de compra'
        verbose_name_plural= 'Unidades de compra'
        ordering = ['state']
        default_permissions = []
    
    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsUnidadCompraMdl, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__ (self):
        return self.purchase_unit

''' 3.4 Tabla unidad de venta de un producto'''
class clsUnidadVentaMdl(BaseModel):
    sales_unit = models.CharField('Unidad de venta',max_length=150, unique=True)
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Unidad de venta'
        verbose_name_plural= 'Unidades de venta'
        ordering = ['state']
        default_permissions = []
    
    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsUnidadVentaMdl, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def fncConsultaUnidadVenta(self):
        item = model_to_dict(self, fields=['id', 'sales_unit'])
        return item

    def __str__ (self):
        return self.sales_unit

''' 3.5 Tabla catálogo de productos'''
class clsCatalogoProductosMdl(BaseModel):
    qr_code = models.ImageField(upload_to = '', blank=True)
    product_desc = models.CharField('Nombre del producto', max_length=200)
    bar_code = models.PositiveBigIntegerField('Código de barras', unique=True, blank=True, null=True)
    trademark = models.CharField('Marca del producto', max_length=200)
    product_cat = models.ForeignKey(clsCategoriaProductoMdl, on_delete=models.CASCADE, verbose_name='Categoría')
    product_subcat = models.ForeignKey(clsSubcategoriaProductoMdl, on_delete=models.CASCADE, verbose_name='Subcategoría', blank=True, null=True)
    purchase_unit = models.ForeignKey(clsUnidadCompraMdl, on_delete=models.CASCADE, verbose_name='Unidad de compra')
    quantity_pu = models.PositiveSmallIntegerField('cantidad por unidad de compra')
    cost_pu = models.DecimalField('Costo de compra', max_digits=10, decimal_places=2)
    sales_unit = models.ForeignKey(clsUnidadVentaMdl, on_delete=models.CASCADE, verbose_name='Unidad de venta')
    quantity_su = models.PositiveSmallIntegerField('cantidad por unidad de venta')
    full_sale_price = models.DecimalField('Precio de venta', max_digits=10, decimal_places=2)
    split = models.PositiveSmallIntegerField('Equivalencia', blank=True, null=True)
    iva = models.DecimalField('Iva', max_digits=5, decimal_places=2, blank=True, null=True)
    other_tax = models.DecimalField('Otros impuestos', max_digits=5, decimal_places=2, blank=True, null=True)
    supplier_lead_time = models.PositiveSmallIntegerField('Tiempo de entrega proveedor')
    state = models.CharField('Estado', max_length=10, choices=STATE, default='AC')
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Catálogo producto'
        verbose_name_plural= 'Catálogo productos'
        ordering = ['state']
        default_permissions = []
        permissions = (('bia_adm_product_catalogue', 'Cátalogo productos'),)
    
    def get_qr_code(self):
        if self.qr_code:
            return '{}{}'.format(MEDIA_URL, self.qr_code)
        return '{}{}'.format(STATIC_URL, 'img/logo.png')

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None, *args, **kwargs):
        user = get_current_user()
        if user is not None:
            if not self.id:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsCatalogoProductosMdl, self).save(*args, **kwargs)

    def toJSON(self, lst_fields=None):
        item = model_to_dict(self, fields=lst_fields)
        item['product_cat'] = self.product_cat.toJSON()
        if self.product_subcat:
            item['product_subcat'] = self.product_subcat.toJSON()
        item['purchase_unit'] = self.purchase_unit.toJSON()
        item['sales_unit'] = self.sales_unit.toJSON()
        item['cost_pu'] = format(self.cost_pu, '.2f')
        item['full_sale_price'] = format(self.full_sale_price, '.2f')
        if self.other_tax:
            item['other_tax'] = format(self.other_tax, '.2f')
        if self.iva:
            item['iva'] = format(self.iva, '.2f')
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        item['qr_code'] = self.get_qr_code()
        return item
    
    def fncDataProductoPedidojsn(self):
        item = model_to_dict(self, fields=[
            'id', 
            'product_desc',
            'sales_unit',
            'full_sale_price',
            'iva'
            ])
        item['value'] = self.product_desc
        item['sales_unit'] = self.sales_unit.fncConsultaUnidadVenta()
        item['full_sale_price'] = format(self.full_sale_price, '.2f')
        if self.iva:
            item['iva'] = format(self.iva, '.2f')
        return item

    def __str__ (self):
        return self.product_desc

#################################################################################################
# 4. CATÁLOGO DE PROVEEDORES
#################################################################################################
''' 4.1 Tabla de catálogo de proveedores'''
class clsCatalogoProveedoresMdl(BaseModel):
    qr_code = models.ImageField(upload_to = 'qr_codes/suppliers/%Y/%m/%d', blank=True)
    person_type = models.CharField('Tipo de persona', max_length=200, choices=PERSON_TYPE)
    id_type = models.CharField('Tipo de identificación', max_length=200, choices=ID_TYPE)
    identification = models.PositiveBigIntegerField('Identificación', unique=True)
    supplier_name = models.CharField('Nombre del proveedor', max_length=200)
    email = models.EmailField('Correo electrónico', max_length=200, blank=True, null=True)
    contact_name = models.CharField('Nombre del contacto', max_length=200)
    contact_cel = models.PositiveBigIntegerField('Celular contacto')
    other_contact_name = models.CharField('Nombre del contacto', max_length=200, blank=True, null=True)
    other_contact_cel = models.PositiveBigIntegerField('Celular contacto', blank=True, null=True)
    department = models.ForeignKey(clsDepartamentosMdl, on_delete=models.CASCADE)
    city = models.ForeignKey(clsCiudadesMdl, on_delete=models.CASCADE)
    supplier_address = models.CharField('Dirección proveedor', max_length=200)
    postal_code = models.PositiveBigIntegerField('Código postal', blank=True, null=True)
    pay_method = models.CharField('Metodo de pago', max_length=200, choices=PAYMETHOD)
    credit_days = models.PositiveSmallIntegerField('Días de crédito', blank=True, null=True)
    credit_limit = models.DecimalField('Cupo de crédito', max_digits=10, decimal_places=2, blank=True, null=True)
    min_purchase_value = models.DecimalField('Valor minimo de compra', max_digits=10, decimal_places=2, blank=True, null=True)
    logistic_condition = models.CharField('Condición de entrega', max_length=200, choices=LOGISTICCONDITION, default='CD')
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')
    objects = DataFrameManager()
    
    class Meta:
        verbose_name = 'Catálogo proveedor'
        verbose_name_plural = 'Catálogo de proveedores'
        ordering = ['state']
        default_permissions = []
        permissions = (('bia_adm_supplier_catalogue', 'Catálogo proveedores'),)

    def get_qr_code(self):
        if self.qr_code:
            return '{}{}'.format(MEDIA_URL, self.qr_code)
        return '{}{}'.format(STATIC_URL, 'img/logo.png')

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        qrcode_img = qrcode.make(self.identification)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.identification}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super(clsCatalogoProveedoresMdl, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['person_type'] = {'id': self.person_type, 'name': self.get_person_type_display()}
        item['id_type'] = {'id': self.id_type, 'name': self.get_id_type_display()}
        item['pay_method'] = {'id': self.pay_method, 'name': self.get_pay_method_display()}
        item['department'] = self.department.toJSON()
        item['city'] = self.city.toJSON()
        item['logistic_condition'] = {'id': self.logistic_condition, 'name': self.get_logistic_condition_display()}
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        item['qr_code'] = self.get_qr_code()
        return item

    def __str__(self):
        return self.supplier_name

''' 4.2 Tabla cantidades mínimas de compra por proveedor'''
class clsCondicionMinimaCompraMdl(BaseModel):
    identification = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    min_amount = models.PositiveSmallIntegerField('Cantidad mínima')
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')
    objects = DataFrameManager()
    
    class Meta:
        verbose_name = 'Compra mínima por producto'
        verbose_name_plural = 'Compras mínimas por producto'
        ordering = ['state']

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsCondicionMinimaCompraMdl, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['identification'] = self.identification.toJSON()
        item['product_code'] = self.product_code.toJSON()
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__(self):
        return self.identification.supplier_name

''' 4.3 Tabla Descuento por proveedor'''
class clsCondicionDescuentoProveedorMdl(BaseModel):
    identification = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    min_amount = models.PositiveSmallIntegerField('Cantidad')
    discount = models.DecimalField('Descuento', max_digits=5, decimal_places=2)
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')
    objects = DataFrameManager()
    
    class Meta:
        verbose_name = 'Descuento de compra por producto'
        verbose_name_plural = 'Descuentos de compra por producto'
        ordering = ['state']

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsCondicionDescuentoProveedorMdl, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['identification'] = self.identification.toJSON()
        item['product_code'] = self.product_code.toJSON()
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__(self):
        return self.identification.supplier_name

#################################################################################################
# 5. CATÁLOGO DE BODEGAS
#################################################################################################
''' 5.1 Tabla de catálogo de bodegas'''
class clsCatalogoBodegasMdl(BaseModel): 
    qr_code = models.ImageField(upload_to = '', blank=True)
    warehouse_name = models.CharField('Nombre bodega', unique=True, max_length=200)
    department = models.ForeignKey(clsDepartamentosMdl, on_delete=models.CASCADE)
    city = models.ForeignKey(clsCiudadesMdl, on_delete=models.CASCADE)
    warehouse_address = models.CharField('Dirección bodega', max_length=200)
    contact_name = models.CharField('Nombre encargado', max_length=200, blank=True, null=True)
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Bodega'
        verbose_name_plural = 'Catálogo de bodegas'
        ordering = ['state']
        permissions = (('bia_adm_warehouse_catalogue', 'Cátalogo bodegas'),)
        
    def get_qr_code(self):
        if self.qr_code:
            return '{}{}'.format(MEDIA_URL, self.qr_code)
        return '{}{}'.format(STATIC_URL, 'img/logo.png')

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.id:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsCatalogoBodegasMdl, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['department'] = self.department.toJSON()
        item['city'] = self.city.toJSON()
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        item['qr_code'] = self.get_qr_code()
        return item

    def __str__(self):
        return self.warehouse_name

#################################################################################################
# 6. LISTAS DE PRECIOS
#################################################################################################
''' 6.1 Tabla de Listas de Precios'''
class clsListaPreciosMdl(BaseModel):
    doc_number = models.CharField('Nº Documento', max_length= 200, blank= True, null= True)
    list_name= models.CharField('Nombre Lista', max_length= 200)
    crossing_doc= models.CharField('Documento Cruce', max_length= 200, blank= True, null= True)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete= models.CASCADE)
    freight= models.DecimalField('Flete', max_digits= 30, decimal_places= 2, blank= True, null= True)
    due_date= models.DateField('Vigencia', blank=True, null=True)
    observations= models.CharField('Observaciones', max_length= 200, blank= True, null= True)
    state = models.CharField('Condición', max_length=200, choices= STATE, default='AC')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Listas de precios'
        verbose_name_plural = 'Lista de precios'
        ordering = ['id']
        permissions = (('bia_adm_listas_precios', 'Listas de precios'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsListaPreciosMdl, self).save()

    def fncConsultaListajsn(self):
        item = model_to_dict(self, fields=['id', 'list_name'])
        return item
    
    def fncConsultaListaPedidosjsn(self):
        item = model_to_dict(self, fields=['store', 'freight'])
        return item
    
    def toJSON(self):
        item = model_to_dict(self)
        item['store'] = self.store.toJSON()
        item['freight'] = format(self.freight, '.2f')
        item['due_date'] = self.due_date.strftime('%Y-%m-%d')
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__(self):
        return self.list_name

''' 6.2 Tabla detalle de listas de precios'''
class clsDetalleListaPreciosMdl(models.Model):
    doc_number= models.ForeignKey(clsListaPreciosMdl, on_delete= models.CASCADE)
    product_code= models.ForeignKey(clsCatalogoProductosMdl, on_delete= models.CASCADE)
    quantity= models.PositiveSmallIntegerField('Cantidad')
    lead_time= models.SmallIntegerField('Tiempo de entrega')
    unit_price= models.DecimalField('Precio Unitario', max_digits= 30, decimal_places= 2)
    observations= models.CharField('Observaciones', max_length= 200, blank= True, null= True)
    objects = DataFrameManager()

    def toJSON(self):
        item = model_to_dict(self, exclude=[self.doc_number])
        item['product_code'] = self.product_code.toJSON()
        item['unit_price'] = format(self.unit_price, '.2f')
        return item

    def fncDetalleListajsn(self):
        item = model_to_dict(self, exclude=[self.doc_number])
        item['product_code'] = self.product_code.id
        item['product_desc'] = self.product_code.product_desc
        item['unit_price'] = format(self.unit_price, '.2f')
        return item
        
    class Meta:
        verbose_name = 'Detalle listas de precios'
        verbose_name_plural = 'Detalle listas de precios'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return str(self.id)

#################################################################################################
# 7. CATÁLOGO DE CLIENTES
#################################################################################################
''' 7.1 Tabla de categoría de cliente'''
class clsCategoriaClienteMdl(BaseModel):
    customer_cat = models.CharField('Nombre de categoría', max_length=200)
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Categoría cliente'
        verbose_name_plural= 'Categorías clientes'
        ordering = ['state']
        default_permissions = []
    
    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsCategoriaClienteMdl, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item
        
    def fncDataCategoriaClienteSlcjsn(self):
        item = model_to_dict(self, fields=['id', 'customer_cat'])
        return item

    def __str__ (self):
        return self.customer_cat
        
''' 7.2 Tabla de margén por categoría de cliente'''
class clsMargenCategoriaClienteMdl(BaseModel):
    customer_cat = models.ForeignKey(clsCategoriaClienteMdl, on_delete=models.CASCADE)
    product_cat = models.ForeignKey(clsCategoriaProductoMdl, on_delete=models.CASCADE)
    margin_min = models.DecimalField('Margen minímo', max_digits=5, decimal_places=2, blank=True, null=True)
    margin_max = models.DecimalField('Margen máximo', max_digits=5, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Margén categoría cliente'
        verbose_name_plural= 'Margénes categoría cliente'
        ordering = ['id']

    
    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsMargenCategoriaClienteMdl, self).save()

    def toJSON(self):
        item = model_to_dict(self,
            exclude=['user_creation', 'user_update']
        )
        item['customer_cat'] = self.customer_cat.toJSON()
        item['product_cat'] = self.product_cat.toJSON()
        item['margin_min'] = format(self.margin_min, '.2f')
        item['margin_max'] = format(self.margin_max, '.2f')
        return item

    def __str__ (self):
        return self.customer_cat.customer_cat

''' 7.3 Tabla de zonas de cliente'''
class clsZonaClienteMdl(BaseModel):
    customer_zone = models.CharField('Zona cliente', max_length=200, unique=True)
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Zona cliente'
        verbose_name_plural= 'Zonas clientes'
        ordering = ['state']
        default_permissions = []
    
    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsZonaClienteMdl, self).save()

    def fncDataZoneSlcjsn(self):
        item = model_to_dict(self, fields=['id', 'customer_zone'])
        return item

    def toJSON(self):
        item = model_to_dict(self)
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__ (self):
        return self.customer_zone

''' 7.4 Tabla asesores comerciales'''
class clsAsesorComercialMdl(BaseModel):
    advisor = models.CharField('Asesor comercial', max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuario')
    zone = models.ForeignKey(clsZonaClienteMdl, on_delete=models.CASCADE, verbose_name='Zona', blank= True, null= True)
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC', blank=True, null=True)
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Asesor comercial'
        verbose_name_plural= 'Asesores comerciales'
        ordering = ['state']
        default_permissions = []
        
    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsAsesorComercialMdl, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__ (self):
        return self.advisor

''' 7.5 Tabla de catálogo de clientes'''
class clsCatalogoClientesMdl(BaseModel):
    qr_code = models.ImageField(upload_to = 'qr_codes/customers/%Y/%m/%d', blank=True)
    person_type = models.CharField('Tipo de persona', max_length=200, choices=PERSON_TYPE, blank=True, null=True)
    id_type = models.CharField('Tipo de identificación', max_length=200, choices=ID_TYPE)
    identification = models.PositiveBigIntegerField('Identificación', unique=True)
    business_name = models.CharField('Nombre del cliente', max_length=200)
    contact_name = models.CharField('Nombre del contacto', max_length=200, blank=True, null=True)
    cel_number = models.PositiveBigIntegerField('Celular')
    email = models.EmailField('Correo electrónico', max_length=200, blank=True, null=True)
    department = models.ForeignKey(clsDepartamentosMdl, on_delete=models.CASCADE, verbose_name='Departamento')
    city = models.ForeignKey(clsCiudadesMdl, on_delete=models.CASCADE,verbose_name='Ciudad')
    customer_zone = models.ForeignKey(clsZonaClienteMdl, on_delete=models.CASCADE, blank= True, null= True, verbose_name='Zona de cliente')
    delivery_address = models.CharField('Dirección entrega', max_length=200)
    del_schedule_init = models.CharField('Horario de entrega inicial', max_length=200, blank=True, null=True)
    del_schedule_end = models.CharField('Horario de entrega final', max_length=200, blank=True, null=True)
    customer_cat = models.ForeignKey(clsCategoriaClienteMdl, on_delete=models.CASCADE, verbose_name='Categoría de cliente')
    commercial_advisor = models.ForeignKey(clsAsesorComercialMdl, on_delete=models.CASCADE, verbose_name='Asesor comercial')
    pay_method = models.CharField('Metodo de pago', max_length=200, choices=PAYMETHOD)
    credit_days = models.PositiveSmallIntegerField('Días de crédito', blank=True, null=True)
    approved_amount = models.DecimalField('Cupo crédito', max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    price_list = models.ForeignKey(clsListaPreciosMdl, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Lista de precios')
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')
    objects = DataFrameManager()
    
    class Meta:
        verbose_name= 'Catálogo cliente'
        verbose_name_plural= 'Catálogo clientes'
        ordering = ['state']
        default_permissions = []
        permissions = (('bia_adm_customer_catalogue', 'Catálogo clientes'),)
    
    def get_qr_code(self):
        if self.qr_code:
            return '{}{}'.format(MEDIA_URL, self.qr_code)
        return '{}{}'.format(STATIC_URL, 'img/logo.png')

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        qrcode_img = qrcode.make(self.identification)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.identification}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super(clsCatalogoClientesMdl, self).save()        
    
    def toJSON(self):
        item = model_to_dict(self)
        item['customer_cat'] = self.customer_cat.toJSON()
        item['customer_zone'] = self.customer_zone.toJSON()
        item['department'] = self.department.toJSON()
        item['city'] = self.city.toJSON()
        item['commercial_advisor'] = self.commercial_advisor.toJSON()
        item['id_type'] = {'id': self.id_type, 'name': self.get_id_type_display()}
        item['pay_method'] = {'id': self.pay_method, 'name': self.get_pay_method_display()}
        if self.price_list:
            item['price_list'] = self.price_list.fncConsultaListajsn()
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        item['qr_code'] = self.get_qr_code()
        return item

    def fncDataClienteSlcjsn(self):
        item = model_to_dict(self, fields=[
            'id',
            'identification',
            'city',
            'cel_number',
            'delivery_address',
            'pay_method',
            'price_list'
        ])
        item['city'] = self.city.fncDataCiudadesSlcjsn()
        item['customer_zone'] = self.customer_zone.fncDataZoneSlcjsn()
        item['pay_method'] = {'id': self.pay_method, 'name': self.get_pay_method_display()}
        item['value'] = self.business_name
        if self.price_list:
            item['price_list'] = self.price_list.fncConsultaListajsn()
        return item
    
    def fncDataClienteCotizacionSlcjsn(self):
        item = model_to_dict(self, fields=[
            'id',
            'identification',
            'city',
            'cel_number',
            'delivery_address',
            'customer_cat',
            'pay_method',
            'price_list'
        ])
        item['city'] = self.city.fncDataCiudadesSlcjsn()
        item['customer_cat'] = self.customer_cat.fncDataCategoriaClienteSlcjsn()
        item['pay_method'] = {'id': self.pay_method, 'name': self.get_pay_method_display()}
        item['value'] = self.business_name
        if self.price_list:
            item['price_list'] = self.price_list.fncConsultaListajsn()
        return item
    
    def __str__ (self):
        return self.business_name

#################################################################################################
# 8. TIEMPOS DE ENTREGA
#################################################################################################
''' 8.1 Tabla de tiempos de entrega'''
class clsTiemposEntregaMdl(BaseModel):
    city = models.ForeignKey(clsCiudadesMdl, on_delete=models.CASCADE)
    customer_zone = models.ForeignKey(clsZonaClienteMdl, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    enlistment_time= models.DecimalField('Tiempo estimado de alistamiento', max_digits= 30, decimal_places= 2)
    travel_time= models.DecimalField('Tiempo estimado de recorrido', max_digits= 30, decimal_places= 2)
    download_time= models.DecimalField('Tiempo estimado de descarga', max_digits= 30, decimal_places= 2)
    total_time= models.DecimalField('Tiempo total estimado', max_digits= 30, decimal_places= 2)
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Tiempo de entrega'
        verbose_name_plural = 'Tiempos de entrega'
        ordering = ['state']
        permissions = (('bia_adm_tiempos_entrega', 'Tiempos de entrega'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.id:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsTiemposEntregaMdl, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['city'] = self.city.toJSON()
        item['customer_zone'] = self.customer_zone.toJSON()
        item['warehouse'] = self.warehouse.toJSON()
        item['enlistment_time'] = format(self.enlistment_time, '.2f')
        item['travel_time'] = format(self.travel_time, '.2f')
        item['download_time'] = format(self.download_time, '.2f')
        item['total_time'] = format(self.total_time, '.2f')
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__(self):
        return str(self.id)

#################################################################################################
# 9. HISTORICO DE MOVIMIENTOS ALTERNO
#################################################################################################
''' 9.1 Tabla de historico de pedidos'''
class clsHistoricoPedidosMdl(models.Model):
    date_creation = models.DateTimeField('Fecha creación')
    doc_number = models.CharField('Nº Documento', max_length=200)
    identification = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    pay_method = models.CharField('Metodo de pago', max_length=200, choices=PAYMETHOD, blank=True, null=True)
    delivery_date = models.DateTimeField('Fecha entrega')
    city = models.ForeignKey(clsCiudadesMdl, on_delete=models.CASCADE, blank=True, null=True)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unit_price = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, blank=True, null=True)
    iva = models.DecimalField('Iva', max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    condition = models.CharField('Condición', max_length=200, choices=ORDERCONDITION)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Historico pedidos'
        verbose_name_plural = 'Historico pedidos'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.identification.business_name

''' 9.2 Tabla de ordenes de compra'''
class clsHistoricoOrdenesCompraMdl(models.Model):
    date_creation = models.DateTimeField('Fecha creación')
    doc_number = models.CharField('Nº Documento', max_length=200)
    identification = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE)
    delivery_date = models.DateTimeField('Fecha entrega')
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unit_price = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField('Subtotal', max_digits=10, decimal_places=2)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    condition = models.CharField('Condición', max_length=200, choices=STATEORDER)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Historico ordenes de compra'
        verbose_name_plural = 'Historico ordenes de compra'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.identification.supplier_name

''' 9.3 Tabla de historico alterno de movimientos'''
class clsHistoricoMovimientosAlternoMdl(models.Model):
    creation_date = models.CharField('Fecha de creación', max_length=200)
    doc_number = models.CharField('Nº Documento', max_length=200)
    document_type = models.CharField('Tipo de documento', max_length=200)
    type = models.CharField('Tipo de movimiento', max_length=200)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.CharField('Fecha vencimiento', max_length=200)
    unitary_cost = models.DecimalField('Costo unitario', max_digits=10, decimal_places=2)
    total_cost = models.DecimalField('Costo total', max_digits=10, decimal_places=2)
    crossing_doc = models.CharField('Documento cruce', max_length=200)
    condition = models.CharField('Condición', max_length=200)
    pre_bal = models.SmallIntegerField('Presaldo')
    balance = models.SmallIntegerField('Saldo')
    inv_value = models.DecimalField('Costo total', max_digits=10, decimal_places=2)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    identification = models.PositiveBigIntegerField('Identificación')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Historico de movimiento Alterno'
        verbose_name_plural = 'Historico de movimientos Alterno'
        ordering = ['id']
        permissions = (('bia_adm_historico_movimientos_alterno', 'Histórico de movimientos alterno'),)

    def __str__(self):
        return self.doc_number

#################################################################################################
# 10. AJUSTES DE INVENTARIO
#################################################################################################
''' 10.1 Tabla ajustes de inventario'''
class clsAjusteInventarioMdl(BaseModel):
    doc_number = models.CharField('Nº Documento', max_length=200, blank=True, null=True)
    total_cost = models.DecimalField('Total costo', max_digits=30, decimal_places=2)
    condition = models.CharField('Condición', max_length=200, choices=INCOMECONDITION, default='CE')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Ajuste inventario'
        verbose_name_plural = 'Ajustes de inventario'
        ordering = ['id']
        permissions = (('bia_adm_ajustes_inventario', 'Ajustes de inventario'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsAjusteInventarioMdl, self).save()

    def __str__(self):
        return str(self.id)

''' 10.2 Tabla detalle ajustes de inventario'''
class clsDetalleAjusteInventarioMdl(models.Model):
    doc_number = models.ForeignKey(clsAjusteInventarioMdl, on_delete=models.CASCADE)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    type = models.CharField('Tipo de ajuste', max_length=200, choices=INCOMETYPE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    batch = models.CharField('Lote', max_length=200, blank=True, null=True)
    expiration_date = models.DateField('Fecha vencimiento', blank=True, null=True)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unitary_cost = models.DecimalField('Costo unitario', max_digits=10, decimal_places=2, blank=True, null=True)
    total_cost = models.DecimalField('Total costo', max_digits=20, decimal_places=2)
    
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Ajuste inventario'
        verbose_name_plural = 'Ajustes de inventario'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return str(self.id)

#################################################################################################
# 11. ENTRADAS DE ALMACEN
#################################################################################################
''' 11.1 Tabla de entradas de almacén'''
class clsEntradasAlmacenMdl(BaseModel):
    doc_number = models.CharField('Nº Documento', max_length= 200, blank=True, null=True)
    identification = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE)
    total_cost = models.DecimalField('Costo total', max_digits= 30, decimal_places= 2)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    crossing_doc = models.CharField('Documento cruce', max_length=200)
    condition = models.CharField('Condición', max_length=200, choices=INCOMECONDITION)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Entrada de almacén'
        verbose_name_plural = 'Entradas de almacén'
        ordering = ['id']
        permissions = (('bia_log_entradas_almacen', 'Entradas de almacén'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsEntradasAlmacenMdl, self).save()

    def __str__(self):
        return str(self.id)

''' 11.2 Tabla detalle de entradas de almacén'''
class clsDetalleEntradaAlmacen(models.Model):
    doc_number = models.ForeignKey(clsEntradasAlmacenMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unitary_cost = models.DecimalField('Costo unitario', max_digits= 30, decimal_places=2)
    total_cost = models.DecimalField('Costo total', max_digits= 30, decimal_places=2)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    state = models.CharField('Estado', max_length=200, choices=VALIDARCANTIDAD)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Detalle entrada de almacén'
        verbose_name_plural = 'Detalle entradas de almacén'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return str(self.id)

#################################################################################################
# 12. DEVOLUCIONES CLIENTE
#################################################################################################
''' 12.1 Tabla de devoluciones de cliente'''
class clsDevolucionesClienteMdl(BaseModel):
    doc_number = models.CharField('Nº Documento', max_length=200)
    returnin_type = models.CharField('Tipo de retorno', max_length=200)
    identification = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    total_cost = models.DecimalField('Costo total', max_digits=10, decimal_places=2)
    condition = models.CharField('Condición', max_length=200, choices=WAREHOUSEEXIT)
    crossing_doc = models.CharField('Documento cruce', max_length=200)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Devolución cliente'
        verbose_name_plural = 'Devoluciones clientes'
        ordering = ['id']
        default_permissions = []

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsDevolucionesClienteMdl, self).save()

    def __str__(self):
        return str(self.id)

''' 12.2 Tabla detalle de devoluciones de cliente'''
class clsDetalleDevolucionesClienteMdl(models.Model):
    doc_number = models.ForeignKey(clsDevolucionesClienteMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unitary_cost = models.DecimalField('Costo unitario', max_digits=10, decimal_places=2)
    total_cost = models.DecimalField('Costo total', max_digits=10, decimal_places=2)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    state = models.CharField('Estado', max_length=200, choices=VALIDARCANTIDAD)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Detalle devolución cliente'
        verbose_name_plural = 'Detalle devoluciones cliente'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return str(self.id)

#################################################################################################
# 13. DEVOLUCIONES PROVEEDOR
#################################################################################################
''' 13.1 Tabla de devoluciones a proveedor'''
class clsDevolucionesProveedorMdl(BaseModel):
    doc_number = models.CharField('Nº Documento', max_length=200)
    returnin_type = models.CharField('Tipo de retorno', max_length=200)
    identification = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE)
    total_cost = models.DecimalField('Costo total', max_digits=10, decimal_places=2)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    condition = models.CharField('Condición', max_length=200, choices=WAREHOUSEEXIT)
    crossing_doc = models.CharField('Documento cruce', max_length=200)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Devolución proveedor'
        verbose_name_plural = 'Devoluciones proveedores'
        ordering = ['id']
        default_permissions = []

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsDevolucionesProveedorMdl, self).save()

    def __str__(self):
        return str(self.id)

''' 13.2 Tabla detalle de devolución de proveedor'''
class clsDetalleDevolucionesProveedorMdl(models.Model):
    doc_number = models.ForeignKey(clsDevolucionesProveedorMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unitary_cost = models.DecimalField('Costo unitario', max_digits=10, decimal_places=2)
    total_cost = models.DecimalField('Costo total', max_digits=10, decimal_places=2)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    state = models.CharField('Estado', max_length=200, choices=VALIDARCANTIDAD)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Detalle devolución proveedor'
        verbose_name_plural = 'Detalle devoluciones proveedor'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return str(self.id)

#################################################################################################
# 14. SALIDAS DE ALMACEN
#################################################################################################
''' 14.1 Tabla de salidas de almacén'''
class clsSalidasAlmacenMdl(BaseModel):
    doc_number = models.CharField('Nº Documento', max_length=200)
    identification = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2)
    taxes = models.DecimalField('Impuestos', max_digits=10, decimal_places=2)
    total_price = models.DecimalField('Precio total', max_digits=10, decimal_places=2)
    total_amount = models.DecimalField('Total', max_digits=10, decimal_places=2)
    total_cost = models.DecimalField('Costo total', max_digits=10, decimal_places=2, blank=True, null=True)
    value_paid = models.DecimalField('Valor pagado', max_digits=10, decimal_places=2)
    credit_state = models.CharField('Estado crédito', max_length=200, choices=INCOMECONDITION)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    crossing_doc = models.CharField('Documento cruce', max_length=200)
    condition = models.CharField('Condición', max_length=200, choices=WAREHOUSEEXIT)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Salida de almacén'
        verbose_name_plural = 'Salidas de almacén'
        ordering = ['id']
        permissions = (('bia_log_salidas_almacen', 'Salidas de almacén'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsSalidasAlmacenMdl, self).save()

    def __str__(self):
        return str(self.id)

''' 14.2 Tabla detalle de salidas de almacen'''
class clsDetalleSalidasAlmacenMdl(models.Model):
    doc_number = models.ForeignKey(clsSalidasAlmacenMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unit_price = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2)
    taxes = models.DecimalField('Impuestos', max_digits=10, decimal_places=2)
    total_price = models.DecimalField('Precio total', max_digits=10, decimal_places=2)
    total_amount = models.DecimalField('Total', max_digits=10, decimal_places=2)
    unitary_cost = models.DecimalField('Costo unitario', max_digits=10, decimal_places=2, blank=True, null=True)
    total_cost = models.DecimalField('Costo total', max_digits=10, decimal_places=2, blank=True, null=True)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    state = models.CharField('Estado', max_length=200, choices=VALIDARCANTIDAD)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Detalle salida de almacén'
        verbose_name_plural = 'Detalle salidas de almacén'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return str(self.id)

#################################################################################################
# 15. OBSEQUIOS
#################################################################################################
''' 15.1 Tabla de obsequios'''
class clsObsequiosMdl(BaseModel):
    doc_number = models.CharField('Nº Documento', max_length=200)
    identification = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    total_cost = models.DecimalField('Total costo', max_digits=10, decimal_places=2)
    condition = models.CharField('Condición', max_length=200, choices=WAREHOUSEEXIT)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Obsequio'
        verbose_name_plural = 'Obsequios'
        ordering = ['id']
        default_permissions = []

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsObsequiosMdl, self).save()

    def __str__(self):
        return str(self.id)

''' 15.2 Tabla detalle de obsequios'''
class clsDetalleObsequiosMdl(models.Model):
    doc_number = models.ForeignKey(clsObsequiosMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unitary_cost = models.DecimalField('Costo unitario', max_digits=10, decimal_places=2)
    total_cost = models.DecimalField('Total costo', max_digits=10, decimal_places=2)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    state = models.CharField('Estado', max_length=200, choices=VALIDARCANTIDAD)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Detalle obsequio'
        verbose_name_plural = 'Detalle obsequios'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return str(self.id)

#################################################################################################
# 16. TRASLADOS DE BODEGA
#################################################################################################
''' 16.1 Tabla de traslados entre bodegas'''
class clsTrasladosBodegasMdl(BaseModel):
    doc_number = models.CharField('Nº Documento', max_length=200)
    identification = models.PositiveBigIntegerField('Identificación')
    total_cost = models.DecimalField('Total costo', max_digits=10, decimal_places=2)
    condition = models.CharField('Condición', max_length=200, choices=WAREHOUSEEXIT)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Traslado bodega'
        verbose_name_plural = 'Traslados bodegas'
        ordering = ['id']
        default_permissions = []

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsTrasladosBodegasMdl, self).save()

    def __str__(self):
        return str(self.id)

''' 16.2 Tabla detalle de traslados entre bodegas'''
class clsDetalleTrasladosBodegaMdl(models.Model):
    doc_number = models.ForeignKey(clsTrasladosBodegasMdl, on_delete=models.CASCADE)
    type = models.CharField('Tipo de traslado', max_length=200, choices=INCOMETYPE, blank=True, null=True)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE, blank=True, null=True)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unitary_cost = models.DecimalField('Costo unitario', max_digits=10, decimal_places=2)
    total_cost = models.DecimalField('Total costo', max_digits=10, decimal_places=2)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    state = models.CharField('Estado', max_length=200, choices=VALIDARCANTIDAD)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Detalle traslado bodega'
        verbose_name_plural = 'Detalle traslados bodegas'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return str(self.id)

#################################################################################################
# 17. SALDOS DE INVENTARIO
#################################################################################################
''' 17.1 Tabla de saldos de inventario'''
class clsSaldosInventarioMdl(models.Model):
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    batch = models.CharField('Lote', max_length=200)
    inventory_avail = models.PositiveSmallIntegerField('Saldo disponible')
    expiration_date = models.CharField('Fecha vencimiento', max_length=200)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Saldo inventario'
        verbose_name_plural = 'Saldos inventarios'
        ordering = ['id']
        permissions = (('bia_log_saldos_inventario', 'Saldos de inventario'),)

    def fncDataSaldosProductojsn(self):
        item = model_to_dict(self, fields=['inventory_avail'])
        return item

    def __str__(self):
        return self.product_code.product_desc

#################################################################################################
# 18. HISTORICO REAL DE MOVIMIENTOS
#################################################################################################
''' 18.1 Tabla de historico real de movimientos'''
class clsHistoricoMovimientosMdl(models.Model):
    creation_date = models.CharField('Fecha de creación', max_length=200)
    doc_number = models.CharField('Nº Documento', max_length=200)
    document_type = models.CharField('Tipo de documento', max_length=200)
    type = models.CharField('Tipo de movimiento', max_length=200)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.CharField('Fecha vencimiento', max_length=200)
    unitary_cost = models.DecimalField('Costo unitario', max_digits=10, decimal_places=2)
    total_cost = models.DecimalField('Costo total', max_digits=10, decimal_places=2)
    crossing_doc = models.CharField('Documento cruce', max_length=200)
    condition = models.CharField('Condición', max_length=200)
    pre_bal = models.SmallIntegerField('Presaldo')
    balance = models.PositiveSmallIntegerField('Saldo')
    inv_value = models.DecimalField('Costo total', max_digits=10, decimal_places=2)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    identification = models.CharField('Identificación', max_length= 200)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Historico de movimiento'
        verbose_name_plural = 'Historico de movimientos'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.doc_number

#################################################################################################
# 19. PEDIDOS
#################################################################################################
''' 19.1 Tabla de pedidos'''
class clsPedidosMdl(BaseModel):
    doc_number = models.CharField('Nº Documento', max_length= 200, blank= True, null= True)
    identification = models.ForeignKey(clsCatalogoClientesMdl, on_delete= models.CASCADE)
    city= models.ForeignKey(clsCiudadesMdl, on_delete= models.CASCADE, blank=True, null=True)
    customer_zone = models.ForeignKey(clsZonaClienteMdl, on_delete=models.CASCADE, blank= True, null= True)
    delivery_address = models.CharField('Dirección entrega', max_length=200, blank=True, null=True)
    delivery_date= models.DateField('Fecha de entrega')
    subtotal= models.DecimalField('Subtotal', max_digits= 30, decimal_places= 2)
    iva= models.DecimalField('Iva', max_digits= 10, decimal_places= 2, blank=True, null=True)
    discount= models.DecimalField('Descuento', max_digits= 20, decimal_places= 2, blank=True, null=True)
    total= models.DecimalField('Total', max_digits= 30, decimal_places= 2)
    observations= models.CharField('Observaciones', max_length= 200, blank=True, null=True)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete= models.CASCADE)
    condition = models.CharField('Condición', max_length=200, choices= STATEORDER, default='AB')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Pedidos'
        verbose_name_plural = 'Pedidos'
        ordering = ['id']
        permissions = (('bia_com_pedidos', 'Pedidos'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsPedidosMdl, self).save()

    def fncDataPedidosjsn(self):
        item = model_to_dict(self, fields=[
            'id',
            'doc_number',
            'creation_date',
            'delivery_date',
            'subtotal',
            'iva',
            'discount',
            'total',
        ])
        item['creation_date'] = self.creation_date.strftime('%Y-%m-%d')
        item['business_name'] = self.identification.business_name
        item['identification'] = self.identification.identification
        item['city'] = self.identification.city.city_name
        item['customer_zone'] = self.identification.customer_zone.customer_zone
        item['delivery_address'] = self.identification.delivery_address
        item['store'] = self.store.warehouse_name
        item['delivery_date'] = self.delivery_date.strftime('%Y-%m-%d')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['discount'] = format(self.discount, '.2f')
        item['total'] = format(self.total, '.2f')
        item['condition'] = {'id': self.condition, 'name': self.get_condition_display()}
        return item

    def __str__(self):
        return str(self.id)

''' 19.2 Tabla detalle de pedidos'''
class clsDetallePedidosMdl(models.Model):
    doc_number = models.ForeignKey(clsPedidosMdl, on_delete= models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete= models.CASCADE, verbose_name='Producto')
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unit_price = models.DecimalField('Precio unitario', max_digits= 10, decimal_places= 2)
    subtotal = models.DecimalField('Subtotal', max_digits= 30, decimal_places= 2)
    iva = models.DecimalField('IVA', max_digits= 10, decimal_places= 2)
    total= models.DecimalField('Total', max_digits= 30, decimal_places= 2)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Detalle pedidos'
        verbose_name_plural = 'Detalle pedidos'
        ordering = ['id']
        default_permissions = []

    def fncDataDetallePedidojsn(self):
        item = model_to_dict(self, fields=[
            'id',
            'quantity',
            'unit_price',
            'subtotal',
            'iva',
            'total',
        ])
        item['product_code'] = self.product_code.id
        item['product_desc'] = self.product_code.product_desc
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        return item

    def __str__(self):
        return str(self.id)

#################################################################################################
# 20. ORDENES DE COMPRA
#################################################################################################
''' 20.1 Tabla de ordenes de compra'''
class clsOrdenesCompraMdl(BaseModel):
    doc_number = models.CharField('Nº Documento', max_length= 200, blank= True, null= True)
    identification = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete= models.CASCADE)
    delivery_date= models.DateTimeField('Fecha de entrega', blank= True, null= True)
    subtotal= models.DecimalField('Subtotal', max_digits= 30, decimal_places= 2)
    iva= models.DecimalField('IVA', max_digits= 10, decimal_places= 2)
    discount= models.DecimalField('Descuento', max_digits= 20, decimal_places= 2)
    total= models.DecimalField('Total', max_digits= 30, decimal_places= 2)
    observations= models.CharField('Observaciones', max_length= 200)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete= models.CASCADE)
    condition = models.CharField('Condición', max_length=200, choices= STATEORDER)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Pedidos'
        verbose_name_plural = 'Pedidos'
        ordering = ['id']
        permissions = (('bia_pur_ordenes_compra', 'Ordenes de compra'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsOrdenesCompraMdl, self).save()

    def fncOrdenCompraDetallejsn(self):
        item = model_to_dict(self, fields=[
            'delivery_date', 'condition'
            ])
        item['delivery_date'] = self.delivery_date.strftime('%Y-%m-%d')
        item['condition'] = {'id': self.condition, 'name': self.get_condition_display()}
        return item

    def __str__(self):
        return str(self.id)

''' 20.2 Tabla detalle de ordenes de compra'''
class clsDetalleOrdenesCompraMdl(models.Model):
    doc_number = models.ForeignKey(clsOrdenesCompraMdl, on_delete= models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete= models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unit_price = models.DecimalField('Precio unitario', max_digits= 10, decimal_places= 2)
    subtotal = models.DecimalField('Subtotal', max_digits= 30, decimal_places= 2)
    iva = models.DecimalField('Iva', max_digits= 10, decimal_places= 2)
    total= models.DecimalField('Total', max_digits= 30, decimal_places= 2)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Detalle ordenes de compra'
        verbose_name_plural = 'Detalle ordenes de compra'
        ordering = ['id']
        default_permissions = []

    def fncDetalleOrdenComprajsn(self):
        item = model_to_dict(self, fields=['doc_number', 'product_code', 'quantity'])
        item['doc_number'] = self.doc_number.doc_number
        item['product_code'] = self.product_code.id
        item['order'] = [ i.fncOrdenCompraDetallejsn() for i in self.clsordenescompramdl_set.all() ]
        return item

    def __str__(self):
        return str(self.id)
        
#################################################################################################
# 21. COTIZACIONES
#################################################################################################
''' 21.1 Tabla de Cotizaciones'''
class clsCotizacionesMdl(BaseModel):
    doc_number = models.CharField('Nº Documento', max_length= 200, blank= True, null= True)
    identification= models.ForeignKey(clsCatalogoClientesMdl, on_delete= models.CASCADE)
    city= models.ForeignKey(clsCiudadesMdl, on_delete= models.CASCADE)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete= models.CASCADE)
    freight= models.DecimalField('Flete', max_digits= 30, decimal_places= 2)
    general_obs= models.CharField('Observaciones Generales', max_length= 200, blank= True, null= True)
    follow_up_date= models.DateTimeField('Fecha de seguimiento')
    subtotal= models.DecimalField('Subtotal', max_digits= 30, decimal_places= 2, blank=True, null=True)
    iva= models.DecimalField('IVA', max_digits= 10, decimal_places= 2, blank=True, null=True)
    total= models.DecimalField('Total', max_digits= 30, decimal_places= 2, blank=True, null=True)
    condition= models.CharField('Condición', max_length= 200, choices= STATEORDER, default='AB')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Cotizaciones'
        verbose_name_plural = 'Cotizaciones'
        ordering = ['id']
        permissions = (('bia_com_cotizacion_cliente', 'Cotización cliente'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsCotizacionesMdl, self).save()

    def __str__(self):
        return str(self.id)

''' 21.2 Tabla detalle de cotizaciones'''
class clsDetalleCotizacionesMdl(models.Model):
    doc_number= models.ForeignKey(clsCotizacionesMdl, on_delete= models.CASCADE)
    product_code= models.ForeignKey(clsCatalogoProductosMdl, on_delete= models.CASCADE)
    quantity= models.PositiveSmallIntegerField('Cantidad')
    lead_time= models.SmallIntegerField('Tiempo de entrega')
    unit_price= models.DecimalField('Precio Unitario', max_digits= 30, decimal_places= 2)
    due_date= models.DateTimeField('Vigencia')
    observations= models.CharField('Observaciones', max_length= 200, blank= True, null= True)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Detalle cotizaciones'
        verbose_name_plural = 'Detalle cotizaciones'
        ordering = ['id']
        default_permissions = []        

    def __str__(self):
        return str(self.id)

#################################################################################################
# 22. INDICADORES COMERCIALES
#################################################################################################
''' 22.1 Tabla indicadores comerciales'''
class clsIndicadoresComercialesMdl(models.Model):
    creation_date =  models.DateTimeField('Fecha creación')
    measurement_date = models.DateTimeField('Fecha medición', blank=True, null=True)
    indicator = models.CharField('Indicador', max_length=200)
    set = models.CharField('Conjunto', max_length=200, blank=True, null=True) 
    subset= models.CharField('Subconjunto', max_length=200, blank=True, null=True)
    objetive = models.DecimalField('Objetivo', max_digits=10, decimal_places=2, blank=True, null=True)
    real = models.DecimalField('Real', max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment = models.DecimalField('Cumplimiento', max_digits=10, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Indicador comercial'
        verbose_name_plural = 'Indicadores comerciales'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.set

#################################################################################################
# 23. ACTIVIDADES COMERCIALES
#################################################################################################
''' 23.1 Tabla actividades comercial'''
class clsActividadesComercialMdl(models.Model):
    task_date =  models.DateTimeField('Fecha actividad')
    start_hour = models.CharField('Hora inicio', max_length=200)
    end_hour = models.CharField('Hora fin', max_length=200)
    identification = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    task = models.CharField('Actividad', max_length=200)
    customer_state =  models.CharField('Estado cliente', max_length=200, choices=ESTADOCLIENTE, blank=True, null=True)
    objetive = models.CharField('Objetivo', max_length=600, choices=OBJETIVOACTIVIDAD, blank=True, null=True)
    observation = models.CharField('Observación', max_length=200)
    condition = models.CharField('Condición', max_length=200, choices=STATE, default='AC')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Actividad comercial'
        verbose_name_plural = 'Actividades comerciales'
        ordering = ['id']
        default_permissions = []

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsActividadesComercialMdl, self).save()

    def __str__(self):
        return self.task

#################################################################################################
# 24. PROMOCIONES
#################################################################################################
''' 24.1 Tabla promociones'''
class clsPromocionesMdl(models.Model):
    doc_number = models.CharField('Nº Documento', max_length=200, blank=True, null=True)
    promo_name = models.CharField('Nombre promoción', max_length=200)
    deadline_for_sale = models.DateTimeField('Fecha vigencia')
    promo_quantity = models.SmallIntegerField('Cantidad')
    promo_price = models.DecimalField('Precio promoción', max_digits=20, decimal_places=2)
    promo_object = models.CharField('Objeto promoción', max_length=200)
    auts = models.SmallIntegerField('Unidades autorizadas por cliente')
    condition = models.CharField('Condición', max_length=200, choices=STATE)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Promoción'
        verbose_name_plural = 'Promociones'
        ordering = ['id']
        permissions = (('bia_pur_promociones', 'Promociones'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsPromocionesMdl, self).save()

    def __str__(self):
        return self.promo_name

''' 24.2 Tabla detalle productos promociones'''
class clsDetalleProductosPromocionesMdl(models.Model):
    doc_number = models.ForeignKey(clsPromocionesMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Detalle producto promoción'
        verbose_name_plural = 'Detalle productos promociones'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return str(self.doc_number)

''' 24.3 Tabla detalle clientes promociones'''
class clsDetalleClientesPromocionesMdl(models.Model):
    doc_number = models.ForeignKey(clsPromocionesMdl, on_delete=models.CASCADE)
    identification = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Detalle cliente promoción'
        verbose_name_plural = 'Detalle clientes promociones'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return str(self.doc_number)

''' 24.4 Tabla detalle filtros'''
class clsDetalleFiltrosPromocionesMdl(models.Model):
    doc_number = models.ForeignKey(clsPromocionesMdl, on_delete=models.CASCADE)
    filter = models.CharField('Filtro', max_length=200)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Detalle filtro promoción'
        verbose_name_plural = 'Detalle filtros promociones'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return str(self.doc_number)

#################################################################################################
# 25. EVALUACIÓN PROVEEDOR
#################################################################################################
''' 25.1 Tabla evaluación proveedor'''
class clsEvaluacionProveedorMdl(models.Model):
    order_purchase = models.ForeignKey(clsOrdenesCompraMdl, on_delete= models.CASCADE)
    incomes = models.ForeignKey(clsEntradasAlmacenMdl, on_delete=models.CASCADE)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Evaluación proveedor'
        verbose_name_plural = 'Evaluaciones de proveedor'
        ordering = ['id']
        permissions = (('bia_pur_evaluacion_proveedor', 'Evaluación proveedor'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsEvaluacionProveedorMdl, self).save()

    def __str__(self):
        return str(self.id)

#################################################################################################
# 26. INDICADORES COMPRAS
#################################################################################################
''' 26.1 Tabla indicadores compras'''
class clsIndicadoresComprasMdl(models.Model):
    measurement_date = models.DateTimeField('Fecha medición', blank=True, null=True)
    indicator = models.CharField('Indicador', max_length=200)
    objetive = models.DecimalField('Objetivo', max_digits=10, decimal_places=2, blank=True, null=True)
    real = models.DecimalField('Real', max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment = models.DecimalField('Cumplimiento', max_digits=10, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Indicador compras'
        verbose_name_plural = 'Indicadores compras'
        ordering = ['id']
        default_permissions = []

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsIndicadoresComprasMdl, self).save()

    def __str__(self):
        return str(self.id)

#################################################################################################
# 27. INDICADORES ALMACEN
#################################################################################################
''' 27.1 Tabla indicadores almacen'''
class clsIndicadoresAlmacenMdl(models.Model):
    measurement_date = models.DateTimeField('Fecha medición', blank=True, null=True)
    indicator = models.CharField('Indicador', max_length=200)
    objetive = models.DecimalField('Objetivo', max_digits=10, decimal_places=2, blank=True, null=True)
    real = models.DecimalField('Real', max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment = models.DecimalField('Cumplimiento', max_digits=10, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Indicador almacen'
        verbose_name_plural = 'Indicadores almacen'
        ordering = ['id']
        default_permissions = []

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsIndicadoresAlmacenMdl, self).save()

    def __str__(self):
        return str(self.id)

#################################################################################################
# 28. VENTAS PERDIDAS
#################################################################################################
''' 28.1 Tabla ventas perdidas'''
class clsVentasPerdidasMdl(models.Model):
    date = models.DateTimeField('Fecha')
    identification = models.ForeignKey(clsCatalogoClientesMdl, on_delete= models.CASCADE, verbose_name='Cliente')
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete= models.CASCADE, verbose_name='Producto')
    quantity = models.PositiveSmallIntegerField('Cantidad')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Venta perdida'
        verbose_name_plural = 'Ventas perdidas'
        ordering = ['id']
        default_permissions = []

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(clsVentasPerdidasMdl, self).save()

    def __str__(self):
        return str(self.id)

#################################################################################################
# FUNCIONES POSTSAVE PARA BASES DE DATOS
#################################################################################################

# Función que genera un nuevo # de documento a la tabla
# sender: Tabla de datos
# instance: Instancia del modelo
def fncGenerarNumeroDocumento(sender, instance, **kwargs):
    if sender == clsAjusteInventarioMdl:
        clsAjusteInventarioMdl.objects.filter(pk=instance.pk).update(doc_number=f'AJS-{instance.pk}')
    elif sender == clsEntradasAlmacenMdl:
        clsEntradasAlmacenMdl.objects.filter(pk=instance.pk).update(doc_number=f'ENT-{instance.pk}')
    elif sender == clsDevolucionesClienteMdl:
        clsDevolucionesClienteMdl.objects.filter(pk=instance.pk).update(doc_number=f'DEC-{instance.pk}')
    elif sender == clsDevolucionesProveedorMdl:
        clsDevolucionesProveedorMdl.objects.filter(pk=instance.pk).update(doc_number=f'DEP-{instance.pk}')
    elif sender == clsSalidasAlmacenMdl:
        clsSalidasAlmacenMdl.objects.filter(pk=instance.pk).update(doc_number=f'SLD-{instance.pk}')
    elif sender == clsObsequiosMdl:
        clsObsequiosMdl.objects.filter(pk=instance.pk).update(doc_number=f'OBS-{instance.pk}')
    elif sender == clsTrasladosBodegasMdl:
        clsTrasladosBodegasMdl.objects.filter(pk=instance.pk).update(doc_number=f'TRL-{instance.pk}')
    elif sender== clsPedidosMdl:
        clsPedidosMdl.objects.filter(pk= instance.pk).update(doc_number= f'PED-{instance.pk}')
    elif sender== clsOrdenesCompraMdl:
        clsOrdenesCompraMdl.objects.filter(pk= instance.pk).update(doc_number= f'OCM-{instance.pk}')
    elif sender== clsListaPreciosMdl:
        clsListaPreciosMdl.objects.filter(pk= instance.pk).update(doc_number= f'LTP-{instance.pk}')
    elif sender== clsCotizacionesMdl:
        clsCotizacionesMdl.objects.filter(pk= instance.pk).update(doc_number= f'COT-{instance.pk}')
    
# Función que genera un nuevo QR-CODE para una instancia de una tabla
# sender: Tabla de datos
# instance: Instancia del modelo
def fncGenerarQrCode(sender, instance, **kwargs):
    if not instance.qr_code:
        qrcode_img = qrcode.make(instance.id)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_codes/bodegas/qr_code-{instance.id}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        instance.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        if sender == clsCatalogoBodegasMdl:
            clsCatalogoBodegasMdl.objects.filter(pk=instance.pk).update(qr_code=fname)
        else:
            clsCatalogoProductosMdl.objects.filter(pk=instance.pk).update(qr_code=fname)
    else:
        pass

post_save.connect(fncGenerarNumeroDocumento, sender=clsAjusteInventarioMdl)
post_save.connect(fncGenerarNumeroDocumento, sender=clsEntradasAlmacenMdl)
post_save.connect(fncGenerarNumeroDocumento, sender=clsDevolucionesClienteMdl)
post_save.connect(fncGenerarNumeroDocumento, sender=clsDevolucionesProveedorMdl)
post_save.connect(fncGenerarNumeroDocumento, sender=clsSalidasAlmacenMdl)
post_save.connect(fncGenerarNumeroDocumento, sender=clsObsequiosMdl)
post_save.connect(fncGenerarNumeroDocumento, sender=clsTrasladosBodegasMdl)
post_save.connect(fncGenerarNumeroDocumento, sender= clsPedidosMdl)
post_save.connect(fncGenerarNumeroDocumento, sender= clsOrdenesCompraMdl)
post_save.connect(fncGenerarNumeroDocumento, sender= clsListaPreciosMdl)
post_save.connect(fncGenerarNumeroDocumento, sender= clsCotizacionesMdl)
post_save.connect(fncGenerarQrCode, sender= clsCatalogoProductosMdl)
post_save.connect(fncGenerarQrCode, sender= clsCatalogoBodegasMdl)