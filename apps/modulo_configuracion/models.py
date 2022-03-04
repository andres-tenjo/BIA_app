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


''' Tablas para carga inicial'''
# Tabla departamentos
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

# Tabla ciudades
class clsCiudadesMdl(BaseModel):
    city_name = models.CharField('Ciudad', max_length=200)
    department = models.ForeignKey(clsDepartamentosMdl, on_delete=models.CASCADE)
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Ciudad'
        verbose_name_plural= 'Ciudades'
        ordering = ['id']
    
    def toJSON(self):
        item = model_to_dict(self)
        item['department'] = self.department.toJSON()
        return item

    def __str__ (self):
        return self.city_name


''' Tabla perfil empresa'''
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


 
''' Tablas catálogo de productos '''
# Tabla categoría de producto
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

# Tabla subcategoría de producto
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

# Tabla unidad de compra de producto
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

# Tabla unidad de venta de un producto
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

    def __str__ (self):
        return self.sales_unit

# Tabla catálogo de productos
class clsCatalogoProductosMdl(BaseModel):
    qr_code = models.ImageField(upload_to = 'qr_codes/products/%Y/%m/%d', blank=True)
    product_desc = models.CharField('Nombre del producto', max_length=200)
    bar_code = models.PositiveBigIntegerField('Código de barras', unique=True, blank=True, null=True)
    trademark = models.CharField('Marca del producto', max_length=200)
    product_cat = models.ForeignKey(clsCategoriaProductoMdl, on_delete=models.CASCADE, verbose_name='Categoría')
    product_subcat = models.ForeignKey(clsSubcategoriaProductoMdl, on_delete=models.CASCADE, verbose_name='Subcategoría')
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
        qrcode_img = qrcode.make(self.id)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.id}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super(clsCatalogoProductosMdl, self).save(*args, **kwargs)

    def toJSON(self, lst_fields=None):
        item = model_to_dict(self, fields=lst_fields)
        item['product_cat'] = self.product_cat.toJSON()
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

    def __str__ (self):
        return self.product_desc


''' Tablas catálogo de proveedores '''
# Tabla de catálogo de proveedores
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

# Tabla cantidades mínimas de compra por proveedor
class clsCondicionMinimaCompraMdl(BaseModel):
    supplier = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE)
    product = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
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
        item['supplier'] = self.supplier.toJSON()
        item['product'] = self.product.toJSON()
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__(self):
        return self.supplier.supplier_name

# Tabla Descuento por proveedor
class clsCondicionDescuentoProveedorMdl(BaseModel):
    supplier = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE)
    product = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
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
        item['supplier'] = self.supplier.toJSON()
        item['product'] = self.product.toJSON()
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__(self):
        return self.supplier.supplier_name


''' Tablas catálogo de clientes '''
# Tabla de categoría de cliente
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

    def __str__ (self):
        return self.customer_cat
        
# Tabla de margén por categoría de cliente
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

# Tabla de zonas de cliente
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

    def toJSON(self):
        item = model_to_dict(self)
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__ (self):
        return self.customer_zone

