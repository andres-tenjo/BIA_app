from import_export import resources
from .models import *

''' Categoria de productos'''
class CategoryProductResource(resources.ModelResource):

    class Meta:
        model = clsCategoriaProductoMdl
        exclude = ('user_creation', 'date_creation', 'user_update', 'date_update', 'state')

''' Subcategoria de productos'''
class clsSubcategoriaProductoMdlResource(resources.ModelResource):

    class Meta:
        model = clsSubcategoriaProductoMdl
        exclude = ('user_creation', 'date_creation', 'user_update', 'date_update', 'state')

''' Unidad de compra de productos'''
class clsUnidadCompraMdlResource(resources.ModelResource):

    class Meta:
        model = clsUnidadCompraMdl
        exclude = ('user_creation', 'date_creation', 'user_update', 'date_update', 'state')

''' Unidad de venta de productos'''
class SaleUnitResource(resources.ModelResource):

    class Meta:
        model = clsUnidadVentaMdl
        exclude = ('user_creation', 'date_creation', 'user_update', 'date_update', 'state')

''' Unidad de venta de productos'''
class ProductResource(resources.ModelResource):

    class Meta:
        model = clsCatalogoProductosMdl
        exclude = ('user_creation', 'date_creation', 'user_update', 'date_update', 'state')