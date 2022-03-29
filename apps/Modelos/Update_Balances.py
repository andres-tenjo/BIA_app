# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 13:50:43 2022

@author: FULERO
"""
import pandas as pd
from apps.Modelos.Several_func import *
import numpy as np
from apps.modulo_configuracion.models import *
from django.db import connection

# Calcula el nuevo valor del producto en una tabla de datos
# strCondition: Valor de la columna que indica si la orden está cerrada o abierta (str)
# strType: Valor de la columna que indica si es entrada o salida (str)
# intQuantity: Valor de la columna que contiene la cantidad del movimiento (int)
# Retorna el valor del saldoco el que se va a actualizar el cuadro de datos (int)
def fncActualizaPresaldoint(strCondition, strType, intQuantity):
    if strCondition!= 'AN':
        if strType== 'EN': return intQuantity
        else: return - 1* intQuantity
    else: return 0            

tplColumnasHistorico= ('id', 'creation_date', 'doc_number', 'document_type', 'type', 'quantity', 'batch', 
'expiration_date', 'unitary_cost', 'total_cost', 'crossing_doc', 'condition', 'balance', 'inv_value', 
'identification', 'product_code_id', 'store_id', 'user_id_id', 'pre_bal')

# Actualiza las tablas de histórico de movimiento y de saldo por bodega cuando se guarda un documento
# strDocumento: Corresponde al nombre del documento que se está guardando o anulando (str)
# dtfDocumento: Corresponde al cuadro de datos que se va a guardar en las tablas de histórico de movimientos y saldos de bodega 
# (pandas.DataFrame)
# tplColumnasHistorico: Corresponde a la tupla que contiene el nombre de las columnas que contiene la tabla Historico de movimientos
# tuple(str)
# Carga automáticamente la información en las correspondientes tablas
def fncActualizaSaldo(strDocumento, dtfDocumento, tplColumnasHistorico= tplColumnasHistorico):
    lstNombreDocumentos= [strDocumento== 'Ingreso_de_almacén', 
                          strDocumento== 'Devolución_de_cliente', 
                          strDocumento== 'Devolución_a_proveedor', 
                          strDocumento== 'Salida_de_almacén', 
                          strDocumento== 'Obsequio']
    lstAccion= ['EN', 'EN', 'SA', 'SA', 'SA']
    if (strDocumento!= 'Ajuste_De_Inventario') & (strDocumento!= 'Traslado'):
        dtfModificado= dtfDocumento.assign(document_type= strDocumento, 
        Type= np.select(lstNombreDocumentos, lstAccion, 'No Definido'))
        dtfModificado= dtfModificado.rename(columns= {'Type': 'type'})
    else: dtfModificado= dtfDocumento.assign(document_type= strDocumento)
    intLlaveHistorico= fncLlavePrimariaint('modulo_configuracion_clshistoricomovimientosmdl')
    for i in range(len(dtfModificado)):
        varParametros= [
            int(intLlaveHistorico+ i),
            str(dtfModificado.iloc[i]['creation_date']),
            str(dtfModificado.iloc[i]['doc_number']),
            str(dtfModificado.iloc[i]['document_type']),
            str(dtfModificado.iloc[i]['type']),            
            int(dtfModificado.iloc[i]['quantity']),
            str(dtfModificado.iloc[i]['batch']),
            str(dtfModificado.iloc[i]['expiration_date']),
            float(dtfModificado.iloc[i]['unitary_cost']),
            float(dtfModificado.iloc[i]['total_cost']),
            'N.A.' if (strDocumento== 'Ajuste_De_Inventario') | (strDocumento== 'Obsequio') | (strDocumento== 'Traslado')\
                else str(dtfModificado.iloc[i]['crossing_doc']),
            str(dtfModificado.iloc[i]['condition']),
            # int(fncActualizaPresaldoint(dtfModificado.iloc[i]['condition'], 
            #                         dtfModificado.iloc[i]['type'], dtfModificado.iloc[i]['quantity'])),
            int(fncActualizaPresaldoint(dtfModificado.iloc[i]['condition'], 
                                    dtfModificado.iloc[i]['type'], dtfModificado.iloc[i]['quantity'])),
            int(fncActualizaPresaldoint(dtfModificado.iloc[i]['condition'], 
                                    dtfModificado.iloc[i]['type'], dtfModificado.iloc[i]['quantity']))\
                * int(dtfModificado.iloc[i]['quantity']),  
            str(dtfModificado.iloc[i]['identification']),
            int(dtfModificado.iloc[i]['product_code_id']),
            int(dtfModificado.iloc[i]['store_id']),
            int(dtfModificado.iloc[i]['user_id_id']), 
            # int(dtfModificado.iloc[i]['store_id']),
            int(fncActualizaPresaldoint(dtfModificado.iloc[i]['condition'], 
                                    dtfModificado.iloc[i]['type'], dtfModificado.iloc[i]['quantity']))
            ]
        strConsultaSubirHistorico= '''INSERT INTO modulo_configuracion_clshistoricomovimientosmdl 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        strConsultaHistorico= '''SELECT * FROM modulo_configuracion_clshistoricomovimientosmdl WHERE store_id= %s AND 
        product_code_id= %s AND batch= %s'''
        strConsultaSubirSaldo= 'INSERT INTO modulo_configuracion_clssaldosinventariomdl VALUES(%s, %s, %s, %s, %s, %s)'
        dtfDocumentoProducto= dtfModificado.iloc[i: i+ 1, :]
        # if len(fncConsultalst(strConsultaHistorico, [varParametros[18], varParametros[16], varParametros[6]]))== 0:
        if len(fncConsultalst(strConsultaHistorico, [varParametros[16], varParametros[15], varParametros[6]]))== 0:
            fncConsultalst(strConsultaSubirHistorico, varParametros)
            intLlaveSaldo= fncLlavePrimariaint('modulo_configuracion_clssaldosinventariomdl')
            # fncConsultalst(strConsultaSubirSaldo, [int(intLlaveSaldo+ i), varParametros[6], int(fncActualizaPresaldoint(dtfModificado.iloc[i]['condition'], 
            # dtfModificado.iloc[i]['type'], dtfModificado.iloc[i]['quantity'])), varParametros[7], varParametros[16], varParametros[18]])
            fncConsultalst(strConsultaSubirSaldo, [int(intLlaveSaldo+ i), varParametros[6], int(fncActualizaPresaldoint(dtfModificado.iloc[i]['condition'], 
            dtfModificado.iloc[i]['type'], dtfModificado.iloc[i]['quantity'])), varParametros[7], varParametros[15], varParametros[16]])
        else:
            lstHistorico= fncConsultalst(strConsultaHistorico, [varParametros[18], varParametros[16], varParametros[6]])
            dtfHistoricoModficado= pd.DataFrame(lstHistorico, columns= list(tplColumnasHistorico))
            dtfHistoricoConcatenado= pd.concat([dtfHistoricoModficado, dtfDocumentoProducto])\
                .fillna(0).reset_index().drop(['index'], axis= 1)    
            dtfHistoricoConcatenado= dtfHistoricoConcatenado[- 2: ].reset_index().drop(['index'], axis= 1)
            index= [i for i in range(len(dtfHistoricoConcatenado))]
            dtfHistoricoConcatenado.at[index[- 1], 'pre_bal']= dtfHistoricoConcatenado.iloc[- 1]['quantity']\
                if dtfHistoricoConcatenado.iloc[- 1]['type']== 'EN' else dtfHistoricoConcatenado.iloc[- 1]['quantity']* - 1
            dtfHistoricoConcatenado.at[index[- 1], 'balance']= dtfHistoricoConcatenado.iloc[- 1]['pre_bal']\
                + int(dtfHistoricoConcatenado.iloc[0]['balance'])
            dtfHistoricoASubir= dtfHistoricoConcatenado[- 1: ].reset_index().drop(['index'], axis= 1)
            dtfHistoricoASubir['id']= int(intLlaveHistorico+ i)
            dtfHistoricoASubir.loc[: , 'creation_date']= dtfHistoricoASubir['creation_date'].astype(str)
            dtfHistoricoASubir.loc[: , 'product_code_id']= dtfHistoricoASubir['product_code_id'].astype(int)
            dtfHistoricoASubir.loc[: , 'quantity']= dtfHistoricoASubir['quantity'].astype(int)
            dtfHistoricoASubir.loc[: , 'batch']= dtfHistoricoASubir['batch'].astype(str)
            dtfHistoricoASubir.loc[: , 'expiration_date']= dtfHistoricoASubir['expiration_date'].astype(str)
            dtfHistoricoASubir.loc[: , 'unitary_cost']= dtfHistoricoASubir['unitary_cost'].astype(float)
            dtfHistoricoASubir.loc[: , 'total_cost']= dtfHistoricoASubir['total_cost'].astype(float)
            dtfHistoricoASubir.loc[: , 'pre_bal']= dtfHistoricoASubir['pre_bal'].astype(int)
            dtfHistoricoASubir.loc[: , 'balance']= dtfHistoricoASubir['balance'].astype(int)
            dtfHistoricoASubir.loc[: , 'inv_value']= dtfHistoricoASubir['inv_value'].astype(float)
            dtfHistoricoASubir.loc[: , 'store_id']= dtfHistoricoASubir['store_id'].astype(int)
            dtfHistoricoASubir.loc[: , 'identification']= dtfHistoricoASubir['identification'].astype(str)
            dtfHistoricoASubir.loc[: , 'user_id_id']= dtfHistoricoASubir['user_id_id'].astype(int)
            dtfHistoricoASubir.at[0, 'inv_value']= dtfHistoricoASubir.iloc[0]['balance']\
                * dtfHistoricoASubir.iloc[0]['unitary_cost']
            lstProductos= dtfHistoricoASubir['product_code_id'].values.tolist()
            lstCantidad= dtfHistoricoASubir['balance'].values.tolist()
            lstBodega= dtfHistoricoASubir['store_id'].values.tolist()
            lstLotes= dtfHistoricoASubir['batch'].values.tolist()
            for i, cod in enumerate(lstProductos):
                strActualiza= '''UPDATE modulo_configuracion_clssaldosinventariomdl SET inventory_avail= %s 
                WHERE product_code_id= %s AND batch= %s AND store_id= %s'''
                varSaldos= [lstCantidad[i], lstProductos[i], lstLotes[i], lstBodega[i]]
                fncConsultalst(strActualiza, varSaldos)
            with connection.cursor() as cursor:
                sqlite3.register_adapter(np.int64, lambda val: int(val))
                sqlite3.register_adapter(np.int32, lambda val: int(val))
                strInserta= f'''INSERT INTO modulo_configuracion_clshistoricomovimientosmdl {tplColumnasHistorico} VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                cursor.executemany(strInserta, dtfHistoricoASubir.to_records(index= False))
    print('se actualizó el histórico y la bodega')
    return 'se actualizó el histórico y la bodega'

# Actualiza los valores para recalcular los saldos de bodega desde un inicio a fin 
# dtfDatos: Corresponde al cuadro de datos donde se va a realizar el recalculo de saldos de inventario (pandas.DataFrame)
# Actualiza los saldos y presaldos de ciertos regisros en el histórico de movimientos
def fncRecalculoSaldoPresaldo(dtfDatos):
    intBodega= int(dtfDatos['store_id'].unique()[0])
    intCodigo= int(dtfDatos['product_code_id'].unique()[0])
    strLote= dtfDatos['batch'].unique()[0]
    dtfDatos.at[1, 'pre_bal']= 0
    dtfDatos= dtfDatos.assign(NewBalance= dtfDatos['pre_bal'])
    dtfDatos.at[0, 'NewBalance']= dtfDatos.iloc[0]['balance']
    dtfDatos= dtfDatos.drop(['balance', 'inv_value'], axis= 1)
    dtfDatos= dtfDatos.assign(balance= dtfDatos['NewBalance'].cumsum())
    dtfActualizado= dtfDatos.assign(inv_value= dtfDatos['unitary_cost']* dtfDatos['balance']).drop(['NewBalance'], axis= 1)
    lstDocumentos= dtfActualizado['doc_number'].values.tolist()
    lstPreSaldo= dtfActualizado['pre_bal'].values.tolist()
    lstSaldo= dtfActualizado['balance'].values.tolist()
    strActualiza= '''UPDATE modulo_configuracion_clshistoricomovimientosmdl SET pre_bal= %s, balance= %s WHERE store_id= %s 
    AND product_code_id= %s AND doc_number= %s'''
    for j, val in enumerate(lstDocumentos):
        fncConsultalst(strActualiza, [lstPreSaldo[j], lstSaldo[j], intBodega, intCodigo, lstDocumentos[j]])
    strEstado= 'UPDATE modulo_configuracion_clshistoricomovimientosmdl SET condition= %s WHERE doc_number= %s'
    fncConsultalst(strEstado, ['AN' ,lstDocumentos[1]])
    strSaldo= '''UPDATE modulo_configuracion_clssaldosinventariomdl SET inventory_avail= %s WHERE product_code_id= %s AND 
    batch= %s AND store_id= %s'''
    fncConsultalst(strSaldo, [lstSaldo[- 1], intCodigo, strLote, intBodega])
    return 

# Actualiza el histórico de movimiento y el saldo por bodega cuando se anula un documento transaccional
# strDocumento: Corresponde al documento que se va a anular (str)
# tplColumnasHistorico: Corresponde a la tupla que contiene el nombre de las columnas que contiene la tabla Historico de movimientos
# tuple(str)
# Realiza la actualización de las tablas del histórico de movimiento y de saldo por bodega
def fncActualizaAnulado(strDocumento, tplColumnasHistorico= tplColumnasHistorico):
    strConsultaDocumento= 'SELECT * FROM modulo_configuracion_clshistoricomovimientosmdl WHERE doc_number= %s'
    lstDocumento= fncConsultalst(strConsultaDocumento, [strDocumento])
    if len(lstDocumento)> 1: dtfDocumento= pd.DataFrame(lstDocumento, columns= list(tplColumnasHistorico))
    else: dtfDocumento= pd.DataFrame(np.array(lstDocumento[0]).reshape(- 1, len(list(lstDocumento[0][- 1]))), 
                                     columns= list(tplColumnasHistorico))
    strConsulta= '''SELECT * FROM modulo_configuracion_clshistoricomovimientosmdl WHERE product_code_id= %s AND store_id= %s 
    AND batch= %s'''
    lstCodigos= dtfDocumento['product_code_id'].values.tolist()
    lstBodegas= dtfDocumento['store_id'].values.tolist()
    lstLotes= dtfDocumento['batch'].values.tolist()
    lstConsultas= [fncConsultalst(strConsulta, [lstCodigos[i], lstBodegas[i], lstLotes[i]]) for i, val in enumerate(lstCodigos)]
    lstIndices= [j for i, lst in enumerate(lstConsultas) for j, val in enumerate(lst) if strDocumento in val]
    lstConsultaFiltrada= [lstConsultas[i][lstIndices[i]- 1: ] for i, j in enumerate(lstConsultas)]
    lstATrabajar= [pd.DataFrame(lst, columns= list(tplColumnasHistorico)) for i, lst in enumerate(lstConsultaFiltrada)]    
    for i in lstATrabajar:
        fncRecalculoSaldoPresaldo(i)
    return