# Tabla asesores comerciales
class clsAsesorComercialMdl(BaseModel):
    advisor = models.CharField('Asesor comercial', max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuario')
    zone = models.ForeignKey(clsZonaClienteMdl, on_delete=models.CASCADE, verbose_name='Zona')
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

# Tabla de catálogo de clientes
class clsCatalogoClientesMdl(BaseModel):
    qr_code = models.ImageField(upload_to = 'qr_codes/customers/%Y/%m/%d', blank=True)
    person_type = models.CharField('Tipo de persona', max_length=200, choices=PERSON_TYPE, blank=True, null=True)
    id_type = models.CharField('Tipo de identificación', max_length=200, choices=ID_TYPE)
    identification = models.PositiveBigIntegerField('Identificación', unique=True)
    business_name = models.CharField('Nombre del cliente', max_length=200)
    contact_name = models.CharField('Nombre del contacto', max_length=200, blank=True, null=True)
    cel_number = models.PositiveBigIntegerField('Celular')
    email = models.EmailField('Correo electrónico', max_length=200, blank=True, null=True)
    department = models.ForeignKey(clsDepartamentosMdl, on_delete=models.CASCADE)
    city = models.ForeignKey(clsCiudadesMdl, on_delete=models.CASCADE)
    customer_zone = models.ForeignKey(clsZonaClienteMdl, on_delete=models.CASCADE)
    delivery_address = models.CharField('Dirección entrega', max_length=200)
    del_schedule_init = models.CharField('Horario de entrega inicial', max_length=200, blank=True, null=True)
    del_schedule_end = models.CharField('Horario de entrega final', max_length=200, blank=True, null=True)
    customer_cat = models.ForeignKey(clsCategoriaClienteMdl, on_delete=models.CASCADE)
    commercial_advisor = models.ForeignKey(clsAsesorComercialMdl, on_delete=models.CASCADE)
    pay_method = models.CharField('Metodo de pago', max_length=200, choices=PAYMETHOD)
    credit_days = models.PositiveSmallIntegerField('Días de crédito', blank=True, null=True)
    credit_value = models.DecimalField('Cupo crédito', max_digits=10, decimal_places=2, default=0, blank=True, null=True)
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
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        item['qr_code'] = self.get_qr_code()
        return item
    
    def __str__ (self):
        return self.business_name



''' Tabla catálogo de bodegas '''
# Tabla de catálogo de bodegas
class clsCatalogoBodegasMdl(BaseModel):
    qr_code = models.ImageField(upload_to = 'qr_codes/bodegas/%Y/%m/%d', blank=True)
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
        default_permissions = []
        
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
        qrcode_img = qrcode.make(self.id)
        canvas = Image.new('RGB', (290, 290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.id}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
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



''' Tablas para cargue de historico de movimientos '''
# Tabla de historico de pedidos
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

# Tabla de ordenes de compra
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

# Tabla de entradas de almacén
class clsHistoricoEntradasAlmacenMdl(models.Model):
    date_creation = models.DateTimeField('Fecha creación')
    doc_number = models.CharField('Nº Documento', max_length=200)
    identification = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unit_price = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField('Total', max_digits=10, decimal_places=2)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    crossing_doc = models.CharField('Documento cruce', max_length=200)
    condition = models.CharField('Condición', max_length=200, choices=INCOMECONDITION, blank=True, null=True)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Entrada de almacén'
        verbose_name_plural = 'Entradas de almacén'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.identification.supplier_name

# Tabla de salidas de almacén
class clsHistoricoSalidasAlmacenMdl(models.Model):
    date_creation = models.DateTimeField('Fecha creación')
    doc_number = models.CharField('Nº Documento', max_length=200)
    identification = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unit_price = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField('Total', max_digits=10, decimal_places=2)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    crossing_doc = models.CharField('Documento cruce', max_length=200)
    condition = models.CharField('Condición', max_length=200, choices=WAREHOUSEEXIT, blank=True, null=True)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Salida de almacén'
        verbose_name_plural = 'Salidas de almacén'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.identification.business_name

# Tabla de ajustes de inventario
class clsHistoricoAjustesInventarioMdl(models.Model):
    date_creation = models.DateTimeField('Fecha creación')
    doc_number = models.CharField('Nº Documento', max_length=200)
    type = models.CharField('Tipo de movimiento', max_length=200, choices=INCOMETYPE)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    total_cost = models.DecimalField('Total costo', max_digits=10, decimal_places=2)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Ajuste inventario'
        verbose_name_plural = 'Ajustes de inventario'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.doc_number

# Tabla de devoluciones de cliente
class clsHistoricoDevolucionesClienteMdl(models.Model):
    date_creation = models.DateTimeField('Fecha creación')
    doc_number = models.CharField('Nº Documento', max_length=200)
    identification = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    crossing_doc = models.CharField('Documento cruce', max_length=200)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Devolución cliente'
        verbose_name_plural = 'Devoluciones clientes'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.identification.business_name

# Tabla de devoluciones a proveedor
class clsHistoricoDevolucionesProveedorMdl(models.Model):
    date_creation = models.DateTimeField('Fecha creación')
    doc_number = models.CharField('Nº Documento', max_length=200)
    identification = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    crossing_doc = models.CharField('Documento cruce', max_length=200)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Devolución proveedor'
        verbose_name_plural = 'Devoluciones proveedores'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.identification.supplier_name

# Tabla de obsequios
class clsHistoricoObsequiosMdl(models.Model):
    date_creation = models.DateTimeField('Fecha creación')
    doc_number = models.CharField('Nº Documento', max_length=200)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    total_cost = models.DecimalField('Total costo', max_digits=10, decimal_places=2)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Obsequio'
        verbose_name_plural = 'Obsequios'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.doc_number

# Tabla de traslados entre bodegas
class clsHistoricoTrasladosBodegasMdl(models.Model):
    date_creation = models.DateTimeField('Fecha creación')
    doc_number = models.CharField('Nº Documento', max_length=200)
    type = models.CharField('Tipo de movimiento', max_length=200, choices=INCOMETYPE)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    total_cost = models.DecimalField('Total costo', max_digits=10, decimal_places=2)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Traslado bodega'
        verbose_name_plural = 'Traslados bodegas'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.doc_number

# Tabla de saldo inicial
class clsHistoricoSaldoInicialMdl(models.Model):
    date_creation = models.DateTimeField('Fecha creación')
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    balance = models.PositiveSmallIntegerField('Cantidad')
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateTimeField('Fecha vencimiento')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Saldo inicial'
        verbose_name_plural = 'Saldos iniciales'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.product_code.product_desc

# Tabla de historico alterno de movimientos
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
        default_permissions = []

    def __str__(self):
        return self.doc_number

''' Tabla ajustes de inventario'''
# Tabla de ajustes de inventario
class clsAjusteInventarioMdl(BaseModel):
    doc_number = models.CharField('Nº Documento', max_length=200, blank=True, null=True)
    total_cost = models.DecimalField('Total costo', max_digits=10, decimal_places=2)
    condition = models.CharField('Condición', max_length=200, choices=INCOMECONDITION, default='CE')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Ajuste inventario'
        verbose_name_plural = 'Ajustes de inventario'
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
        super(clsAjusteInventarioMdl, self).save()

    def __str__(self):
        return str(self.id)

# Tabla de ajustes de inventario
class clsDetalleAjusteInventarioMdl(models.Model):
    doc_number = models.ForeignKey(clsAjusteInventarioMdl, on_delete=models.CASCADE)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    type = models.CharField('Tipo de ajuste', max_length=200, choices=INCOMETYPE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    batch = models.CharField('Lote', max_length=200)
    expiration_date = models.DateField('Fecha vencimiento')
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unitary_cost = models.DecimalField('Costo unitario', max_digits=10, decimal_places=2, blank=True, null=True)
    total_cost = models.DecimalField('Total costo', max_digits=10, decimal_places=2)
    
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Ajuste inventario'
        verbose_name_plural = 'Ajustes de inventario'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return str(self.id)



''' Tablas para historico de movimientos'''
# Tabla de entradas de almacén
class clsEntradasAlmacenMdl(BaseModel):
    doc_number = models.CharField('Nº Documento', max_length=200, blank=True, null=True)
    identification = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE)
    total_cost = models.DecimalField('Costo total', max_digits=10, decimal_places=2)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    crossing_doc = models.CharField('Documento cruce', max_length=200)
    condition = models.CharField('Condición', max_length=200, choices=INCOMECONDITION)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Entrada de almacén'
        verbose_name_plural = 'Entradas de almacén'
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
        super(clsEntradasAlmacenMdl, self).save()

    def __str__(self):
        return str(self.id)

# Tabla detalle de entradas de almacén
class clsTblDetalleEntradaAlmacen(models.Model):
    doc_number = models.ForeignKey(clsEntradasAlmacenMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad')
    unitary_cost = models.DecimalField('Costo unitario', max_digits=10, decimal_places=2)
    total_cost = models.DecimalField('Costo total', max_digits=10, decimal_places=2)
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

# Tabla de devoluciones de cliente
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

# Tabla detalle de devoluciones de cliente
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

# Tabla de devoluciones a proveedor
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

# Tabla detalle de devolución de proveedor
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

# Tabla de salidas de almacén
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
        default_permissions = []

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

# Tabla detalle de devolución de proveedor
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

# Tabla de obsequios
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

# Tabla detalle de obsequios
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

# Tabla de traslados entre bodegas
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

# Tabla detalle de obsequios
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

# Tabla de saldos de inventario
class clsSaldosInventarioMdl(models.Model):
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    # product_code = models.SmallIntegerField('codigo producto')
    batch = models.CharField('Lote', max_length=200)
    inventory_avail = models.PositiveSmallIntegerField('Saldo disponible')
    expiration_date = models.CharField('Fecha vencimiento', max_length=200)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    # store = models.SmallIntegerField('bodega')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Saldo inventario'
        verbose_name_plural = 'Saldos inventarios'
        ordering = ['id']
        default_permissions = []

    def __str__(self):
        return self.product_code.product_desc

# Tabla de historico real de movimientos
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
    pre_bal = models.PositiveSmallIntegerField('Presaldo')
    balance = models.PositiveSmallIntegerField('Saldo')
    inv_value = models.DecimalField('Costo total', max_digits=10, decimal_places=2)
    store = models.ForeignKey(clsCatalogoBodegasMdl, on_delete=models.CASCADE)
    # identification = models.PositiveBigIntegerField('Identificación')
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


''' Señales post-save para agregar numero de documento a tablas transaccionales'''
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
    

post_save.connect(fncGenerarNumeroDocumento, sender=clsAjusteInventarioMdl)
post_save.connect(fncGenerarNumeroDocumento, sender=clsEntradasAlmacenMdl)
post_save.connect(fncGenerarNumeroDocumento, sender=clsDevolucionesClienteMdl)
post_save.connect(fncGenerarNumeroDocumento, sender=clsDevolucionesProveedorMdl)
post_save.connect(fncGenerarNumeroDocumento, sender=clsSalidasAlmacenMdl)
post_save.connect(fncGenerarNumeroDocumento, sender=clsObsequiosMdl)
post_save.connect(fncGenerarNumeroDocumento, sender=clsTrasladosBodegasMdl)
