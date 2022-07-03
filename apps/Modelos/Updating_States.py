import numpy as np
from apps.Modelos.Several_func import fncConsultalst

# Actualiza el estado del crédido (credit_state) en la tabla de datos correspondiente al documento que recibe el pago
# strNombreDocumento: Corresponde al documento a actualizar (str)
# strNumeroDocumento: Corresponde al número de id del documento (str)
# fltValorPagado: Corresponde al valor a pagar a el documento (float)
def fncActualizaEstadoCreditoPagos(strNombreDocumento, strNumeroDocumento, fltValorPagado):
    lstNombreDocumento= [strNombreDocumento== 'Ingreso_de_almacén', strNombreDocumento== 'Salida_de_almacén']
    lstTablasDocumentos= ['modulo_configuracion_clsentradasalmacenmdl', 'modulo_configuracion_clssalidasalmacenmdl']
    strConsulta= f'''SELECT total_amount, value_paid FROM {np.select(lstNombreDocumento, lstTablasDocumentos)[()]} 
    WHERE doc_number= %s'''
    lstConsulta= fncConsultalst(strConsulta, [strNumeroDocumento])
    fltNuevoValorPagado= fltValorPagado+ lstConsulta[0][1]
    if lstConsulta[0][0]> fltNuevoValorPagado: strNuevoEstado= 'NC'
    elif lstConsulta[0][0]== fltNuevoValorPagado: strNuevoEstado= 'CA'
    else: strNuevoEstado= 'CS'
    strActualiza= f'''UPDATE {np.select(lstNombreDocumento, lstTablasDocumentos)[()]} SET value_paid= %s, credit_state= %s WHERE 
    doc_number= %s'''
    fncConsultalst(strActualiza, [fltNuevoValorPagado, strNuevoEstado, strNumeroDocumento])
    return 

# Actualiza el estado de crédito (credit_state) en la tabla de datos correspondiente al documento al que se 
# realiza devolución
# strNombreDocumento: Corresponde al nombre del documento de devolución que se creo (str)
# strNumeroDocumento: Corresponde al número de id del documento a actualizar según la devolución (str)
# fltTotalDevolucion: Corresponde al valor total de la devolución (float)
def fncActualizaEstadoCreditoDevolucion(strNombreDocumento, strNumeroDocumento, fltTotalDevolucion):
    lstNombreDocumento= [strNombreDocumento== 'Devolución_a_proveedor', strNombreDocumento== 'Devolución_de_cliente']
    lstTablasDocumentos= ['modulo_configuracion_clsentradasalmacenmdl', 'modulo_configuracion_clssalidasalmacenmdl']
    strConsulta= f'''SELECT total_amount, value_paid, credit_state FROM {np.select(lstNombreDocumento, 
    lstTablasDocumentos)[()]} WHERE doc_number= %s'''
    lstConsulta= fncConsultalst(strConsulta, [strNumeroDocumento])
    if lstConsulta[0][2]== 'NC':
        if fltTotalDevolucion< lstConsulta[0][0]- lstConsulta[0][1]: strNuevoEstado= 'NC'
        elif fltTotalDevolucion== lstConsulta[0][0]- lstConsulta[0][1]: strNuevoEstado= 'CA'
        else: strNuevoEstado= 'CS'
    else: strNuevoEstado= 'CS'
    strActualiza= f'''UPDATE {np.select(lstNombreDocumento, lstTablasDocumentos)[()]} SET credit_state= %s WHERE 
    doc_number= %s'''
    fncConsultalst(strActualiza, [strNuevoEstado, strNumeroDocumento])
    return

# Actualiza la condición del documento en la tabla respectiva cuando esté se anula
# strNombreDocumento: Corresponde al nombre del documento anulado (str)
# strNumeroDocumento: Corresponde al número de id del documento anulado (str)
def fncActualizaCondicionAnulado(strNombreDocumento, strNumeroDocumento):
    lstNombreDocumento= [strNombreDocumento== 'Ingreso_de_almacén', strNombreDocumento== 'Devolución_a_proveedor', 
    strNombreDocumento== 'Salida_de_almacén', strNombreDocumento== 'Devolución_de_cliente', 
    strNombreDocumento== 'Obsequio', strNombreDocumento== 'Ajuste_De_Inventario', strNombreDocumento== 'Traslado']
    lstTablasDocumentos= ['modulo_configuracion_clsentradasalmacenmdl', 'modulo_configuracion_clsdevolucionesproveedormdl',
    'modulo_configuracion_clssalidasalmacenmdl', 'modulo_configuracion_clsdevolucionesclientemdl', 
    'modulo_configuracion_clsobsequiosmdl', 'modulo_configuracion_clsajusteinventariomdl', 
    'modulo_configuracion_clstrasladosbodegasmdl']
    strConsulta= f'''UPDATE {np.select(lstNombreDocumento, lstTablasDocumentos, 'NA')[()]} SET condition= %s 
    WHERE doc_number= %s'''
    fncConsultalst(strConsulta, ['AN' ,strNumeroDocumento])
    return