from datetime import datetime, date
from crum import get_current_user
from pandas import pandas as pd
from django_pandas.io import read_frame

from django.db import models
from django.db.models import Model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import model_to_dict

from apps.models import BaseModel
from apps.choices import *
from apps.modulo_configuracion.models import *


''' Tablas pedidos '''
class Orders(BaseModel):
    doc_number = models.CharField('Documento Nº', max_length=200, blank=True, null=True)
    identification = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    order_date = models.DateField('Fecha de pedido', default=datetime.now)
    payment_method = models.CharField('Método de pago', max_length=200, choices=PAYMETHOD, default='CO')
    delivery_date = models.DateField('Fecha de entrega', default=datetime.now)
    delivery_address = models.CharField('Dirección de entrega', max_length=200)
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField('Iva', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0.00)
    observations = models.TextField('Observaciones', blank=True, null=True)
    state = models.CharField('Estado', max_length=200, choices=STATEORDER, default='AB')
    objects = DataFrameManager()
    
    class Meta:
        verbose_name = 'Pedido cliente'
        verbose_name_plural = 'Pedidos clientes'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_com_order', 'Pedidos'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(Orders, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['identification'] = self.identification.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['dcto'] = format(self.discount, '.2f')
        item['total'] = format(self.total, '.2f')
        item['order_date'] = self.order_date.strftime('%Y-%m-%d')
        item['delivery_date'] = self.order_date.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.ordersdetail_set.all()]
        return item
    
    def __str__(self):
        return self.identification.business_name

