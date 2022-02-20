from datetime import datetime, date
from crum import get_current_user

from django.db import models
from django.db.models import Model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import model_to_dict

from apps.models import BaseModel
from apps.choices import *
from apps.modulo_configuracion.models import *
from apps.modulo_compras.models import *
from apps.modulo_comercial.models import *


'''Tabla entradas de almacén'''
class WarehouseRevenue(BaseModel):
    supplier = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE, verbose_name='Proveedor')
    crossing_doc = models.CharField('Documento de cruce', max_length=200)
    documentation = models.BooleanField('Documentaciòn', default=False)
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField('Iva', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0.00)
    observations = models.TextField('Observaciones', blank=True, null=True)
    state = models.CharField('Estado', max_length=200, choices=WAREHOUSEENTRY, default='CA')

    class Meta:
        verbose_name = 'Entrada de almacèn'
        verbose_name_plural = 'Entradas de almacén'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_log_revenue_warehouse', 'Entradas de almacén'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(WarehouseRevenue, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['supplier'] = self.supplier.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['discount'] = format(self.discount, '.2f')
        item['total'] = format(self.total, '.2f')
        return item

    def __str__(self):
        return self.supplier.supplier_name

# Tabla detalle entradas de almacén
class WarehouseRevenueDetail(BaseModel):
    warehouse_entry = models.ForeignKey(WarehouseRevenue, on_delete=models.CASCADE, verbose_name='Entrada de almacén')
    #store = models.ForeignKey(WarehouseCatalogue, on_delete=models.CASCADE, verbose_name='Bodega')
    product = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad recibida', default=0)
    unit_price = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField('Precio total', max_digits=10, decimal_places=2, default=0.00)
    #store = models.ForeignKey(WarehouseCatalogue, on_delete=models.CASCADE, verbose_name='Bodega')
    batch_record = models.CharField('Lote', max_length=200)
    expiration_date = models.DateField('Fecha de vencimiento', default=datetime.now)
    prod_observations = models.TextField('Observaciones', blank=True, null=True)
    state = models.CharField('Estado', max_length=200, choices=WAREHOUSEENTRY, default='CA')

    class Meta:
        verbose_name = 'Detalle entrada de almacén'
        verbose_name_plural = 'Detalle entradas de almacén'
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
        super(WarehouseRevenue, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['product'] = self.product.toJSON()
        item['store'] = self.store.toJSON()
        item['unit_price'] = format(self.unit_price, '.2f')
        item['discount'] = format(self.discount, '.2f')
        item['total_price'] = format(self.total_price, '.2f')
        item['expiration_date'] = self.expiration_date.strftime('%Y-%m-%d')
        return item

    def __str__(self):
        return self.product.product_desc

'''Tablas salidas de almacén'''
class WarehouseOutFlows(BaseModel):
    customer = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE, verbose_name='Cliente')
    crossing_doc = models.CharField('Documento de cruce', max_length=200)
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField('Iva', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0.00)
    observations = models.TextField('Observaciones', blank=True, null=True)
    state = models.CharField('Estado', max_length=200, choices=WAREHOUSEEXIT, default='CE')
    
    class Meta:
        verbose_name = 'Salida de almacén'
        verbose_name_plural = 'Salidas de almacén'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_log_outflows_warehouse', 'Salidas de almacén'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(WarehouseOutFlows, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['customer'] = self.customer.toJSON()
        return item

    def __str__(self):
        return self.customer.business_name

