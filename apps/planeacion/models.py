from django.db import models
from apps.modulo_configuracion.models import *

''' Tablas planificación comercial'''
# Tabla planificación comercial
class CommercialPlanning(BaseModel):
    measurement_date = models.DateTimeField(auto_now_add=True)
    monetary_goal = models.DecimalField('Meta monetaria', max_digits=10, decimal_places=2)
    real = models.DecimalField('Real', max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment = models.DecimalField('Cumplimiento', max_digits=10, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Planificación comercial'
        verbose_name_plural= 'Planificaciones comerciales'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_adm_commercial_plan', 'Planificación comercial'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(CommercialPlanning, self).save()
    
    def toJSON(self):
        item = model_to_dict(self)
        item['monetary_goal'] = format(self.monetary_goal, '.2f')
        item['real'] = format(self.monetary_goal, '.2f')
        item['fulfillment'] = format(self.monetary_goal, '.2f')
        
    def __str__ (self):
        return self.measurement_date

# Tabla planeación comercial por indicador
class CommercialPlanningIndicators(BaseModel):
    planning = models.ForeignKey(CommercialPlanning, on_delete=models.CASCADE)
    indicator_name = models.CharField('Nombre indicador', max_length=200)
    monetary_goal = models.DecimalField('Meta monetaria', max_digits=10, decimal_places=2)
    real = models.DecimalField('Real', max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment = models.DecimalField('Cumplimiento', max_digits=10, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    def toJSON(self):
        item = model_to_dict(self)
        item['planning'] = self.planning.toJSON()
        item['monetary_goal'] = format(self.monetary_goal, '.2f')
        item['real'] = format(self.monetary_goal, '.2f')
        item['fulfillment'] = format(self.monetary_goal, '.2f')
        return item

    def __str__ (self):
        return self.indicator_name

# Tabla planeación comercial por ciudad
class CommercialPlanningCity(BaseModel):
    planning = models.ForeignKey(CommercialPlanning, on_delete=models.CASCADE)
    city = models.ForeignKey(clsCiudadesMdl, on_delete=models.CASCADE)
    monetary_goal = models.DecimalField('Meta monetaria', max_digits=10, decimal_places=2)
    real = models.DecimalField('Real', max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment = models.DecimalField('Cumplimiento', max_digits=10, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    def toJSON(self):
        item = model_to_dict(self)
        item['planning'] = self.planning.toJSON()
        item['city'] = self.city.toJSON()
        item['monetary_goal'] = format(self.monetary_goal, '.2f')
        item['real'] = format(self.monetary_goal, '.2f')
        item['fulfillment'] = format(self.monetary_goal, '.2f')
        return item

    def __str__ (self):
        return self.city.city_name

# Tabla planeación comercial por zona
class CommercialPlanningZone(BaseModel):
    planning = models.ForeignKey(CommercialPlanning, on_delete=models.CASCADE)
    customer_zone = models.ForeignKey(clsZonaClienteMdl, on_delete=models.CASCADE)
    monetary_goal = models.DecimalField('Meta monetaria', max_digits=10, decimal_places=2)
    real = models.DecimalField('Real', max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment = models.DecimalField('Cumplimiento', max_digits=10, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    def toJSON(self):
        item = model_to_dict(self)
        item['planning'] = self.planning.toJSON()
        item['customer_zone'] = self.customer_zone.toJSON()
        item['monetary_goal'] = format(self.monetary_goal, '.2f')
        item['real'] = format(self.monetary_goal, '.2f')
        item['fulfillment'] = format(self.monetary_goal, '.2f')
        return item

    def __str__ (self):
        return self.customer_zone.customer_zone

# Tabla planeación comercial por asesor
class CommercialPlanningAdvisor(BaseModel):
    planning = models.ForeignKey(CommercialPlanning, on_delete=models.CASCADE)
    commercial_advisor = models.ForeignKey(clsAsesorComercialMdl, on_delete=models.CASCADE)
    monetary_goal = models.DecimalField('Meta monetaria', max_digits=10, decimal_places=2)
    real = models.DecimalField('Real', max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment = models.DecimalField('Cumplimiento', max_digits=10, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    def toJSON(self):
        item = model_to_dict(self)
        item['planning'] = self.planning.toJSON()
        item['commercial_advisor'] = self.commercial_advisor.toJSON()
        item['monetary_goal'] = format(self.monetary_goal, '.2f')
        item['real'] = format(self.monetary_goal, '.2f')
        item['fulfillment'] = format(self.monetary_goal, '.2f')
        return item

    def __str__ (self):
        return self.commercial_advisor.advisor

# Tabla planeación comercial por categoría cliente
class CommercialPlanningclsCategoriaClienteMdl(BaseModel):
    planning = models.ForeignKey(CommercialPlanning, on_delete=models.CASCADE)
    customer_cat = models.ForeignKey(clsCategoriaClienteMdl, on_delete=models.CASCADE)
    monetary_goal = models.DecimalField('Meta monetaria', max_digits=10, decimal_places=2)
    real = models.DecimalField('Real', max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment = models.DecimalField('Cumplimiento', max_digits=10, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    def toJSON(self):
        item = model_to_dict(self)
        item['planning'] = self.planning.toJSON()
        item['customer_cat'] = self.customer_cat.toJSON()
        item['monetary_goal'] = format(self.monetary_goal, '.2f')
        item['real'] = format(self.monetary_goal, '.2f')
        item['fulfillment'] = format(self.monetary_goal, '.2f')
        return item

    def __str__ (self):
        return self.customer_cat.customer_cat

# Tabla planeación comercial por cliente
class CommercialPlanningCustomer(BaseModel):
    planning = models.ForeignKey(CommercialPlanning, on_delete=models.CASCADE)
    customer = models.ForeignKey(clsCatalogoClientesMdl, on_delete=models.CASCADE)
    monetary_goal = models.DecimalField('Meta monetaria', max_digits=10, decimal_places=2)
    real = models.DecimalField('Real', max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment = models.DecimalField('Cumplimiento', max_digits=10, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    def toJSON(self):
        item = model_to_dict(self)
        item['planning'] = self.planning.toJSON()
        item['customer'] = self.customer.toJSON()
        item['monetary_goal'] = format(self.monetary_goal, '.2f')
        item['real'] = format(self.monetary_goal, '.2f')
        item['fulfillment'] = format(self.monetary_goal, '.2f')
        return item

    def __str__ (self):
        return self.customer.business_name

''' Tablas promociones '''
class Promotions(BaseModel):
    name = models.CharField('Nombre promoción', max_length=50)
    desc = models.TextField('Descripción promoción')
    quantity = models.PositiveIntegerField('Cantidad disponible')
    cons = models.TextField('Consideraciones', blank = True, null = True)
    obs = models.TextField('Observaciones', blank = True, null = True)
    expiration_date = models.DateField('Fecha de vigencia', default=datetime.now)

    class Meta:
        verbose_name = 'Promoción'
        verbose_name_plural = 'Promociones'
        ordering = ['id']

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(Promotions, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        item['expiration_date'] = self.expiration_date.strftime('%Y-%m-%d')
        return item
    
    def __str__(self):
        return self.name

# Tabla detalle de productos por promoción
class PromotionProducts(BaseModel):
    prom = models.ForeignKey(Promotions, on_delete=models.CASCADE, verbose_name='Código promoción')
    product = models.ForeignKey(clsCatalogoProductosMdl, on_delete=models.CASCADE, verbose_name='Producto')
    sales_unit = models.ForeignKey(clsUnidadVentaMdl, on_delete=models.CASCADE, verbose_name='Unidad venta')
    quantity = models.PositiveIntegerField('Cantidad')
    unit_price = models.DecimalField('Precio unitario', max_digits=10, decimal_places=2, default=0.00)
    dcto = models.DecimalField('Descuento', max_digits=10, decimal_places=2, default=0)
    prom_price = models.DecimalField('Precio descuento', max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Promoción producto'
        verbose_name_plural = 'Promociones productos'
        ordering = ['id']

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(PromotionProducts, self).save()
    
    def toJSON(self):
        item = model_to_dict(self)
        item['prom'] = self.prom.toJSON()
        item['product'] = self.product.toJSON()
        item['und_venta'] = self.und_venta.toJSON()
        item['unit_price'] = format(self.unit_price, '.2f')
        item['dcto'] = format(self.dcto, '.2f')
        item['prom_price'] = format(self.prom_price, '.2f')
        return item
    
    def __str__(self):
        return self.prom.name

''' Tabla planificación compras'''
# Tabla planificación compras
class PurchasePlanning(BaseModel):
    measurement_date = models.DateTimeField('Fecha de medición', auto_now_add=True)
    monetary_goal = models.DecimalField('Meta monetaria', max_digits=10, decimal_places=2)
    real = models.DecimalField('Real', max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment = models.DecimalField('Cumplimiento', max_digits=10, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Planificación compras'
        verbose_name_plural= 'Planificaciones compras'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_adm_purchase_plan', 'Planificación compras'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(PurchasePlanning, self).save()
    
    def toJSON(self):
        item = model_to_dict(self)
        item['monetary_goal'] = format(self.monetary_goal, '.2f')
        item['real'] = format(self.monetary_goal, '.2f')
        item['fulfillment'] = format(self.monetary_goal, '.2f')
        
    def __str__ (self):
        return self.measurement_date

''' Tabla planificación almacén'''
# Tabla planificación compras
class WarehousePlanning(BaseModel):
    measurement_date = models.DateTimeField('Fecha de medición', auto_now_add=True)
    monetary_goal = models.DecimalField('Meta monetaria', max_digits=10, decimal_places=2)
    real = models.DecimalField('Real', max_digits=10, decimal_places=2, blank=True, null=True)
    fulfillment = models.DecimalField('Cumplimiento', max_digits=10, decimal_places=2, blank=True, null=True)
    objects = DataFrameManager()

    class Meta:
        verbose_name= 'Planificación compras'
        verbose_name_plural= 'Planificaciones compras'
        ordering = ['id']
        default_permissions = []
        permissions = (('bia_adm_warehouse_plan', 'Planificación almacén'),)

    def save(self, force_insert=False, force_update=False, using=None, 
            update_fields=None):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_creation = user
            else:
                self.user_update = user
        super(WarehousePlanning, self).save()
    
    def toJSON(self):
        item = model_to_dict(self)
        item['monetary_goal'] = format(self.monetary_goal, '.2f')
        item['real'] = format(self.monetary_goal, '.2f')
        item['fulfillment'] = format(self.monetary_goal, '.2f')
        
    def __str__ (self):
        return self.measurement_date




