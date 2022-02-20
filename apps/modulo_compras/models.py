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

''' Tablas ordenes de compra '''
class OrderPurchase(BaseModel):
    identification = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE, verbose_name='Proveedor')
    order_date = models.DateField('Fecha de orden', default=datetime.now)
    pay_method = models.CharField('Método de pago', max_length=200, choices=PAYMETHOD, default='CO')
    delivery_date = models.DateField('Fecha de entrega', default=datetime.now)
    delivery_address = models.CharField('Dirección de entrega', max_length=200)
    observations = models.TextField('Observaciones', blank=True, null=True)
    urgency_level = models.CharField('Nivel de urgencia', max_length=200, choices=URGENCYLEVEL, default='AL')
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField('Iva', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0.00)
    state = models.CharField('Estado', max_length=200, choices=STATEORDER, default='AB')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Orden de compra'
        verbose_name_plural = 'Ordenes de compra'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_pur_order_pur', 'Ordenes de compra'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(OrderPurchase, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['discount'] = format(self.discount, '.2f')
        item['total'] = format(self.total, '.2f')
        item['order_date'] = self.order_date.strftime('%Y-%m-%d')
        item['deliver_date'] = self.order_date.strftime('%Y-%m-%d')
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        item['orders_detail'] = [ i for i in self.orderspurchasedetail_set.all() ]
        return item
    
    def __str__(self):
        return self.identification.supplier_name

