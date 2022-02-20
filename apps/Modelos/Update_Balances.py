# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 13:50:43 2022

@author: FULERO
"""
import pandas as pd
from apps.Modelos.Several_func import *
from apps.Modelos.Inquiries import *
import sqlite3
import datetime as dt
import numpy as np
from apps.modulo_configuracion.models import *

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

tplColumnasHistorico= ('creation_date', 'doc_number', 'document_type', 'type', 'product_code', 'quantity', 
                       'batch', 'expiration_date', 'unitary_cost', 'total_cost', 'crossing_doc', 'condition', 
                       'pre_bal', 'balance', 'inv_value', 'store', 'identification', 'user_id')

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
        dtfModificado= dtfDocumento.assign(document_type= strDocumento, Type= np.select(lstNombreDocumentos, lstAccion, 'No Definido'))
        dtfModificado= dtfModificado.rename(columns= {'Type': 'type'})
    else: dtfModificado= dtfDocumento.assign(document_type= strDocumento)
    for i in range(len(dtfModificado)):
        varParametros= [
            str(dtfModificado.iloc[i]['creation_date']),
            str(dtfModificado.iloc[i]['doc_number']),
            str(dtfModificado.iloc[i]['document_type']),
            str(dtfModificado.iloc[i]['type']),
            int(dtfModificado.iloc[i]['product_code']),
            int(dtfModificado.iloc[i]['quantity']),
            str(dtfModificado.iloc[i]['batch']),
            str(dtfModificado.iloc[i]['expiration_date']),
            str(dtfModificado.iloc[i]['unitary_cost']),
            str(dtfModificado.iloc[i]['total_cost']),
            'N.A.' if (strDocumento== 'Ajuste_De_Inventario') | (strDocumento== 'Obsequio') | (strDocumento== 'Traslado')\
                else str(dtfModificado.iloc[i]['crossing_doc']),
            str(dtfModificado.iloc[i]['condition']),
            int(fncActualizaPresaldoint(dtfModificado.iloc[i]['condition'], 
                                    dtfModificado.iloc[i]['type'], dtfModificado.iloc[i]['quantity'])),
            int(fncActualizaPresaldoint(dtfModificado.iloc[i]['condition'], 
                                    dtfModificado.iloc[i]['type'], dtfModificado.iloc[i]['quantity'])),
            int(fncActualizaPresaldoint(dtfModificado.iloc[i]['condition'], 
                                    dtfModificado.iloc[i]['type'], dtfModificado.iloc[i]['quantity']))\
                * int(dtfModificado.iloc[i]['quantity']), 
            int(dtfModificado.iloc[i]['store']),
            int(dtfModificado.iloc[i]['identification']), 
            int(dtfModificado.iloc[i]['user_id'])
            ]
        dtfDocumentoProducto= dtfModificado.iloc[i: i+ 1, :]
        qrsHistoricoMovimientos = clsHistoricoMovimientosMdl.objects.filter(store=varParametros[15], product_code= varParametros[4], batch=varParametros[6])
        if not qrsHistoricoMovimientos:
            clsHistoricoMovimientosMdl.objects.create(
                creation_date = varParametros[0],
                doc_number = varParametros[1],
                document_type = varParametros[2],
                type = varParametros[3],
                product_code_id = varParametros[4],
                quantity = varParametros[5],
                batch = varParametros[6],
                expiration_date = varParametros[7],
                unitary_cost = float(varParametros[8]),
                total_cost = float(varParametros[9]),
                crossing_doc = varParametros[10],
                condition = varParametros[11],
                pre_bal = varParametros[12],
                balance = varParametros[13],
                inv_value = varParametros[14],
                store_id = varParametros[15],
                identification = varParametros[16],
                user_id_id = int(varParametros[17])
            )
            qrsSaldosInventario = clsSaldosInventarioMdl()
            qrsSaldosInventario.product_code_id = varParametros[4]
            qrsSaldosInventario.batch = varParametros[6]
            qrsSaldosInventario.inventory_avail = int(fncActualizaPresaldoint(dtfModificado.iloc[i]['condition'], dtfModificado.iloc[i]['type'], dtfModificado.iloc[i]['quantity']))
            qrsSaldosInventario.expiration_date = varParametros[7]
            qrsSaldosInventario.store_id = varParametros[15]
            qrsSaldosInventario.save()
        else:
            lstHistorico= clsHistoricoMovimientosMdl.objects.filter(store=varParametros[15], product_code= varParametros[4], batch=varParametros[6]).values_list(
                'creation_date',
                'doc_number',
                'document_type',
                'type',
                'product_code',
                'quantity',
                'batch',
                'expiration_date',
                'unitary_cost',
                'total_cost',
                'crossing_doc',
                'condition',
                'pre_bal',
                'balance',
                'inv_value',
                'store',
                'identification',
                'user_id',
            )
            dtfHistoricoModficado= pd.DataFrame(lstHistorico,
                                                  columns= list(tplColumnasHistorico))
            dtfHistoricoConcatenado= pd.concat([dtfHistoricoModficado, dtfDocumentoProducto])\
                .fillna(0).reset_index().drop(['index'], axis= 1)
            index= [i for i in range(len(dtfHistoricoConcatenado))]
            dtfHistoricoConcatenado.at[index[- 1], 'pre_bal']= dtfHistoricoConcatenado.iloc[- 1]['quantity']\
                if dtfHistoricoConcatenado.iloc[- 1]['type']== 'EN' else dtfHistoricoConcatenado.iloc[- 1]['quantity']* - 1                
            dtfHistoricoConcatenado.at[index[- 1], 'balance']= dtfHistoricoConcatenado.iloc[- 1]['pre_bal']\
                + int(dtfHistoricoConcatenado.iloc[0]['balance'])
            dtfHistoricoASubir= dtfHistoricoConcatenado[- 1: ].reset_index().drop(['index'], axis= 1)
            dtfHistoricoASubir.loc[: , 'creation_date']= dtfHistoricoASubir['creation_date'].astype(str)
            dtfHistoricoASubir.loc[: , 'product_code']= dtfHistoricoASubir['product_code'].astype(int)
            dtfHistoricoASubir.loc[: , 'quantity']= dtfHistoricoASubir['quantity'].astype(int)
            dtfHistoricoASubir.loc[: , 'batch']= dtfHistoricoASubir['batch'].astype(str)
            dtfHistoricoASubir.loc[: , 'expiration_date']= dtfHistoricoASubir['expiration_date'].astype(str)
            dtfHistoricoASubir.loc[: , 'unitary_cost']= dtfHistoricoASubir['unitary_cost'].astype(float)
            dtfHistoricoASubir.loc[: , 'total_cost']= dtfHistoricoASubir['total_cost'].astype(float)
            dtfHistoricoASubir.loc[: , 'pre_bal']= dtfHistoricoASubir['pre_bal'].astype(int)
            dtfHistoricoASubir.loc[: , 'balance']= dtfHistoricoASubir['balance'].astype(int)
            dtfHistoricoASubir.loc[: , 'inv_value']= dtfHistoricoASubir['inv_value'].astype(float)
            dtfHistoricoASubir.loc[: , 'store']= dtfHistoricoASubir['store'].astype(int)
            dtfHistoricoASubir.loc[: , 'identification']= dtfHistoricoASubir['identification'].astype(int)
            dtfHistoricoASubir.loc[: , 'user_id']= dtfHistoricoASubir['user_id'].astype(int)
            dtfHistoricoASubir.at[0, 'inv_value']= dtfHistoricoASubir.iloc[0]['balance']\
                * dtfHistoricoASubir.iloc[0]['unitary_cost']
            lstProductos= dtfHistoricoASubir['product_code'].values.tolist()
            lstCantidad= dtfHistoricoASubir['balance'].values.tolist()
            lstBodega= dtfHistoricoASubir['store'].values.tolist()
            lstLotes= dtfHistoricoASubir['batch'].values.tolist()
            print(dtfHistoricoASubir)
            for i, cod in enumerate(lstCantidad):
                clsSaldosInventarioMdl.objects.filter(store=lstBodega[i], product_code= lstProductos[i], batch=lstLotes[i]).update(inventory_avail=lstCantidad[i])
            for historico in (dtfHistoricoASubir.values.tolist()):
                clsHistoricoMovimientosMdl.objects.create(
                creation_date = historico[0],
                doc_number = historico[1],
                document_type = historico[2],
                type = historico[3],
                product_code_id = historico[4],
                quantity = historico[5],
                batch = historico[6],
                expiration_date = historico[7],
                unitary_cost = float(historico[8]),
                total_cost = float(historico[9]),
                crossing_doc = historico[10],
                condition = historico[11],
                pre_bal = historico[12],
                balance = historico[13],
                inv_value = historico[14],
                store_id = historico[15],
                identification = historico[16],
                user_id_id = historico[17],
                )
    return 'se actualizó el histórico y la bodega'

# Actualiza los valores para recalcular los saldos de bodega desde un inicio a fin 
# dtfDatos: Corresponde al cuadro de datos donde se va a realizar el recalculo de saldos de inventario (pandas.DataFrame)
# Actualiza los saldos y presaldos de ciertos regisros en el histórico de movimientos
def fncRecalculoSaldoPresaldo(dtfDatos):
    intBodega= int(dtfDatos['store'].unique()[0])
    intCodigo= int(dtfDatos['product_code'].unique()[0])
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
    strActualiza= 'UPDATE Historical_Movement SET pre_bal= ?, balance= ? WHERE store= ? AND product_code= ? AND doc_number= ?'
    for j, val in enumerate(lstDocumentos):
        fncConsultalst(strActualiza, [lstPreSaldo[j], lstSaldo[j], intBodega, intCodigo, lstDocumentos[j]])
    strEstado= 'UPDATE Historical_Movement SET condition= ? WHERE doc_number= ?'
    fncConsultalst(strEstado, ['AN' ,lstDocumentos[1]])
    strSaldo= 'UPDATE Store_Inventory_Balance SET inventory_avail= ? WHERE product_code= ? AND batch= ? AND store= ?'
    fncConsultalst(strSaldo, [lstSaldo[- 1], intCodigo, strLote, intBodega])
    return 

# Actualiza el histórico de movimiento y el saldo por bodega cuando se anula un documento transaccional
# strDocumento: Corresponde al documento que se va a anular (str)
# tplColumnasHistorico: Corresponde a la tupla que contiene el nombre de las columnas que contiene la tabla Historico de movimientos
# tuple(str)
# Realiza la actualización de las tablas del histórico de movimiento y de saldo por bodega
def fncActualizaAnulado(strDocumento, tplColumnasHistorico= tplColumnasHistorico):
    strConsultaDocumento= 'SELECT * FROM Historical_Movement WHERE doc_number= ?'
    lstDocumento= fncConsultalst(strConsultaDocumento, [strDocumento])
    if len(lstDocumento)> 1: dtfDocumento= pd.DataFrame(lstDocumento, columns= list(tplColumnasHistorico))
    else: dtfDocumento= pd.DataFrame(np.array(lstDocumento[0]).reshape(- 1, len(list(lstDocumento[0][- 1]))), 
                                     columns= list(tplColumnasHistorico))
    strConsulta= 'SELECT * FROM Historical_Movement WHERE product_Code= ? AND store= ? AND batch= ?'
    lstCodigos= dtfDocumento['product_code'].values.tolist()
    lstBodegas= dtfDocumento['store'].values.tolist()
    lstLotes= dtfDocumento['batch'].values.tolist()
    lstConsultas= [fncConsultalst(strConsulta, [lstCodigos[i], lstBodegas[i], lstLotes[i]]) for i, val in enumerate(lstCodigos)]
    lstIndices= [j for i, lst in enumerate(lstConsultas) for j, val in enumerate(lst) if strDocumento in val]
    lstConsultaFiltrada= [lstConsultas[i][lstIndices[i]- 1: ] for i, j in enumerate(lstConsultas)]
    lstATrabajar= [pd.DataFrame(lst, columns= list(tplColumnasHistorico)) for i, lst in enumerate(lstConsultaFiltrada)]    
    for i in lstATrabajar:
        fncRecalculoSaldoPresaldo(i)
    return