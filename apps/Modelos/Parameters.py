import pandas as pd
from Several_func import *
from Inquiries import *
import sqlite3
import datetime as dt
import numpy as np

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
# dtfCatalogoProductos: Cuadro de datos que contiene la información de cada producto (pd.DataFrame)
# lstBasesDatos: Lista que contiene las bases de datos con la información del producto
# Retorna un cuadro de datos con el movimiento histórico del producto (pandas.DataFrame)
def fncMovimientoHistoricodtf(intCodigoProducto, dtfCatalogoProductos, lstBasesDatos):
    lstNombreDocumentos= ['Saldo_Inicial', 'Ajuste_de_inventario', 'Ingreso_de_almacén', 'Devolución_de_cliente', 
                          'Devolución_a_proveedor', 'Salida_de_almacén', 'Obsequio', 'Translado']
    dtfFiltroCatalogo= dtfCatalogoProductos.loc[dtfCatalogoProductos['product_code']== intCodigoProducto].reset_index()
    fltCostoUnitario= dtfFiltroCatalogo['cost_pu'][0]/ dtfFiltroCatalogo['split_(pu/su)'][0]
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
def fncMovimientosHistoricosProductosdtf():
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
# Linea para insertar el método que consulta desde django las bases de datos para importar las tablas abajo mencionadas
    db= data_consulting(['Initial_Balance', 'Inventory_Adjustment', 'Income', 'Customer_Return', 'Return_Supplier', 
                          'Outflows', 'Gifts', 'Transfer', 'Catálogo', 'Stores_Catalogue'])
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    dtfCatalogoProductos, dtfCatalogoBodegas, lstBasesDatos= db[8], db[9], db[: -2]
    lstCodigoBodegas= [i for i in dtfCatalogoBodegas['store_code'].unique()]
    lstDatosProducto= [[i.loc[i['store']==j] for i in lstBasesDatos] for j in lstCodigoBodegas]
    lstCodigoProductos= [pd.concat(i)['product_code'].unique() for i in lstDatosProducto]
    lstMovimientosHistoricos= [fncMovimientoHistoricodtf(lstCodigoProductos[i][j], dtfCatalogoProductos, lstDatosProducto[i])\
                               for i in range(0, len(lstDatosProducto)) for j in range(0, len(lstCodigoProductos[i]))]
    dtfMovimientoHistorico= pd.concat(lstMovimientosHistoricos).sort_values(by= ['store', 'creation_date', 'batch', 'document_type'])
    dtfMovimientoHistorico= dtfMovimientoHistorico.reindex(columns= ['creation_date', 'doc_number', 'document_type', 'type', 
                                                                     'product_code', 'quantity', 'batch', 'expiration_date', 
                                                                     'unitary_cost', 'total_cost', 'crossing_doc', 'condition', 
                                                                     'pre_bal', 'balance', 'inv_value', 'store', 'identification', 
                                                                     'unit_price', 'discount', 'total_price'])
    dtfMovimientoHistorico['id']= 'Código del super usuario'
    return dtfMovimientoHistorico