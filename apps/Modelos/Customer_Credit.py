# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 19:12:31 2022

@author: FULERO
"""
import pandas as pd
import datetime as dt
from apps.Modelos.Several_func import fncConsultalst, fncFormatoFechadtf

# Calcula los días vencidos para el pago de una factura
# datFechaCreacion: Corresponde a la fecha de creación del documento de salida (dt.datetime)
# intDiasCredito: Corresponde a los días otorgados para pagar una salida (int)
# Retorna los días vencidos que tiene una factura o 0 si no se ha vencido (int)
def fncDiasVencidosint(datFechaCreacion, intDiasCredito):
    datVencimeintoDocumento= datFechaCreacion+ dt.timedelta(days= intDiasCredito)
    intDiasVencidos= (dt.datetime.now()- datVencimeintoDocumento).days
    if intDiasVencidos< 0: return 0
    else: return intDiasVencidos
        
# Cálcula y organiza la información de un cliente con crédito
# intCodigoCliente: Corresponde al código unico del cliente en la base de datos (int)
# Retorna una tupla con el cuadro de datos de la información detallada de las salidas pendientes por pago y el total del cupo
# disponble del cliente (tuple(pandas.DataFrame, float))
def fncClienteCreditotpl(intCodigoCliente):
    tplColumnasSalidas= ('Fecha Creación', 'N° Documento', 'Código Cliente', 'Código Bodega', 'Documento Cruce', 
    'Estado del Crédito', 'Descuento', 'Precio Total', 'Impuestos', 'Valor Total', 'Valor Pagado', 'Código Usuario Creación')
    strConsultaSalidas= '''SELECT creation_date, doc_number, identification_id, store_id, crossing_doc, credit_state, discount,
    total_price, taxes, total_amount, value_paid, user_creation_id FROM modulo_configuracion_clssalidasalmacenmdl 
    WHERE identification_id= %s AND credit_state= %s'''
    varParametroSalida= [intCodigoCliente, 'NC']
    lstSalidas= fncConsultalst(strConsultaSalidas, varParametroSalida)
    if len(lstSalidas)== 0: return 'El cliente no tiene pagos pendientes',
    else: 
        dtfSalidas= pd.DataFrame(lstSalidas, columns= list(tplColumnasSalidas))        
        dtfSalidas= fncFormatoFechadtf(dtfSalidas, 'Fecha Creación')
        strCatalogo= '''SELECT identification, business_name, credit_days, approved_amount 
        FROM modulo_configuracion_clscatalogoclientesmdl WHERE id= %s'''
        lstCatalogo= fncConsultalst(strCatalogo, [intCodigoCliente])
        intIdentificacion, strNombre= int(lstCatalogo[0][0]), lstCatalogo[0][1]
        intDiasCredito= int(lstCatalogo[0][2]) if lstCatalogo[0][2] is not None else 1
        fltCupoAprobado= float(lstCatalogo[0][3])
        dtfFinal= dtfSalidas.assign(amount= dtfSalidas['Valor Total']- dtfSalidas['Valor Pagado'], 
        payday_limit= dtfSalidas['Fecha Creación']+ dt.timedelta(days= intDiasCredito), 
        days_past_due= dtfSalidas.apply(lambda x: fncDiasVencidosint(x['Fecha Creación'], intDiasCredito), axis= 1),
        Identificacion= intIdentificacion, Nombre_Cliente= strNombre)
        fltCupoDisponible= fltCupoAprobado- dtfFinal['amount'].sum()
        dtfFinal= dtfFinal.rename(columns= {'payday_limit': 'Fecha Límite Pago', 'days_past_due': 'Días Vencidos', 
        'Identificacion': 'Identificación', 'Nombre_Cliente': 'Nombre Cliente'}).drop(['amount'], axis= 1)
        return dtfFinal, fltCupoDisponible
        

# Construye un cuadro de datos que lista los clientes que tienen pendienten pagos por realizar, ordenandolos por días vencidos
# Retorna el cuadro de datos con el listado de clientes con que adeudan (pandas.DataFrame)
def fncTablaCarteradtf():
    strConsultaSalidas= 'SELECT identification_id FROM modulo_configuracion_clssalidasalmacenmdl WHERE credit_state= %s'
    varParametrosSalida= ['NC']
    lstSalidas= fncConsultalst(strConsultaSalidas, varParametrosSalida)
    if len(lstSalidas)== 0: return 'No hay clientes con pagos pendientes'
    else:
        lstCodigoCliente= list(set([int(i[0]) for i in lstSalidas]))
        strConsultaCatalogo= '''SELECT identification, business_name, credit_days, approved_amount
        FROM modulo_configuracion_clscatalogoclientesmdl WHERE id= %s'''
        lstCatalogo= [fncConsultalst(strConsultaCatalogo, [i]) for i in lstCodigoCliente] 
        lstClienteCredito= [fncClienteCreditotpl(int(i)) for i in lstCodigoCliente]
        lstIdentificacion= [i[0][0] for i in lstCatalogo]
        lstNombres= [i[0][1] for i in lstCatalogo]
        lstCupos= [i[0][3] for i in lstCatalogo]
        lstDisponible= [i[1] for i in lstClienteCredito]
        lstDiasVencidos= [i[0]['Días Vencidos'].max() for i in lstClienteCredito]
        dtfResultado= pd.DataFrame({'Identificación': lstIdentificacion, 'Cliente': lstNombres, 'Cupo Aprobado': lstCupos, 
        'Cupo Disponible': lstDisponible, 'Días Vencidos': lstDiasVencidos}, index= [i for i in range(0, len(lstCodigoCliente))])
        dtfResultado= dtfResultado.sort_values(by= ['Días Vencidos'], ascending= False)
        return dtfResultado