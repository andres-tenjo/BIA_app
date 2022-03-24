import pandas as pd
from apps.Modelos.Several_func import fncConsultalst
from apps.Modelos.Customer_Credit import fncClienteCreditotpl

# Inactiva las condiciones de compra a un proveedor cuando se inactiva un producto
# intProducto: Corresponde al código del producto para consultar (int)
# strNombreTabla: Corresponde al nombre de la tabla de la condición comercial donde se va a realizar la inactivación (str)
# Actualiza la tabla seleccionada en la condición específica para la inactivación
def fncInactivaCondicionProducto(intProducto, strNombreTabla):
    strConsulta= f'''UPDATE {strNombreTabla} SET state= %s WHERE product_code_id= %s AND state= %s'''
    fncConsultalst(strConsulta, ['IN', intProducto, 'AC'])
    return print('Se actualizó el estado de la condición para el producto')
    
# Confirma si existe inventario para uno o varios productos en una bodega específica
# intVariable: Corresponde al código del producto o al código de la bodega como valor del filtro (int)
# strColumnaFiltro: Corresponde a la columna donde se va a realizar el filtro en la tabla (str)
# Retorna una tupla un boleano y un cuadro de datos, según el resultado de la consulta (tuple(bool, pandas.DataFrame))
def fncExisteInventariotpl(intVariable, strColumnaFiltro):
    strSaldoInventario= f'''SELECT product_code_id, batch, inventory_avail, store_id FROM 
    modulo_configuracion_clssaldosinventariomdl WHERE {strColumnaFiltro}= %s'''
    lstSaldoInventario= fncConsultalst(strSaldoInventario, [intVariable])
    if len(lstSaldoInventario)== 0: return (True, '')
    else:
        lstBoleano= [0 if i[2]== 0 else 1 for i in lstSaldoInventario]
        if sum(lstBoleano)== 0: return (True, '')
        else: 
            dtfSaldoInventario= pd.DataFrame(lstSaldoInventario, columns= ['Código Producto', 'Lote', 'Inventario Disponible', 
            'Bodega'])
            return (False, dtfSaldoInventario.loc[dtfSaldoInventario['Inventario Disponible']!= 0])    


# Realiza la consulta para confirmar si existen registros abiertos para un documento específico
# intProducto: Corresponde al código del producto para consultar (int)
# strTablaDetalle: Corresponde al nombre de la tabla de detalle a consultar (str)
# strTablaGeneral: Corresponde al nombre de la tabla de general a consultar (str)
# strColumna1: Corresponde al nombre de la columna en la tabla a importar (str)
# strColumna2: Corresponde al nombre a asignar al cuadro de datos para la columna específica consultada (str)
# strColumna3: Corresponde al nombre de la columna a filtrar (str)
# strValor: Corresponde al filtro a usar en la columna (str)
# Retorna una tupla un boleano y un cuadro de datos, según el resultado de la consulta (tuple(bool, pandas.DataFrame))
def fncDAbiertoProductotpl(intProducto, strTablaDetalle, strTablaGeneral, strColumna1, strColumna2, strColumna3, strValor):
    strConsultaDetalle= f'''SELECT doc_number_id FROM {strTablaDetalle} WHERE product_code_id= %s'''
    lstConsultaDetalle= fncConsultalst(strConsultaDetalle, [intProducto])
    if len(lstConsultaDetalle)== 0: return True, 
    else:
        dtfConsultaDetalle= pd.DataFrame(lstConsultaDetalle, columns= ['key'])
        lstDocumentos= [i[0] for i in lstConsultaDetalle]
        lstDatos= []
        for i in lstDocumentos:
            strConsultaGeneral= f'''SELECT id, creation_date, doc_number, {strColumna1} FROM {strTablaGeneral}
            WHERE id= %s AND {strColumna3}= %s'''
            lstConsultaGeneral= fncConsultalst(strConsultaGeneral, [i, strValor])
            if len(lstConsultaGeneral)== 0: pass
            else: lstDatos.append(lstConsultaGeneral)
        if len(lstDatos)== 0: return True,
        else: 
            lstCuadroDatos= [pd.DataFrame(i, columns= ['key', 'Fecha Creacion', 'N° Documento', f'{strColumna2}'])\
                for i in lstDatos]
            if len(lstCuadroDatos)== 1: dtfConsultaGeneral= lstCuadroDatos[0]
            else: dtfConsultaGeneral= pd.concat(lstCuadroDatos)
            return False, dtfConsultaGeneral.merge(dtfConsultaDetalle, how= 'left', on= 'key')

