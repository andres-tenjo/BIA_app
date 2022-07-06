import pandas as pd
from django.db import connection
from apps.Modelos.Several_func import fncConsultalst, fncFormatoFechadtf
import numpy as np
import sqlite3
from sklearn.impute import KNNImputer

# Calcula un saldo no acumulado
# dtfMovimientoHistorico: Es el cuadro de datos que contiene el histórico de movimiento para todos los productos, bodegas y lotes
# (pd.DataFrame)
# Retorna una lista con los pre-saldos calculados
def fncPreSaldolst(dtfMovimientoHistorico):
    lstPresaldo= [dtfMovimientoHistorico['quantity'][i] if dtfMovimientoHistorico['type'][i]== 'EN'\
                else -1 * dtfMovimientoHistorico['quantity'][i] for i in range(0, len(dtfMovimientoHistorico['type']))]  
    return lstPresaldo

# Organiza cronológicamente los diferentes cuadros de datos para un producto construyendo el histórico de movimiento
# intCodigoProducto: Código del producto a construir el movimiento histórico (int)
# lstBasesDatos: Lista que contiene las bases de datos con la información del producto
# Retorna un cuadro de datos con el movimiento histórico del producto (pandas.DataFrame)
def fncMovimientoHistoricodtf(intCodigoProducto, lstBasesDatos):
    lstNombreDocumentos= ['Saldo_Inicial', 'Ajuste_de_inventario', 'Ingreso_de_almacén', 'Devolución_de_cliente', 
                          'Devolución_a_proveedor', 'Salida_de_almacén', 'Obsequio', 'Translado']
    strCatalogo= 'SELECT id, cost_pu, split FROM modulo_configuracion_clscatalogoproductosmdl WHERE id= %s'
    lstCatalogo= fncConsultalst(strCatalogo, [intCodigoProducto])
    dtfFiltroCatalogo= pd.DataFrame(lstCatalogo, columns= ['product_code', 'cost_pu', 'split'])
    fltCostoUnitario= dtfFiltroCatalogo['cost_pu'][0]/ dtfFiltroCatalogo['split'][0]
    lstDatosProducto= [lstBasesDatos[i].loc[lstBasesDatos[i]['product_code']== intCodigoProducto] for i in range(
        0, len(lstBasesDatos))]
    for i in range(0, len(lstDatosProducto)):
        lstDatosProducto[i]= fncFormatoFechadtf(lstDatosProducto[i], 'creation_date')
        lstDatosProducto[i]= lstDatosProducto[i].assign(document_type= lstNombreDocumentos[i])
    lstDatosProducto[0]= lstDatosProducto[0].assign(
        Type= 'EN', total_cost= fltCostoUnitario* lstDatosProducto[0]['quantity'], doc_number= '')
    for i in range(2, 4):
        lstDatosProducto[i]= lstDatosProducto[i].assign(Type= 'EN')        
    for i in range(2, 6):
        lstDatosProducto[i]= lstDatosProducto[i].assign(total_cost= fltCostoUnitario* lstDatosProducto[i]['quantity'])
    for i in range(4, 7):
        lstDatosProducto[i]= lstDatosProducto[i].assign(Type= 'SA')
    lstDatosProducto[1]= lstDatosProducto[1].rename(columns= {'type': 'Type'})
    lstDatosProducto[7]= lstDatosProducto[7].rename(columns= {'type': 'Type'})
    dtfMovimientoHistorico= pd.concat(lstDatosProducto).fillna(0)
    dtfMovimientoHistorico= dtfMovimientoHistorico.rename(columns= {'Type': 'type'})
    dtfMovimientoHistorico.sort_values(by= ['creation_date', 'batch', 'document_type'], inplace= True)
    dtfMovimientoHistorico.reset_index(inplace= True)
    dtfMovimientoHistorico.drop(['index'], axis= 1, inplace= True)
    dtfMovimientoHistorico= dtfMovimientoHistorico.assign(pre_bal= fncPreSaldolst(dtfMovimientoHistorico))
    dtfMovimientoHistorico= dtfMovimientoHistorico.assign(balance= dtfMovimientoHistorico['pre_bal'].cumsum())
    dtfMovimientoHistorico= dtfMovimientoHistorico.assign(inv_value= dtfMovimientoHistorico['balance']* fltCostoUnitario)
    return dtfMovimientoHistorico    