# Tabla detalle de productos por orden de compra
class OrderPurchaseDetail(BaseModel):
    order_purchase = models.ForeignKey(OrderPurchase, on_delete=models.CASCADE, verbose_name='Orden de compra')
    product = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE)
    cant = models.PositiveSmallIntegerField('Cantidad', default=0)
    unit_price = models.DecimalField('Precio de compra', max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField('Iva', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0.00)
    #store = models.ForeignKey(WarehouseCatalogue, on_delete=models.CASCADE)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Detalle orden de compra'
        verbose_name_plural = 'Detalle ordenes de compra'
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
        super(OrderPurchaseDetail, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['order_purchase'] = self.order_purchase.toJSON()
        item['product'] = self.product.toJSON()
        item['unit_price'] = format(self.unit_price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['discount'] = format(self.discount, '.2f')
        item['total_price'] = format(self.total_price, '.2f')
        return item
    
    def __str__(self):
        return self.product.product_desc

# Mismo modelo
''' Tablas cotizaciones proveedor '''
class SupplierQuote(BaseModel):
    identification = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE, verbose_name='Proveedor')
    quote_date = models.DateField('Fecha de cotización', default=datetime.now)
    lead_time = models.PositiveIntegerField('Tiempo entrega', blank=True, null=True)
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField('Iva', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0.00)
    observations = models.TextField('Observaciones')
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Cotización proveedor'
        verbose_name_plural = 'Cotizaciones proveedores'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_pur_quote_pur', 'Cotizaciónes'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(SupplierQuote, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['supplier'] = self.supplier.toJSON()
        item['quote_date'] = self.quote_date.strftime('%Y-%m-%d')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['discount'] = format(self.discount, '.2f')
        item['total'] = format(self.total, '.2f')
        return item
    
    def __str__(self):
        return self.supplier.supplier_name

# Tabla detalle de productos por cotización
class SupplierQuoteDetail(BaseModel):
    supplier_quote = models.ForeignKey(SupplierQuote, on_delete=models.CASCADE, verbose_name='Cotización')
    product = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE, verbose_name='Producto')
    quantity = models.PositiveSmallIntegerField('Cantidad', default=0)
    unit_price = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField('Iva', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField('Precio total', max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Detalle cotización'
        verbose_name_plural = 'Detalle cotizaciones'
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
        super(SupplierQuoteDetail, self).save()

    def toJSON(self):
        item = model_to_dict(self, exclude=['quotes'])
        item['supplier_quote'] = self.supplier_quote.toJSON()
        item['product'] = self.product.toJSON()
        item['unit_price'] = format(self.unit_price, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['discount'] = format(self.discount, '.2f')
        item['total_price'] = format(self.total_price, '.2f')
        return item
    
    def __str__(self):
        return self.product.product_desc

'''Tabla gestión y evaluación de proveedores'''
class EvaluationSuppliers(BaseModel):
    supplier = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE, verbose_name='Proveedor')
    evaluation_type = models.CharField('Tipo de evaluación', max_length=200, choices=EVALUATIONTYPE, default='CT')
    buyer = models.CharField('Comprador', max_length=200)
    general_score = models.DecimalField('Puntaje', max_digits=4, decimal_places=2)
    deliver_score = models.DecimalField('Puntaje cumplimiento entregas', max_digits=4, decimal_places=2)
    quantity_score = models.DecimalField('Puntaje cumplimiento cantidades', max_digits=4, decimal_places=2)
    quality_score = models.DecimalField('Puntaje cumplimiento calidad', max_digits=4, decimal_places=2)
    products_score = models.DecimalField('Puntaje Cumplimiento en productos', max_digits=4, decimal_places=2)
    price_score = models.DecimalField('Puntaje Cumplimiento en precio', max_digits=4, decimal_places=2)
    pay_score = models.DecimalField('Puntaje Cumplimiento en forma de pago', max_digits=4, decimal_places=2)
    demand_score = models.DecimalField('Puntaje Cumplimiento en flexibilidad de la demanda', max_digits=4, decimal_places=2)
    doc_score = models.DecimalField('Puntaje Cumplimiento en documentación', max_digits=4, decimal_places=2)
    obs = models.TextField('Observaciones')
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')

    class Meta:
        verbose_name = 'Gestión y evaluación proveedor'
        verbose_name_plural = 'Gestión y evaluación proveedores'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_pur_sup_eva', 'Evaluación proveedores'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(EvaluationSuppliers, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['supplier'] = self.supplier.toJSON()
        item['evaluation_type'] = {'id': self.evaluation_type, 'name': self.get_evaluation_type_display()}
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__(self):
        return self.supplier.name

''' Tabla cartera proveedores '''
class SupplierDebt(BaseModel):
    supplier = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE, verbose_name='Proveedor')
    order_purchase = models.ForeignKey(OrderPurchase, on_delete=models.CASCADE, verbose_name='Orden de compra')
    order_value = models.DecimalField('Valor orden de compra', max_digits=10, decimal_places=2)
    term = models.PositiveSmallIntegerField('Plazo')
    next_payment_date = models.DateField('Fecha de próximo pago orden')
    next_payment_value = models.DecimalField('Valor próximo pago orden', max_digits=10, decimal_places=2)
    balance_payment = models.DecimalField('Saldo pendiente de pago', max_digits=10, decimal_places=2)
    credit_value = models.DecimalField('Valor crédito', max_digits=10, decimal_places=2)
    balance_credit_value = models.DecimalField('Saldo crédito', max_digits=10, decimal_places=2)
    state = models.CharField('Estado', max_length=200, choices=STATECARTERA, default='AC', blank=True, null=True)
    objects = DataFrameManager()
    
    class Meta:
        verbose_name = 'Cartera proveedor'
        verbose_name_plural = 'Cartera proveedores'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_pur_sup_deb', 'Cartera proveedores'),)
        

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(SupplierDebt, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['supplier'] = self.supplier.toJSON()
        item['order_purchase'] = self.order_purchase.toJSON()
        item['order_value'] = format(self.order_value, '.2f')
        item['next_payment_date'] = self.next_payment_date.strftime('%Y-%m-%d')
        item['next_payment_value'] = format(self.order_value, '.2f')
        item['balance_payment'] = format(self.balance_payment, '.2f')
        item['credit_value'] = format(self.credit_value, '.2f')
        item['balance_credit_value'] = format(self.balance_credit_value, '.2f')
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item

    def __str__(self):
        return self.supplier.supplier_name

''' Tabla pagos proveedores '''
class SuppliersPayments(BaseModel):
    cartera = models.ForeignKey(SupplierDebt, on_delete=models.CASCADE, verbose_name='Cartera')
    payment = models.DecimalField('Pago', max_digits=10, decimal_places=2, default=0.00)
    obs = models.TextField('Observaciones')

    class Meta:
        verbose_name = 'Pago cliente'
        verbose_name_plural = 'Pagos clientes'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_pur_sup_pay', 'Pagos proveedores'),)
    
    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(SuppliersPayments, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['cartera'] = self.cartera.toJSON()
        item['payment'] = format(self.payment, '.2f')
        return item

    def __str__(self):
        return self.customer.customer

''' Tabla entregas incumplidas '''
class EntregasIncumplidas(BaseModel):
    supplier = models.ForeignKey(clsCatalogoProveedoresMdl, on_delete=models.CASCADE, verbose_name='Proveedor')
    order_purchase = models.ForeignKey(OrderPurchase, on_delete=models.CASCADE, verbose_name='Orden de compra')
    order_value = models.DecimalField('Valor orden de compra', max_digits=10, decimal_places=2)
    days = models.PositiveSmallIntegerField('Días atraso')

    class Meta:
        verbose_name = 'Entrega incumplida'
        verbose_name_plural = 'Entregas incumplidas'
        ordering = ['id']

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(EntregasIncumplidas, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['supplier'] = self.supplier.toJSON()
        item['order_purchase'] = self.order_purchase.toJSON()
        item['order_value'] = format(self.order_value, '.2f')
        return item

    def __str__(self):
        return self.supplier.name