# Evalua cada tupla dentro de la lista para determinar si un código se puede inactivar
# lstConfirmacion: Lista que contiene tuplas con información correspondiente a diferentes validaciones (list)
# Retorna un valor booleano o una lista, según el resultado de la evaluación (bool, list)
def fncValidaConfirmaciontpl(lstConfirmacion):
    lstDatos= []
    for i in lstConfirmacion:
        if i[0]== True: pass
        else: lstDatos.append(i[1])
    if len(lstDatos)== 0: return (True, )
    else: return (False, lstDatos)

# Confirma si un producto se puede inactivar
# intProducto: Corresponde al código del producto a inactivar
# Retorna un valor booleano (True) que confirma si el producto se puede inactivar o un cuadro de datos con la información
# de por qué no se puede inactivar el producto (bool, pandas.DataFrame)
def fncInactivarProductotpl(intProducto):
    lstConfirmacion= [fncExisteInventariotpl(intProducto, 'product_code_id'),
    fncDAbiertoProductotpl(intProducto, 'modulo_configuracion_clsdetallepedidosmdl', 
    'modulo_configuracion_clspedidosmdl', 'identification_id', 'Código Cliente', 'condition', 'AB'), 
    fncDAbiertoProductotpl(intProducto, 'modulo_configuracion_clsdetalleordenescompramdl', 
    'modulo_configuracion_clsordenescompramdl', 'identification_id', 'Código Proveedor', 'condition', 'AB'),
    fncDAbiertoProductotpl(intProducto, 'modulo_configuracion_clsdetallelistapreciosmdl', 
    'modulo_configuracion_clslistapreciosmdl', 'store_id', 'Código Bodega', 'state', 'AC'),
    fncDAbiertoProductotpl(intProducto, 'modulo_configuracion_clsdetallecotizacionesmdl', 
    'modulo_configuracion_clscotizacionesmdl', 'identification_id', 'Código Cliente', 'condition', 'AB')]
    fncInactivaCondicionProducto(intProducto, 'modulo_configuracion_clscondiciondescuentoproveedormdl')
    fncInactivaCondicionProducto(intProducto, 'modulo_configuracion_clscondicionminimacompramdl')
    return fncValidaConfirmaciontpl(lstConfirmacion)

# Confirma si existen documentos abiertos para una bodega específica
# intBodega: Corresponde al código de la bodega (int)
# strTablaGeneral: Corresponde al nombre de la tabla de general a consultar (str)
# strColumna: Corresponde al nombre de la columna a filtrar (str)
# strValor: Corresponde al filtro a usar en la columna (str)
# Retorna una tupla un boleano y un cuadro de datos, según el resultado de la consulta (tuple(bool, pandas.DataFrame))
def fncDAbiertoBodegatpl(intBodega, strTablaGeneral, strColumna, strValor):
    strConsultaDocumento= f'''SELECT creation_date, doc_number, {strColumna} FROM {strTablaGeneral} WHERE store_id= %s
    AND {strColumna}= %s'''
    lstConsultaDocumento= fncConsultalst(strConsultaDocumento, [intBodega, strValor])
    if len(lstConsultaDocumento)== 0: return (True, '')
    else: return (False, pd.DataFrame(lstConsultaDocumento, columns= ['Fecha Creacion', 'N° Documento', 'Estado']))

# Confirma si una bodega se puede inactivar
# intBodega: Corresponde al código de la bodega (int)
# Retorna un valor booleano (True) que confirma si el asesor se puede inactivar o un cuadro de datos con la información
# de por qué no se puede inactivar el asesor (bool, pandas.DataFrame)
def fncInactivaBodegatpl(intBodega):
    lstConfirmacion= [fncExisteInventariotpl(intBodega, 'store_id'), 
    fncDAbiertoBodegatpl(intBodega, 'modulo_configuracion_clspedidosmdl', 'condition', 'AB'),
    fncDAbiertoBodegatpl(intBodega, 'modulo_configuracion_clsordenescompramdl', 'condition', 'AB'), 
    fncDAbiertoBodegatpl(intBodega, 'modulo_configuracion_clslistapreciosmdl', 'state', 'AC'), 
    fncDAbiertoBodegatpl(intBodega, 'modulo_configuracion_clscotizacionesmdl', 'condition', 'AB')]
    return fncValidaConfirmaciontpl(lstConfirmacion)