# Tabla detalle de productos por pedido
class OrdersDetail(BaseModel):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Pedido')
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE, verbose_name='Producto')
    #store = models.ForeignKey(WarehouseCatalogue, on_delete=models.CASCADE, verbose_name='Bodega')
    quantity = models.PositiveSmallIntegerField('Cantidad', default=0)
    unit_price = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField('Iva', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0.00)
    state = models.CharField('Estado', max_length=200, choices=STATEORDER, default='AB')

    class Meta:
        verbose_name = 'Detalle pedido'
        verbose_name_plural = 'Detalle pedidos'
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
        super(OrdersDetail, self).save()

    def toJSON(self):
        item = model_to_dict(self, exclude=['order'])
        item['product_code'] = self.product.toJSON()
        item['unit_price'] = format(self.sale_price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['discount'] = format(self.dcto, '.2f')
        item['total'] = format(self.total, '.2f')
        return item
    
    def __str__(self):
        return self.product_code.product_desc

# Tabla de ventas perdidas
class LostSales(BaseModel):
    order_date = models.DateField('Fecha de venta')
    customer = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE, verbose_name='Producto')
    quantity = models.PositiveSmallIntegerField('Cantidad')

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
        super(LostSales, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['date'] = self.date.strftime('%Y-%m-%d')
        item['customer'] = self.customer.toJSON()
        item['product_code'] = self.product_code.toJSON()
        return item
    
    def __str__(self):
        return self.customer.business_name

''' Tablas cotizaciones clientes '''
class Quotes(BaseModel):
    identification = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    quote_date = models.DateField('Fecha de cotización', default=datetime.now)
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField('Iva', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0.00)
    observations = models.TextField('Observaciones', blank=True, null=True)

    class Meta:
        verbose_name = 'Cotización cliente'
        verbose_name_plural = 'Cotizaciones clientes'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_com_quote', 'Cotizaciones'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(Quotes, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['identification'] = self.identification.toJSON()
        item['quote_date'] = self.quote_date.strftime('%Y-%m-%d')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['discount'] = format(self.discount, '.2f')
        item['total'] = format(self.total, '.2f')
        return item
    
    def __str__(self):
        return self.identification.business_name

# Tabla detalle de productos por cotización
class QuotesDetail(BaseModel):
    quote = models.ForeignKey(Quotes, on_delete=models.CASCADE, verbose_name='Cotización')
    product_code = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE, verbose_name='Producto')
    quantity = models.PositiveSmallIntegerField('Cantidad', default=0)
    lead_time = models.PositiveSmallIntegerField('Tiempo de entrega', default=0)
    unit_price = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField('Iva', max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('Total', max_digits=10, decimal_places=2, default=0.00)
    due_date = models.DateField('Fecha de vigencia', default=datetime.now)

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
        super(QuotesDetail, self).save()

    def toJSON(self):
        item = model_to_dict(self, exclude=['quotes'])
        item['product_code'] = self.product_code.toJSON()
        item['unit_price'] = format(self.unit_price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['discount'] = format(self.discount, '.2f')
        item['total'] = format(self.total, '.2f')
        item['due_date'] = self.due_date.strftime('%Y-%m-%d')
        return item
    
    def __str__(self):
        return self.product_code.product_desc

''' Tabla cartera clientes '''
class CustomerDebt(BaseModel):
    customer = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name='Pedido')
    order_value = models.DecimalField('Valor orden', max_digits=10, decimal_places=2, default=0)
    term = models.PositiveSmallIntegerField('Cuotas', default=0)
    next_payment_date = models.DateField('Fecha de próximo pago pedido', default=datetime.now)
    next_payment_value = models.DecimalField('Valor próximo pago pedido', max_digits=10, decimal_places=2, default=0)
    balance_payment = models.DecimalField('Saldo pendiente de pago', max_digits=10, decimal_places=2, default=0)
    credit_value = models.DecimalField('Valor crédito', max_digits=10, decimal_places=2, default=0)
    balance_credit_value = models.DecimalField('Saldo crédito', max_digits=10, decimal_places=2, default=0)
    state = models.CharField('Estado', max_length=200, choices=STATECARTERA, default='AC', blank=True, null=True)
    objects = DataFrameManager()

    class Meta:
        verbose_name = 'Cartera cliente'
        verbose_name_plural = 'Cartera clientes'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_com_cust_debt', 'Cartera clientes'),)

    
    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(CustomerDebt, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['customer'] = self.customer.toJSON()
        item['order'] = self.order.toJSON()
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        item['det_payments'] = [i.toJSON() for i in self.customerpayments_set.all()]
        return item

    def __str__(self):
        return self.customer.customer

''' Tabla pagos clientes '''
class CustomerPayments(BaseModel):
    cartera = models.ForeignKey(CustomerDebt, on_delete=models.CASCADE, verbose_name='Cartera')
    payment = models.DecimalField('Pago', max_digits=10, decimal_places=2, default=0.00)
    obs = models.TextField('Observaciones')

    class Meta:
        verbose_name = 'Pago cliente'
        verbose_name_plural = 'Pagos clientes'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_com_cust_pay', 'Pagos clientes'),)
    
    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(CustomerPayments, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['payment'] = format(self.payment, '.2f')
        return item

    def __str__(self):
        return self.customer.customer

''' Tabla agenda de llamadas '''
class ScheduleCall(BaseModel):
    customer = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    call_date = models.DateField('Fecha de llamada', default=datetime.now)
    start_call = models.DateTimeField('Hora inicio llamada')
    end_call = models.DateTimeField('Hora fin llamada')
    call_time = models.DurationField('Tiempo de llamada')
    obs = models.TextField('Observaciones')
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')

    class Meta:
        verbose_name= 'Agenda llamada'
        verbose_name_plural= 'Agenda llamadas'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_com_sch_call', 'Agenda de llamadas'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(ScheduleCall, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['customer'] = self.customer.toJSON()
        item['call_date'] = self.call_date.strftime('%Y-%m-%d')
        return item

    def __str__(self):
        return self.customer.customer

# Revisar------------------------------------------
''' Tabla ruta visitas '''
class VisitsRoute(BaseModel):
    customer = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE, verbose_name='Cliente')
    visit_date = models.DateField('Fecha de visita', default=datetime.now)
    start_time = models.CharField('Hora inicio visita', max_length=200)
    end_time = models.CharField('Hora fin visita', max_length=200)
    visit_time = models.CharField('Tiempo de visita',  max_length=200)
    observations = models.TextField('Observaciones visita')
    state = models.CharField('Estado', max_length=200, choices=STATE, default='AC')

    class Meta:
        verbose_name = 'Ruta de visita'
        verbose_name_plural = 'Ruta de visitas'
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
        super(VisitsRoute, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['customer'] = self.customer.toJSON()
        item['state'] = {'id': self.state, 'name': self.get_state_display()}
        return item
    
    def __str__(self):
        return self.customer.business_name