# Tabla detalle de salidas de almacén por producto
class WarehouseOutFlowsDetail(BaseModel):
    warehouse_exit = models.ForeignKey(WarehouseOutFlows, on_delete=models.CASCADE, verbose_name='Salida')
    #store = models.ForeignKey(WarehouseCatalogue, on_delete=models.CASCADE, verbose_name='Bodega')
    product = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('Cantidad', default=0)
    unit_price = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField('Precio total', max_digits=10, decimal_places=2, default=0.00)
    batch_record = models.CharField('Lote', max_length=200,)
    expiration_date = models.DateField('Fecha de vencimiento', default=datetime.now)
    state = models.CharField('Estado', max_length=200, choices=WAREHOUSEEXIT, default='CE')

    class Meta:
        verbose_name = 'Detalle salida de almacén'
        verbose_name_plural = 'Detalle salidas de almacén'
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
        super(WarehouseOutFlowsDetail, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['store'] = self.store.toJSON()
        item['product'] = self.product.toJSON()
        item['unit_price'] = format(self.unit_price, '.2f')
        item['discount'] = format(self.discount, '.2f')
        item['total_price'] = format(self.total_price, '.2f')
        item['expiration_date'] = self.expiration_date.strftime('%Y-%m-%d')
        return item

    def __str__(self):
        return self.product.product_desc    




# Revisar------------------------------------
'''Tablas de conteo de inventario'''
class InventoryCount(BaseModel):
    inventory_type = models.CharField('Tipo de inventario', choices=INVENTORYTYPE, default='AL', max_length=200)
    #warehouse = models.ForeignKey(WarehouseCatalogue, on_delete=models.CASCADE, verbose_name='Bodega')
    real_quantity = models.PositiveSmallIntegerField('Cantidad recibida', default=0, blank=True, null=True)

    class Meta:
        verbose_name = 'Conteo de inventario'
        verbose_name_plural = 'Conteos de inventario'
        ordering = ['id']

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(InventoryCount, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['warehouse'] = self.warehouse.toJSON()
        return item

    def __str__(self):
        return self.inventory_type

# Tabla detalle de conteo de inventario
class InventoryCountDetail(BaseModel):
    inventory_count = models.ForeignKey(InventoryCount, on_delete=models.CASCADE, verbose_name='Conteo de inventario')
    product = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    first_count = models.PositiveSmallIntegerField('Conteo 1', blank=True, null=True)
    second_count = models.PositiveSmallIntegerField('Conteo 2', blank=True, null=True)
    third_count = models.PositiveSmallIntegerField('Conteo 3', blank=True, null=True)
    difference = models.PositiveSmallIntegerField('Diferencia', blank=True, null=True)

    class Meta:
        verbose_name = 'Detalle conteo de inventario'
        verbose_name_plural = 'Detalle conteos de inventario'
        ordering = ['id']

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(InventoryCountDetail, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['inventory_count'] = self.inventory_count.toJSON()
        item['product'] = self.product.toJSON()
        return item

    def __str__(self):
        return self.inventory_count.inventory_type


'''Tabla de inventario'''
class Inventory(BaseModel):
    product = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    previous_balance = models.PositiveSmallIntegerField('Saldo anterior', blank=True, null=True)
    warehouse_entry = models.ForeignKey(WarehouseRevenue, on_delete=models.CASCADE, verbose_name='Entrada')
    warehouse_exit = models.ForeignKey(WarehouseOutFlows, on_delete=models.CASCADE, verbose_name='Salida')
    inventory_balance = models.PositiveSmallIntegerField('Saldo de inventario', blank=True, null=True)
    inventory_count = models.ForeignKey(InventoryCount, on_delete=models.CASCADE)
    difference = models.PositiveSmallIntegerField('Diferencia en conteo', blank=True, null=True)
    final_balance = models.PositiveSmallIntegerField('Saldo final', blank=True, null=True)
    indice_rotacion = models.CharField('Indice de rotación de inventario', max_length=200)

    class Meta:
        verbose_name = 'Inventario de producto'
        verbose_name_plural = 'Inventario de productos'
        ordering = ['id']

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(Inventory, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['product'] = self.product.toJSON()
        item['warehouse_entry'] = self.warehouse_entry.toJSON()
        item['warehouse_exit'] = self.warehouse_exit.toJSON()
        item['inventory_count'] = self.inventory_count.toJSON()
        return item

    def __str__(self):
        return self.product.name




'''




class PackingPedidos(Model):
    ESTADO = (
        ('VI', 'Vigente'),
        ('NV', 'No vigente'),
    )
    fecha_creacion = models.DateField('Fecha de creación', auto_now_add = True)
    fecha_picking = models.DateField('Fecha de picking')
    cod_producto = models.ForeignKey(CatalogoProductos, on_delete=models.CASCADE)
    cod_unidad_almacenamiento = models.ForeignKey(UnidadAlmacenamiento, on_delete=models.CASCADE)
    cantidad_total = models.IntegerField('Cantidad total producto')
    estado_packing = models.CharField('Estado packing', max_length=200, choices=ESTADO)
    usuario_creacion = models.CharField('Usuario de creación', max_length=200) #'se debe relacionar al campo nombre de usuario de la tabla Usuarios formulada en la vista con el usuario que este loguiado'
    fecha_modificacion = models.DateField('Fecha de modificación', auto_now = True, auto_now_add = False)
    usuario_modificacion = models.CharField('Usuario de modificación', max_length=200) #'se debe relacionar al campo nombre de usuario de la tabla Usuarios formulada en la vista con el usuario que este loguiado'    

    class Meta:
        verbose_name= 'Packing pedido'
        verbose_name_plural= 'Packing pedidos'
        ordering = ['fecha_creacion']

    def __str__ (self):
        return self.cod_producto

#Instancia para ruta de entregas
class RutaEntregas(Model):
    ESTADO = (
        ('AC', 'Activo'),
        ('IN', 'Inactivo'),
    )
    cod_entrega = models.AutoField('Código de entrega', primary_key = True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now_add = True)
    fecha_entrega = models.DateField('Fecha de entrega') #usuario formulario
    vehiculos = models.ForeignKey(CatalogoVehiculos, on_delete=models.CASCADE)
    cod_cliente = models.ForeignKey(ClientsCatalog, on_delete=models.CASCADE)
    cod_actividad = models.ForeignKey(Actividades, on_delete=models.CASCADE)
    cod_pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField('Fecha inicio entrega') # 
    fecha_fin = models.DateTimeField('Fecha fin entrega') #
    tiempo_entrega = models.DurationField('Tiempo de entrega') #'calcular de acuerdo a hora inicio y hora fin'
    observaciones = models.CharField('Observaciones', max_length=200) 
    estado_entrega = models.CharField('Estado de bodega', max_length=200, choices=ESTADO) #calculado
    usuario_creacion = models.CharField('Usuario de creación', max_length=200) #'se debe relacionar al campo nombre de usuario de la tabla Usuarios formulada en la vista con el usuario que este loguiado'
    fecha_modificacion = models.DateField('Fecha de modificación', auto_now = True, auto_now_add = False)
    usuario_modificacion = models.CharField('Usuario de modificación', max_length=200) #'se debe relacionar al campo nombre de usuario de la tabla Usuarios formulada en la vista con el usuario que este loguiado'

    class Meta:
        verbose_name= 'Ruta de entrega'
        verbose_name_plural= 'Ruta de entregas'
        ordering = ['fecha_entrega']

    def __str__ (self):
        return self.cod_entrega
class InventoryRotation(BaseModel):
    warehouse_catalog = models.ForeignKey(WarehouseCatalog, on_delete=models.CASCADE, verbose_name='Bodega')

'''