# Confirma si existen documentos documentos abiertos para un proveedor específico
# intProveedor: Corresponde al código del proveedor
# Retorna un valor booleano (True) que confirma si el asesor se puede inactivar o un cuadro de datos con la información
# de por qué no se puede inactivar el asesor (bool, pandas.DataFrame)
def fncDAbiertoProveedortpl(intProveedor):
    strConsultaDocumento= '''SELECT creation_date, doc_number, condition FROM modulo_configuracion_clsordenescompramdl
    WHERE identification_id= %s AND condition= %s'''
    lstConsultaDocumento= fncConsultalst(strConsultaDocumento, [intProveedor, 'AB'])
    if len(lstConsultaDocumento)== 0: return (True, )
    else: return (False, pd.DataFrame(lstConsultaDocumento, columns= ['Fecha Creacion', 'N° Documento', 'Estado']))

# Inactiva todas las condiciones donde aparece el proveedor
# intProveedor: Corresponde al código del proveedor
# strNombreTabla: Corresponde al nombre de la tabla de la condición comercial donde se va a realizar la inactivación (str)
# Actualiza el estado a inactivo en la tabla correspondiente de condiciones
def fncInactivaCondicionProveedor(intProveedor, strNombreTabla):
    strConsultaCondicion= f'''UPDATE {strNombreTabla} SET state= %s WHERE identification_id= %s AND state= %s'''
    fncConsultalst(strConsultaCondicion, ['IN', intProveedor, 'AC'])
    return print('Se inactivaron todas las condiciones para el proveedor')

# Confirma si un proveedor se puede inactivar
# intProveedor: Corresponde al código del proveedor
# Retorna un valor booleano (True) que confirma si el asesor se puede inactivar o un cuadro de datos con la información
# de por qué no se puede inactivar el asesor (bool, pandas.DataFrame)
def fncInactivaProveedortpl(intProveedor):
    lstConfirmacion= [fncDAbiertoProveedortpl(intProveedor)]
    fncInactivaCondicionProveedor(intProveedor, 'modulo_configuracion_clscondiciondescuentoproveedormdl')
    fncInactivaCondicionProveedor(intProveedor, 'modulo_configuracion_clscondicionminimacompramdl')
    return fncValidaConfirmaciontpl(lstConfirmacion)

# Confirma si un asesor comercial o una categoría de cliente o una zona se puede inactivar
# intAsesor: Corresponde al código del asesor (int)
# intVariable: Corresponde al código del producto o al código de la bodega como valor del filtro (int)
# strColumnaFiltro: Corresponde a la columna donde se va a realizar el filtro en la tabla (str)
# Retorna un valor booleano (True) que confirma si el asesor se puede inactivar o un cuadro de datos con la información
# de por qué no se puede inactivar el asesor (bool, pandas.DataFrame)
def fncInactivarAtrClientetpl(intVariable, strColumnaFiltro):
    strCatalogoCliente= f'''SELECT id, identification, business_name FROM modulo_configuracion_clscatalogoclientesmdl
    WHERE {strColumnaFiltro}= %s'''
    lstCatalogoCliente= fncConsultalst(strCatalogoCliente, [intVariable])
    if len(lstCatalogoCliente)== 0: return (True, )
    else: return (False, pd.DataFrame(lstCatalogoCliente, columns= ['Código Cliente', 'Identificación', 'Nombre Cliente']))

# Confirma si una categoría de producto o una subcategoría de producto o una unidad de compra o una unidad de venta se puede
# inactivar
# intVariable: Corresponde al código del producto o al código de la bodega como valor del filtro (int)
# strColumnaFiltro: Corresponde a la columna donde se va a realizar el filtro en la tabla (str)
# Retorna un valor booleano (True) que confirma si el asesor se puede inactivar o un cuadro de datos con la información
# de por qué no se puede inactivar el asesor (bool, pandas.DataFrame)
def fncInactivaAtrProductotpl(intVariable, strColumnaFiltro):
    strCatalogoProducto= f'''SELECT id, product_desc FROM modulo_configuracion_clscatalogoproductosmdl
    WHERE {strColumnaFiltro}= %s AND state= %s'''
    lstCatalogoProducto= fncConsultalst(strCatalogoProducto, [intVariable, 'AC'])
    if len(lstCatalogoProducto)== 0: return (True, )
    else: return (False, pd.DataFrame(lstCatalogoProducto, columns= ['Código Producto', 'Descripción Producto']))

