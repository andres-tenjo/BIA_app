from rest_framework import serializers
from django.utils.formats import number_format
from apps.modulo_configuracion.models import *

exclude_tuple = (
    'user_creation', 
    'creation_date', 
    'user_update', 
    'update_date',
    'state'
    )

class clsDepartamentosMdlSerializer(serializers.ModelSerializer):
    class Meta:
        model = clsDepartamentosMdl
        fields = (
            'id',
            'department_name',
            )

class clsCiudadesMdlSerializer(serializers.ModelSerializer):
    class Meta:
        model = clsCiudadesMdl
        fields = (
            'id',
            'city_name',
            )

class clsCategoriaProductoMdlSerializer(serializers.ModelSerializer):
    class Meta:
        model = clsCategoriaProductoMdl
        exclude = exclude_tuple

class ProductSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = clsSubcategoriaProductoMdl
        exclude = exclude_tuple

class clsUnidadCompraMdlSerializer(serializers.ModelSerializer):
    class Meta:
        model = clsUnidadCompraMdl
        exclude = exclude_tuple

class clsUnidadVentaMdlSerializer(serializers.ModelSerializer):
    class Meta:
        model = clsUnidadVentaMdl
        exclude = exclude_tuple

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = clsCatalogoProductosMdl
        exclude = exclude_tuple

class clsCategoriaClienteMdlSerializer(serializers.ModelSerializer):
    class Meta:
        model = clsCategoriaClienteMdl
        exclude = exclude_tuple

class clsZonaClienteMdlSerializer(serializers.ModelSerializer):
    class Meta:
        model = clsZonaClienteMdl
        exclude = exclude_tuple

class CustomerAdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = clsAsesorComercialMdl
        fields = (
            'id',
            'advisor',
            )

class clsCatalogoProductosPlantillajson(serializers.ModelSerializer):
    class Meta:
        model = clsCatalogoProductosMdl
        fields = (
            'id',
            'product_desc',
            )

class clsCatalogoProveedoresPlantillajson(serializers.ModelSerializer):
    class Meta:
        model = clsCatalogoProveedoresMdl
        fields = (
            'id',
            'identification',
            'supplier_name',
            )

class clsCatalogoClientesPlantillajson(serializers.ModelSerializer):
    class Meta:
        model = clsCatalogoClientesMdl
        fields = (
            'id',
            'identification',
            'business_name',
            )

class clsCatalogoBodegasPlantillajson(serializers.ModelSerializer):
    class Meta:
        model = clsCatalogoBodegasMdl
        fields = (
            'id',
            'warehouse_name',
            'contact_name',
            )

class clsCatalogoProductosMdlSerializer(serializers.ModelSerializer):
    cost_pu = serializers.SerializerMethodField('fncFormatoNumero')
    full_sale_price = serializers.SerializerMethodField('fncFormatoNumero')
    iva = serializers.SerializerMethodField('fncFormatoNumero')
    other_tax = serializers.SerializerMethodField('fncFormatoNumero')
    product_cat = serializers.StringRelatedField()
    product_subcat = serializers.StringRelatedField()
    purchase_unit = serializers.StringRelatedField()
    sales_unit = serializers.StringRelatedField()
    creation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    state_display = serializers.CharField(
        source='get_state_display'
    )
    class Meta:
        model = clsCatalogoProductosMdl
        exclude = ('qr_code','split','state', 'user_creation', 'user_update')
    
    def fncFormatoNumero(self, obj):
        return number_format(obj.cost_pu)

class clsCatalogoProveedoresMdlSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    creation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    person_type_display = serializers.CharField(
        source='get_person_type_display'
    )
    id_type_display = serializers.CharField(
        source='get_id_type_display'
    )
    pay_method_display = serializers.CharField(
        source='get_pay_method_display'
    )
    logistic_condition_display = serializers.CharField(
        source='get_logistic_condition_display'
    )
    state_display = serializers.CharField(
        source='get_state_display'
    )
    class Meta:
        model = clsCatalogoProveedoresMdl
        exclude = ('qr_code', 'user_creation', 'user_update', 'person_type', 'id_type', 'pay_method', 'state', 'logistic_condition')

class clsCatalogoClientesMdlSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    customer_zone = serializers.StringRelatedField()
    customer_cat = serializers.StringRelatedField()
    commercial_advisor = serializers.StringRelatedField()
    creation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    person_type_display = serializers.CharField(
        source='get_person_type_display'
    )
    id_type_display = serializers.CharField(
        source='get_id_type_display'
    )
    pay_method_display = serializers.CharField(
        source='get_pay_method_display'
    )
    state_display = serializers.CharField(
        source='get_state_display'
    )
    class Meta:
        model = clsCatalogoClientesMdl
        exclude = ('qr_code','user_creation', 'user_update', 'person_type', 'id_type', 'pay_method', 'state')

class clsCatalogoBodegasSerializador(serializers.ModelSerializer):
    department = serializers.StringRelatedField()
    city = serializers.StringRelatedField()
    creation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    update_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    state_display = serializers.CharField(
        source='get_state_display'
    )
    class Meta:
        model = clsCatalogoBodegasMdl
        exclude = ('qr_code','user_creation', 'user_update', 'state')

class clsSaldosInventarioMdlSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = clsSaldosInventarioMdl
        fields = '__all__'

class clsAjusteInventarioMdlSerializador(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = clsAjusteInventarioMdl
        exclude = ('user_update', 'update_date')

class clsDetalleAjusteInventarioMdlSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = clsDetalleAjusteInventarioMdl
        fields = '__all__'




class clsEntradasAlmacenMdlSerializador(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = clsEntradasAlmacenMdl
        exclude = ('user_update', 'update_date', 'total_cost')

class clsTblDetalleEntradaAlmacenSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = clsTblDetalleEntradaAlmacen
        exclude = ('state',)

class clsDevolucionesClienteMdlSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = clsDevolucionesClienteMdl
        exclude = ('user_creation', 'user_update', 'update_date', 'returnin_type', 'total_cost')

class clsDetalleDevolucionesClienteMdlSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = clsDetalleDevolucionesClienteMdl
        exclude = ('state',)

class clsDevolucionesProveedorMdlSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = clsDevolucionesProveedorMdl
        exclude = ('user_creation', 'user_update', 'update_date', 'returnin_type', 'total_cost')

class clsDetalleDevolucionesProveedorMdlSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = clsDetalleDevolucionesProveedorMdl
        exclude = ('state',)

class clsSalidasAlmacenMdlSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = clsSalidasAlmacenMdl
        exclude = ('user_creation', 'user_update', 'update_date', 'credit_state', 'taxes', 'discount', 'total_price', 'total_amount', 'total_cost', 'value_paid')

class clsDetalleSalidasAlmacenMdlSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = clsDetalleSalidasAlmacenMdl
        exclude = ('unit_price', 'taxes', 'discount', 'total_price', 'total_amount')

class clsObsequiosMdlSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = clsObsequiosMdl
        exclude = ('user_creation', 'user_update', 'update_date', 'total_cost')

class clsDetalleObsequiosMdlSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = clsDetalleObsequiosMdl
        exclude = ('state',)

class clsTrasladosBodegasMdlSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = clsTrasladosBodegasMdl
        exclude = ('user_creation', 'user_update', 'update_date', 'total_cost')

class clsDetalleTrasladosBodegaMdlSerializador(serializers.ModelSerializer):
    
    class Meta:
        model = clsDetalleTrasladosBodegaMdl
        exclude = ('state',)