# Función que construye el histórico de movimientos para cada lote de cada producto en cada bodega que exista en las BBDD
# Corresponde a la lista que contiene los cuadros de datos requeridos para realizar la construcción del histórico (list)
# ['Saldo Inicial', 'Ajustes de Inventario', 'Entradas', 'Devoluciones de clientes', 'Devoluciones a proveedor', 
#                      'salidas', 'obsequíos', 'Traslados', 'Catálogo de productos', 'Catálogo de bodegas']
def fncMovimientosHistoricosProductosdtf(lstDocumentos):
    tplColumnasHistorico= ('id', 'creation_date', 'doc_number', 'document_type', 'type', 'quantity', 'batch', 'expiration_date', 
    'unitary_cost', 'total_cost', 'total_price', 'crossing_doc', 'condition', 'pre_bal', 'balance', 'inv_value', 'identification', 
    'product_code_id', 'store_id', 'user_id_id')
    lstBasesDatos= lstDocumentos
    strConsultaBodegas= 'SELECT id FROM modulo_configuracion_clscatalogobodegasmdl'
    lstBodegas= fncConsultalst(strConsultaBodegas, [])
    lstCodigoBodegas= [i[0] for i in lstBodegas]
    lstDatosProducto= [[i.loc[i['store']==j] for i in lstBasesDatos] for j in lstCodigoBodegas]
    lstCodigoProductos= [pd.concat(i)['product_code'].unique() for i in lstDatosProducto]
    lstMovimientosHistoricos= [fncMovimientoHistoricodtf(lstCodigoProductos[i][j], lstDatosProducto[i])\
                               for i in range(0, len(lstDatosProducto)) for j in range(0, len(lstCodigoProductos[i]))]
    dtfMovimientoHistorico= pd.concat(lstMovimientosHistoricos).sort_values(by= ['store', 'creation_date', 'batch', 'document_type'])
    dtfMovimientoHistorico.drop(['unit_price', 'discount'], axis= 1, inplace= True)
    dtfMovimientoHistorico['id']= [i for i in range(1, len(dtfMovimientoHistorico['creation_date'])+ 1)]
    dtfMovimientoHistorico['user_id']= 1
    dtfMovimientoHistorico= dtfMovimientoHistorico.reindex(columns= ['id', 'creation_date', 'doc_number', 'document_type', 'type', 
    'quantity', 'batch', 'expiration_date', 'unitary_cost', 'total_cost', 'total_price', 'crossing_doc', 'condition', 'pre_bal', 
    'balance',  'inv_value', 'identification', 'product_code', 'store', 'user_id'])
    dtfMovimientoHistorico.loc[:, 'id']= dtfMovimientoHistorico['id'].astype(int)
    dtfMovimientoHistorico.loc[:, 'creation_date']= dtfMovimientoHistorico['creation_date'].astype(str)
    dtfMovimientoHistorico.loc[:, 'doc_number']= dtfMovimientoHistorico['doc_number'].astype(str)
    dtfMovimientoHistorico.loc[:, 'document_type']= dtfMovimientoHistorico['document_type'].astype(str)
    dtfMovimientoHistorico.loc[:, 'type']= dtfMovimientoHistorico['type'].astype(str)
    dtfMovimientoHistorico.loc[:, 'quantity']= dtfMovimientoHistorico['quantity'].astype(int)
    dtfMovimientoHistorico.loc[:, 'batch']= dtfMovimientoHistorico['batch'].astype(str)
    dtfMovimientoHistorico.loc[:, 'expiration_date']= dtfMovimientoHistorico['expiration_date'].astype(str)
    dtfMovimientoHistorico.loc[:, 'unitary_cost']= dtfMovimientoHistorico['unitary_cost'].astype(float)
    dtfMovimientoHistorico.loc[:, 'total_cost']= dtfMovimientoHistorico['total_cost'].astype(float)
    dtfMovimientoHistorico.loc[:, 'total_price']= dtfMovimientoHistorico['total_price'].astype(float)
    dtfMovimientoHistorico.loc[:, 'crossing_doc']= dtfMovimientoHistorico['crossing_doc'].astype(str)
    dtfMovimientoHistorico.loc[:, 'condition']= dtfMovimientoHistorico['condition'].astype(str)
    dtfMovimientoHistorico.loc[:, 'pre_bal']= dtfMovimientoHistorico['pre_bal'].astype(int)
    dtfMovimientoHistorico.loc[:, 'balance']= dtfMovimientoHistorico['balance'].astype(int)
    dtfMovimientoHistorico.loc[:, 'inv_value']= dtfMovimientoHistorico['inv_value'].astype(float)
    dtfMovimientoHistorico.loc[:, 'identification']= dtfMovimientoHistorico['identification'].astype(int)
    dtfMovimientoHistorico.loc[:, 'product_code']= dtfMovimientoHistorico['product_code'].astype(int)
    dtfMovimientoHistorico.loc[:, 'store']= dtfMovimientoHistorico['store'].astype(int)
    dtfMovimientoHistorico.loc[:, 'user_id']= dtfMovimientoHistorico['user_id'].astype(int)
    strConsultaHistorico= f'''INSERT INTO modulo_configuracion_clshistoricomovimientosalternomdl {tplColumnasHistorico} VALUES
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    with connection.cursor() as cursor:    
        sqlite3.register_adapter(np.int64, lambda val: int(val))
        sqlite3.register_adapter(np.int32, lambda val: int(val))
        cursor.executemany(strConsultaHistorico, dtfMovimientoHistorico.to_records(index= False))
        return