# Confirma si una categoria de producto se puede inactivar
# intCategoriaProducto: Corresponde al código de la categoría de producto a inactivar (int)
# Retorna un valor booleano (True) que confirma si el asesor se puede inactivar o un cuadro de datos con la información
# de por qué no se puede inactivar el asesor (bool, pandas.DataFrame)
def fncInactivaCategoriaProductotpl(intCategoriaProducto):
    strSubCategoria= 'SELECT id, product_subcat FROM modulo_configuracion_clssubcategoriaproductomdl WHERE product_cat_id= %s'
    lstSubCategoria= fncConsultalst(strSubCategoria, [intCategoriaProducto])
    if len(lstSubCategoria)== 0: lstConfirmacion= [(True, )]
    else: lstConfirmacion= [(False, pd.DataFrame(lstSubCategoria, columns= ['Código SubCategoría', 'Nombre SubCategoría']))]
    lstConfirmacion.append(fncInactivaAtrProductotpl(intCategoriaProducto, 'product_cat_id'))
    return fncValidaConfirmaciontpl(lstConfirmacion)

# Confirma si una zona se puede inactivar 
# intZona: Corresponde al código de la zona a inactivar (int)
# Retorna un valor booleano (True) que confirma si el asesor se puede inactivar o un cuadro de datos con la información
# de por qué no se puede inactivar el asesor (bool, pandas.DataFrame)
def fncInactivarZonatpl(intZona):
    strAsesor= '''SELECT id, advisor FROM modulo_configuracion_clsasesorcomercialmdl WHERE zone_id= %s'''
    lstAsesor= fncConsultalst(strAsesor, [intZona])
    if len(lstAsesor)== 0: lstConfirmacion= [(True, )]
    else: lstConfirmacion= [(False, pd.DataFrame(lstAsesor, columns= ['Código Asesor', 'Descripción Asesor']))]
    lstConfirmacion.append(fncInactivarAtrClientetpl(intZona, 'customer_zone_id'))
    return fncValidaConfirmaciontpl(lstConfirmacion)

# Confirma si existen documentos abiertos para un cliente específico
# intCliente: Corresponde al código del cliente (int)
# strNombreTabla: Corresponde al nombre de la tabla del documento a consultar (str)
# Retorna un valor booleano (True) que confirma si el asesor se puede inactivar o un cuadro de datos con la información
# de por qué no se puede inactivar el asesor (bool, pandas.DataFrame)
def fncDAbiertoClientetpl(intCliente, strNombreTabla):
    strDocumento= f'''SELECT creation_date, doc_number, identification_id FROM {strNombreTabla} WHERE identification_id= %s
    AND condition= %s'''
    lstDocumento= fncConsultalst(strDocumento, [intCliente, 'AB'])
    if len(lstDocumento)== 0: return (True, )
    else: return (False, pd.DataFrame(lstDocumento, columns= ['Fecha Creación', 'N° Documento', 'Código Cliente']))

# Confirma si un cliente se puede inactivar
# intCliente: Corresponde al códigodel cliente a inactivar (int)
# Retorna un valor booleano (True) que confirma si el asesor se puede inactivar o un cuadro de datos con la información
# de por qué no se puede inactivar el asesor (bool, pandas.DataFrame)
def fncInactivaClientetpl(intCliente):
    lstConfirmacion= [fncDAbiertoClientetpl(intCliente, 'modulo_configuracion_clspedidosmdl')]
    lstConfirmacion.append(fncDAbiertoClientetpl(intCliente, 'modulo_configuracion_clscotizacionesmdl'))
    tplCredito= fncClienteCreditotpl(intCliente)
    if isinstance(tplCredito[0], str)== True: lstConfirmacion.append((True, ))
    else: lstConfirmacion.append((False, tplCredito[0]))
    return fncValidaConfirmaciontpl(lstConfirmacion)   
