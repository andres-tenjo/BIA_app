import numpy as np
import pandas as pd
import datetime as dt
from collections import defaultdict
from django.db import connection
import sqlite3
from django.db import transaction
from apps.modulo_configuracion.models import *

# Convierte una columna de un cuadro de datos al tipo objeto fecha (datetime.datetime)
# dtfDatos: Cuadro de datos en donde se encuentra la columna a modificar el formato (pandas.DataFrame)
# strNombreColumna: Nombre de la columna a la cual se le dará formato fecha (str)
# Retorna el cuadro de datos con la columna modificada (pandas.DataFrame)
def fncFormatoFechadtf(dtfDatos, strNombreColumna):
    pd.options.mode.chained_assignment= None
    dtfDatos[strNombreColumna]= pd.to_datetime(dtfDatos[strNombreColumna], format= '%Y-%m-%d')
    return dtfDatos

# Elimina los valores de 0 de la lista de entrada
# lstLista: Es la lista a la cual se le van a eliminar los ceros (list)
# Retorna una lista sin ceros (list)
def fncEliminaCerolst(lstLista):
     if 0 in lstLista:               
          if lstLista.count(0)> 1:
               return  fncEliminaCerolst(lstLista[lstLista.index(0)+ 1: ])
          else:
               return lstLista[lstLista.index(0)+ 1: ]
     else:
          return lstLista

# Valida si la tabla de datos se encuentra en el rango ingresado de parámetros
# dtfDatos: Es el cuadro de datos para la validación de períodos (pd.DataFrame)
# intMinimo: Valor mínimo del rango (int)
# intMaximo: Valor máximo del rango (int)
# Retorna un texto que indica si la lista no es mayor al valor mínimo del rango (Incomplete), si está dentro del rango (Complete)
# o si es mayor al rango ('Bigger) (str)
def fncRangoPeriodosstr(dtfDatos, intMinimo, intMaximo):
     if not dtfDatos.empty:
          lstPeriodos= list(dtfDatos['Periods'])
          lstValidacion= []
          for i, val in enumerate(lstPeriodos):
               if i< len(lstPeriodos)- 1:
                    if lstPeriodos[i]== lstPeriodos[i+ 1]- 1:
                         lstValidacion.append(lstPeriodos[i])
                    else:
                         lstValidacion.append(lstPeriodos[i])
                         lstValidacion.append(0)
               else:
                    lstValidacion.append(lstPeriodos[i])
          lstFinal= fncEliminaCerolst(lstValidacion)
          return np.where(len(lstFinal)>= intMinimo, np.where(len(lstFinal)<= intMaximo, 'Complete', 'Bigger'), 'Incomplete')
     else:
          return 'Empty'          

# Corta el cuadro de datos según el tamaño en meses especificado
# dtfDatos: Corresponde al cuadro de datos que se desea cortar (pandas.DataFrame)
# intTamaño: Corresponde al tamaño en meses al que se desea reducir el cuadro de datos (int)
# Retorma el cuadro de datos recortado al tamaño de meses específicado (pandas.DataFrame)
def fncCortaCuadrodtf(dtfDatos, intTamaño):
    intTotalDias= int(round(intTamaño* 30.36, 0))
    lstFechas= [dt.datetime.strptime(str(dtfDatos['creation_date'].max()), '%Y-%m-%d %H:%M:%S')- dt.timedelta(days= i)\
        for i in range(intTotalDias)]
    dtfCortado= pd.concat([dtfDatos.loc[dtfDatos['creation_date']== i] for i in lstFechas])
    return dtfCortado

# Confirma si una base de datos es consecutiva cronológicamente con la fecha actual
# dtfDatos: Corresponde al cuadro de datos que se desea cortar (pandas.DataFrame)
# Retorna un valor booleano confirmando si hay continuidad (True Continuidad, False lo contrario) (bool)
def fncFechaConsecutivabol(dtfDatos):
    datUltimo= dtfDatos['creation_date'].max().month
    datActual= dt.datetime.now().month
    if (datUltimo== datActual) | (datActual- 1== datUltimo) | (datUltimo- 1== datActual): return True
    else: return False

# Función que según la frecuencia de tiempo de un cuadro de datos, asigna los períodos por fila en el cuadro de datos
# dtfDatos: Es el cuadro de datos al que se le van a incluir los períodos (pd.DataFrame)
# strNombreColumnaFecha: Cadena de texto que corresponde al nombre de la columna que contiene el registro de la fecha (str)
# strNombreColumnaValor: Cadena de texto que corresponde al nombre de la columna que contiene el registro de los valores (str)
# strFrecuencia: Cadena de texto que corresponde a la frecuencia en que están registrados los datos (str)
# Retorna un cuadro de datos organizado por fecha y por períodos (pd.DataFrame)
def fncNumeroPeriodosdtf(dtfDatos, strNombreColumnaFecha, strNombreColumnaValor, strFrecuencia):
    lstOpciones= [strFrecuencia== 'W', strFrecuencia== 'SM', strFrecuencia== 'M', strFrecuencia== '2M',
        strFrecuencia== 'Q', strFrecuencia== '6M']
    lstDecisiones= [(7, 8), (13, 17), (28, 32), (59, 63), (91, 93), (181, 185)]
    lstPromedio= [7, 15.2, 30.36, 60.83, 91.66, 182.5]
    dtfDatos= dtfDatos.sort_values(by= [strNombreColumnaFecha])
    lstFechas= list(dtfDatos[strNombreColumnaFecha])
    lstPeriodos= []
    for i, val in enumerate(lstFechas):
         if i== 0: lstPeriodos.append(i+ 1)
         else:
             if np.select(lstOpciones, lstDecisiones, (365, 366))[0]<=\
                 (lstFechas[i]- lstFechas[i- 1]).days< np.select(lstOpciones, lstDecisiones, (365, 366))[1]: 
                 lstPeriodos.append(int(lstPeriodos[i- 1]+ 1))
             else:
                 lstPeriodos.append(
                     int(lstPeriodos[i- 1]+ (lstFechas[i]- lstFechas[i- 1]).days/ np.select(lstOpciones, lstPromedio, 365)))          
    dtfDatos= dtfDatos.assign(Periods= lstPeriodos)
    dtfDatos= dtfDatos.rename(columns= {strNombreColumnaValor: 'value'})
    dtfDatos= dtfDatos.set_index(strNombreColumnaFecha)
    if dtfDatos.columns.nlevels> 1: dtfDatos.columns= dtfDatos.columns.droplevel(1)
    else:  pass
    return dtfDatos        
            
# Realiza el proceso de agrupamiento para una tabla de datos de acuerdo a una frecuencia y una función específica    
# dtfDatos: Es el cuadro de datos que se desea agrupar (pd.DataFrame)
# strFrecuencia: Cadena de texto que corresponde a la frecuencia en que están registrados los datos (str)
# bolAgrupaProd: Indica si se debe tener en cuenta en la agrupación o no a los productos (bool)
# strNombreColumnaValor: Cadena de texto que corresponde al nombre de la columna que contiene el registro de los valores (str)
# strFuncion: Es la operación a realizar sobre la columna de agrupación (column2), pre-establecida la operación de suma (str)
# strNombreColumnaFecha: Cadena de texto que corresponde al nombre de la columna que contiene el registro de la fecha (str)
# bolAgrupaProd: Valor booleano que indica si la agrupación se debe realizar con producto o sin el (bool)
# Retorna la tabla de datos agrupada según la frecuencia deseada y con la función deseada, incluyendo columna de período 
# (pandas.DataFrame)
def fncAgrupadtf(dtfDatos, strFrecuencia, strNombreColumnaValor, strFuncion, strNombreColumnaFecha, bolAgrupaProd= False):
    if bolAgrupaProd== True:
        dtfDatos= dtfDatos.groupby(['product_code', pd.Grouper(key= strNombreColumnaFecha, freq= strFrecuencia)])\
            .agg({strNombreColumnaValor: [strFuncion]}).reset_index()
        dtfDatos= pd.concat([fncNumeroPeriodosdtf(dtfDatos.loc[dtfDatos['product_code']== i], 
                                                  strNombreColumnaFecha, strNombreColumnaValor, strFrecuencia)\
                             for i in dtfDatos['product_code'].unique()])
        dtfDatos['product_code']= dtfDatos['product_code'].astype(int)
        return dtfDatos
    else:
        dtfDatos= dtfDatos.groupby([pd.Grouper(key= strNombreColumnaFecha, freq= strFrecuencia)])\
            .agg({strNombreColumnaValor: [strFuncion]}).reset_index()
        return fncNumeroPeriodosdtf(dtfDatos, strNombreColumnaFecha, strNombreColumnaValor, strFrecuencia)

# Organiza la tabla de datos para realizar el pronóstico en Bia
# dtfDatos: Es el cuadro de datos que se desea agrupar (pd.DataFrame)
# strNombreColumnaFecha: Cadena de texto que corresponde al nombre de la columna que contiene el registro de la fecha (str)
# strNombreColumnaValor: Cadena de texto que corresponde al nombre de la columna que contiene el registro de los valores (str)
# strFrecuencia: Cadena de texto que corresponde a la frecuencia en que están registrados los datos (str)
# strFuncion: Es la operación a realizar sobre la columna de agrupación (column2), pre-establecida la operación de suma (str)
# bolAgrupaProd: Indica si se debe tener en cuenta en la agrupación o no a los productos (bool)
# Retorna una tabla de datos organizada con y agrupada (pandas.DataFrame)
def fncOrganizadtf(dtfDatos, strNombreColumnaFecha, strNombreColumnaValor, strFrecuencia, strFuncion, bolAgrupaProd= False):
    dtfDatos= dtfDatos.assign(Format_Date= pd.to_datetime(dtfDatos[strNombreColumnaFecha], format= '%Y-%m-%d'))
    if strFrecuencia== 'W':
         return fncAgrupadtf(dtfDatos, 'W', strNombreColumnaValor, strFuncion, 'Format_Date', bolAgrupaProd= bolAgrupaProd)
    elif strFrecuencia== 'SM':
         return fncAgrupadtf(dtfDatos, 'SM', strNombreColumnaValor, strFuncion, 'Format_Date', bolAgrupaProd= bolAgrupaProd)
    elif strFrecuencia== 'M':
         return fncAgrupadtf(dtfDatos, 'M', strNombreColumnaValor, strFuncion, 'Format_Date', bolAgrupaProd= bolAgrupaProd)
    elif strFrecuencia== '2M':
         return fncAgrupadtf(dtfDatos, '2M', strNombreColumnaValor, strFuncion, 'Format_Date', bolAgrupaProd= bolAgrupaProd)
    elif strFrecuencia== 'Q':
         return fncAgrupadtf(dtfDatos, 'Q', strNombreColumnaValor, strFuncion, 'Format_Date', bolAgrupaProd= bolAgrupaProd)
    elif strFrecuencia== '6M':
         return fncAgrupadtf(dtfDatos, '6M', strNombreColumnaValor, strFuncion, 'Format_Date', bolAgrupaProd= bolAgrupaProd)
    else:
         return fncAgrupadtf(dtfDatos, 'Y', strNombreColumnaValor, strFuncion, 'Format_Date', bolAgrupaProd= bolAgrupaProd)
    
# Valida si un producto se puede debitar o acreditar en una bodega específica y para un lote especifico (si aplica)
# dtfSaldosBodega: Cuadro de datos con los saldos por producto de una bodega específica (pandas.DataFrame)
# intCodigoProducto: Corresponde al código del producto a validar (int)
# bolTipoAjuste: Corresponde al tipo de ajuste a revisar, True= entradas, False= Salidas (bool), pre-establecido False
# strLote: Es el lote del producto, si aplica (str)
# intCantidad: Es la cantidad a ajustar (int)
# Retorna False si el ajuste no se puede realizar, de lo contrario retorna True (bool)
def fncValidaAjustebol(intCodigoProducto, intBodega, strLote, intCantidad, bolTipoAjuste= False):
    strSaldo= '''SELECT inventory_avail FROM modulo_configuracion_clssaldosinventariomdl 
    WHERE product_code_id= %s AND batch= %s AND store_id= %s'''
    lstSaldo= fncConsultalst(strSaldo, [intCodigoProducto, strLote, intBodega])
    if len(lstSaldo)== 0:
        if bolTipoAjuste== False: return False
        else: return True
    else:
        if bolTipoAjuste== False:
            if lstSaldo[0][0]- intCantidad< 0: return False
            else: return True
        else: return True

# Conecta con la base de datos sqlite3 y ejecuta una consulta específica
# strConsulta: Es la consulta a realizar en la tabla de datos (str)
# varParametro: Es el párametro de consulta en la tabla, puede ser int, dt.datetime, float, str
# Retorna una lista con la información de la consulta realizada (list)
def fncConsultalst(strConsulta, varParametro):
    with connection.cursor() as cursor:
        sqlite3.register_adapter(np.int64, lambda val: int(val))
        sqlite3.register_adapter(np.int32, lambda val: int(val))
        lstConsulta= cursor.execute(strConsulta, varParametro).fetchall()
        return lstConsulta
        
# Conecta con la base de datos sqlite3 sin realizar ningúna consulta
def fncConecta():
    with connection.cursor() as cursor:
        sqlite3.register_adapter(np.int64, lambda val: int(val))
        sqlite3.register_adapter(np.int32, lambda val: int(val))
        return cursor
    
# Análiza si para una fecha específica existen rangos de horario disponibles
# datFechaConsulta: Corresponde a la fecha en la que el usuario desea asignar una actividad 
# en el horario en punto de la media noche (datetime.datetime) 
# strNombreTabla: Corresponde al nombre de la tabla en donde se almacenan las actividades (str)
# intUsuario: Corresponde al código de identificacion del usuario que hace la consuta (int)
# intDuracionTarea: Corresponde al tiempo de duración de la tarea en minutos, (int)
# bolSegmento: Valor booleano donde True es antes del medio día y False igual o después del medio día, por defecto True (bool)
# Retorna una tupla con una cadena de texto según el evento y con una lista de textos tuple(str, list(str))
def fncDisponibilidadHorariotpl(datFechaConsulta, strNombreTabla, intUsuario, intDuracionTarea, bolSegmento= True):
    strConsulta= 'SELECT * FROM '+strNombreTabla+' WHERE Task_Date= ? AND User_ID= ?'
    varParametro= [datFechaConsulta, intUsuario]
    lstTareasFecha= fncConsultalst(strConsulta, varParametro)
    if (lstTareasFecha== 'No existe tabla de datos') | (len(lstTareasFecha)== 0): return 'Todos los horarios disponibles',
    else: 
        lstHorariosInicio= [dt.datetime.strptime(i[1][: 11]+' '+i[2], '%Y-%m-%d %H:%M')\
                            for i in lstTareasFecha]
        lstHorariosFin= [dt.datetime.strptime(i[1][: 11]+' '+i[3], '%Y-%m-%d %H:%M')\
                          for i in lstTareasFecha]
        datInicioFecha=dt.datetime.strptime(lstTareasFecha[0][1], '%Y-%m-%d %H:%M:%S').replace(hour= 0, minute= 0, second= 0)
        datMedioDiaFecha= datFechaConsulta.replace(hour= 12, minute= 0, second= 0, microsecond= 0)
        datFinFecha= datInicioFecha.replace(hour= 23, minute= 59, second= 59)
        lstRangoHorario= [int((lstHorariosInicio[0]- dt.timedelta(minutes= 1)- datInicioFecha).seconds/ 60)\
                          if lstHorariosInicio[0]!= datInicioFecha else int((lstHorariosInicio[0] - datInicioFecha).seconds/ 60)]
        lstPosibleHorario= [(datInicioFecha, lstHorariosInicio[0]- dt.timedelta(minutes= 1)\
                             if lstHorariosInicio[0]!= datInicioFecha else lstHorariosInicio[0])]
        if len(lstHorariosInicio)> 1:
            for i in range(0, len(lstHorariosInicio)):
                if (i< len(lstHorariosInicio)- 1):
                    intMinuto= int((lstHorariosInicio[i+ 1]- dt.timedelta(minutes= 2)- lstHorariosFin[i]).seconds/ 60)\
                        if lstHorariosInicio[i+ 1]- dt.timedelta(minutes= 2)>= lstHorariosFin[i]\
                            else int(0)
                    lstRangoHorario.append(intMinuto)
                    lstPosibleHorario.append((lstHorariosFin[i]+ dt.timedelta(minutes= 1), 
                                              lstHorariosInicio[i+ 1]- dt.timedelta(minutes= 1)))
                else: pass
            intMinuto= int((datFinFecha- dt.timedelta(minutes= 1)- lstHorariosFin[- 1]).seconds/ 60)\
                if datFinFecha- dt.timedelta(minutes= 1)>= lstHorariosFin[- 1] else int(0)
            lstRangoHorario.append(intMinuto)
            lstPosibleHorario.append((lstHorariosFin[- 1]+ dt.timedelta(minutes= 1), datFinFecha))
        else:
            intMinuto= int((datFinFecha- dt.timedelta(minutes= 1)- lstHorariosFin[- 1]).seconds/ 60)\
                if datFinFecha- dt.timedelta(minutes= 1)>= lstHorariosFin[- 1] else int(0)
            lstRangoHorario.append(intMinuto)
            lstPosibleHorario.append((lstHorariosFin[- 1]+ dt.timedelta(minutes= 1), datFinFecha))
        lstValidacion= [True if i/ intDuracionTarea>= 1 else False for i in lstRangoHorario]
        lstHorarioDisponible= [lstPosibleHorario[i] for i in range(0, len(lstValidacion)) if lstValidacion[i]== True]
        if len(lstHorarioDisponible)== 0: return 'No hay horario disponible', lstHorarioDisponible
        else:
            lstValidacionMediodia= []
            for i in lstHorarioDisponible:
                intMinutos= int((i[1]- i[0]).seconds/ 60)
                lstRango= [i[0]+ dt.timedelta(minutes= j) for j in range(0, intMinutos+ 1)]
                lstValidacionMediodia.append(lstRango)
            lstMedioDia= [(i, j) for i, j in enumerate(lstValidacionMediodia) if datMedioDiaFecha in j]
            if len(lstMedioDia)!= 0:
                lstCorte= [(lstMedioDia[0][1][0], lstMedioDia[0][1][i]) for i in range(0, len(lstMedioDia[0][1]))\
                           if lstMedioDia[0][1][i]== datMedioDiaFecha- dt.timedelta(minutes= 1)]
                lstHorarioDisponible= lstHorarioDisponible[: lstMedioDia[0][0]]+ lstCorte+ [(datMedioDiaFecha, lstMedioDia[0][1][- 1])]\
                    + lstHorarioDisponible[lstMedioDia[0][0]+ 1: ]
                lstDisponibilidadMañana= [(i[0].strftime('%Y-%m-%d %I:%M %p')[11: ], i[1].strftime('%Y-%m-%d %I:%M %p')[11: ])\
                                          for i in lstHorarioDisponible if (datInicioFecha<= i[0] < datMedioDiaFecha) &\
                                              (datInicioFecha<= i[1] < datMedioDiaFecha)]
                lstDisponibilidadTarde= [(i[0].strftime('%Y-%m-%d %I:%M %p')[11: ], i[1].strftime('%Y-%m-%d %I:%M %p')[11: ])\
                                         for i in lstHorarioDisponible if (datMedioDiaFecha<= i[0] < datFinFecha) &\
                                             (datMedioDiaFecha<= i[1] <= datFinFecha)]
            else:
                lstDisponibilidadMañana= [(i[0].strftime('%Y-%m-%d %I:%M %p')[11: ], i[1].strftime('%Y-%m-%d %I:%M %p')[11: ])\
                                          for i in lstHorarioDisponible if (datInicioFecha<= i[0] < datMedioDiaFecha) &\
                                              (datInicioFecha<= i[1] < datMedioDiaFecha)]
                lstDisponibilidadTarde= [(i[0].strftime('%Y-%m-%d %I:%M %p')[11: ], i[1].strftime('%Y-%m-%d %I:%M %p')[11: ])\
                                         for i in lstHorarioDisponible if (datMedioDiaFecha<= i[0] <= datFinFecha) &\
                                             (datMedioDiaFecha<= i[1] <= datFinFecha)]
            if bolSegmento== True: return 'Horarios disponibles', lstDisponibilidadMañana
            else: return 'Horarios disponibles', lstDisponibilidadTarde

# Evita que el usuario ingrese un horario no disponible en los rangos recibidos
# datFechaConsulta: Corresponde a la fecha en la que el usuario desea asignar una actividad 
# en el horario en punto de la media noche (datetime.datetime) 
# lstHorarioDisponible: Corresponde a lista que contiene los rangos horarios disponibles para ingresar una tarea (list)
# intDuracionTarea: Corresponde al tiempo de duración de la tarea en minutos, (int)
# strHorarioSeleccion: Corresponde al horario seleccionado por el usuario para iniciar la tarea (str)
# Retorna un booleano donde True indica que el horario seleccionado puede ser ingresado como hora inicial y False lo contrario (bool)
def fncHoraIniciobol(datFechaConsulta, lstHorarioDisponible, intDuracionTarea, strHorarioSeleccion):
    datFecha= datFechaConsulta.strftime('%Y-%m-%d %H:%M')[: 11]
    if isinstance(lstHorarioDisponible, list):
        if len(lstHorarioDisponible)== 0: return False
        else:
            lstHorarios= []
            for i in lstHorarioDisponible:
                intMinutos= int((dt.datetime.strptime(datFecha+' '+i[1], '%Y-%m-%d %I:%M %p')\
                                 - dt.datetime.strptime(datFecha+' '+i[0], '%Y-%m-%d %I:%M %p')).seconds/ 60)
                lstRango= [dt.datetime.strptime(datFecha+' '+i[0], '%Y-%m-%d %I:%M %p')+ dt.timedelta(minutes= j)\
                           for j in range(0, (intMinutos+ 1)- intDuracionTarea)]
                lstHoras= [k.strftime('%Y-%m-%d %I:%M %p')[11: ] for k in lstRango]
                lstHorarios.append(lstHoras)
            lstHorariosParaInicio= [i for j in lstHorarios for i in j]
            if strHorarioSeleccion in lstHorariosParaInicio: return True
            else: return False
    else: return False

# Valida si una lista contiene valores repetidos 
# lstValores: Lista que puede contener o no los valores repetidos
# Retorna el valor y el indice dentro de la lista donde se encuentran repetidos los valores (tuple)
def fncDuplicadoListatpl(lstValores):
    dctLista= defaultdict(list)
    for i, j in enumerate(lstValores): dctLista[j].append(i)
    return ((i, j) for (i, j) in dctLista.items() if len(j)> 1)    

# Función para importar de sqlite3 la base de datos de los movimientos históricos (¿TEMPORAL': Verificar en la integración)
# lstNombreTabla: Listado con el nombre de las bases de datos a importar (list)
# Retorna una lista con el (los) cuadro(s) de dato(s) solicitados
def fncCuadroConsultalst(lstNombreTabla):    
    if len(lstNombreTabla)> 1: lstDatos= [pd.read_sql_query(f'SELECT * FROM {i}', connection) for i in lstNombreTabla]
    else: lstDatos= pd.read_sql_query(f'SELECT * FROM {lstNombreTabla[0]}', connection)
    return lstDatos

# Entrega al última posición de una llave primaria de una tabla de datos específica
# strNombreTabla: Corresponde al nombre de la tabla que se va a consultar (str)
# Retorna un entero con el consecutivo de la llave primaria de la tabla (int)
def fncLlavePrimariaint(strNombreTabla):
    strConsultaLlave= f'SELECT id FROM {strNombreTabla}'
    lstConsultaLlave= fncConsultalst(strConsultaLlave, [])
    if isinstance(lstConsultaLlave, list):
        if len(lstConsultaLlave)== 0: return 1
        else: return int(max([i[0] for i in lstConsultaLlave])+ 1)
    else: 'No existe la tabla de datos'

# Actualiza el valor del costo por unidad de compra del producto en el catálogo de productos
# dtfDatos: Corresponde al cuadro de datos de la entrada a almacén (pandas.DataFrame)
# Actualiza el valor de la columna costo por unidad de compra
def fncActualizaCostoPU(dtfDatos):
    dtfDatos= dtfDatos.reset_index()
    dtfDatos.drop(['index'], axis= 1, inplace= True)
    for i, val in enumerate(dtfDatos['product_code'].unique()):
        strCatalogo= 'SELECT split FROM modulo_configuracion_clscatalogoproductosmdl WHERE id= %s'
        lstCatalogo= fncConsultalst(strCatalogo, [val])
        fltNuevoCosto= float(dtfDatos.iloc[i]['unitary_cost'])* int(lstCatalogo[0][0])
        strActualiza= 'UPDATE modulo_configuracion_clscatalogoproductosmdl SET cost_pu= %s WHERE id= %s'
        lstActualiza= fncConsultalst(strActualiza, [float(fltNuevoCosto), val])
    print('Se actualizó el costo por unidad de compra')
    return


######### Función para realizar pruebas ########
def creapedido(intProducto):
    with transaction.atomic():
        qrsConsulta = clsPedidosMdl()
        qrsConsulta.identification= clsCatalogoClientesMdl.objects.get(pk= 3)
        qrsConsulta.delivery_date= dt.datetime.now()
        qrsConsulta.subtotal= 100.0
        qrsConsulta.iva= 19
        qrsConsulta.discount= 0.0
        qrsConsulta.total= 119.0
        qrsConsulta.observations= 'Sin observación'
        qrsConsulta.store= clsCatalogoBodegasMdl.objects.get(id= 1)
        qrsConsulta.condition= 'AB'
        qrsConsulta.save()
        qrsDetalle = clsDetallePedidosMdl()
        qrsDetalle.doc_number = clsPedidosMdl.objects.get(id= 5)
        qrsDetalle.product_code = clsCatalogoProductosMdl.objects.get(id= intProducto)
        qrsDetalle.quantity = 1
        qrsDetalle.unit_price= 100
        qrsDetalle.subtotal= 100
        qrsDetalle.iva = 19
        qrsDetalle.total= 119
        qrsDetalle.save()
        print('Se creo registro')

def creaordencompra(intProducto):
    with transaction.atomic():
        qrsConsulta = clsOrdenesCompraMdl()
        qrsConsulta.identification= clsCatalogoProveedoresMdl.objects.get(pk= 1)
        qrsConsulta.delivery_date= dt.datetime.now()
        qrsConsulta.subtotal= 100.0
        qrsConsulta.iva= 19
        qrsConsulta.discount= 0.0
        qrsConsulta.total= 119.0
        qrsConsulta.observations= 'Sin observación'
        qrsConsulta.store= clsCatalogoBodegasMdl.objects.get(id= 1)
        qrsConsulta.condition= 'AB'
        qrsConsulta.save()
        qrsDetalle = clsDetalleOrdenesCompraMdl()
        qrsDetalle.doc_number = clsOrdenesCompraMdl.objects.get(id= 1)
        qrsDetalle.product_code = clsCatalogoProductosMdl.objects.get(id= intProducto)
        qrsDetalle.quantity = 1
        qrsDetalle.unit_price= 100
        qrsDetalle.subtotal= 100
        qrsDetalle.iva = 19
        qrsDetalle.total= 119
        qrsDetalle.save()
        print('Se creo registro')

def creacotizacion(intProducto):
    with transaction.atomic():
        qrsConsulta= clsCotizacionesMdl()
        qrsConsulta.identification= clsCatalogoClientesMdl.objects.get(pk= 3)
        qrsConsulta.condition= 'AB'
        qrsConsulta.city= clsCiudadesMdl.objects.get(pk= 1)
        qrsConsulta.store= clsCatalogoBodegasMdl.objects.get(pk= 1)
        qrsConsulta.freight= 0.7
        qrsConsulta.general_obs= 'Sin Observación'
        qrsConsulta.follow_up_date= dt.datetime(2022, 5, 30)
        qrsConsulta.save()
        qrsDetalle= clsDetalleCotizacionesMdl()
        qrsDetalle.doc_number= clsCotizacionesMdl.objects.get(id= 2)
        qrsDetalle.product_code= clsCatalogoProductosMdl.objects.get(id= intProducto)
        qrsDetalle.quantity= 1
        qrsDetalle.lead_time= 3
        qrsDetalle.unit_price= 100.0
        qrsDetalle.due_date= dt.datetime(2023, 1, 1)
        qrsDetalle.observations= 'sin Observación'
        qrsDetalle.save()

def crealistaprecios(intProducto):
    with transaction.atomic():
        qrsConsulta= clsListaPreciosMdl()
        qrsConsulta.list_name= 'Fabrifolder'
        qrsConsulta.crossing_doc= 'prueba'
        qrsConsulta.store= clsCatalogoBodegasMdl.objects.get(pk= 1)
        qrsConsulta.freight= 0.6
        qrsConsulta.state= 'AB'
        qrsConsulta.save()
        qrsDetalle= clsDetalleListaPreciosMdl()
        qrsDetalle.doc_number= clsListaPreciosMdl.objects.get(pk= 1)
        qrsDetalle.product_code= clsCatalogoProductosMdl.objects.get(id= intProducto)
        qrsDetalle.quantity= 1
        qrsDetalle.lead_time= 3
        qrsDetalle.unit_price= 100.0
        qrsDetalle.due_date= dt.datetime(2023, 1, 1)
        qrsDetalle.observations= 'sin Observación'
        qrsDetalle.save()

def creasalida(intCliente):
    with transaction.atomic():
        qrsConsulta= clsSalidasAlmacenMdl()
        qrsConsulta.identification= clsCatalogoClientesMdl.objects.get(pk= intCliente)
        qrsConsulta.discount= 0.0
        qrsConsulta.taxes= 19.0
        qrsConsulta.total_price= 100
        qrsConsulta.total_amount= 119
        qrsConsulta.total_cost= 90
        qrsConsulta.value_paid= 100
        qrsConsulta.credit_state= 'NC'
        qrsConsulta.store= clsCatalogoBodegasMdl.objects.get(pk= 1)
        qrsConsulta.crossing_doc= 'Prueba'
        qrsConsulta.condition= 'CE'
        qrsConsulta.save()
        qrsDetalle= clsDetalleSalidasAlmacenMdl()
        qrsDetalle.doc_number= clsSalidasAlmacenMdl.objects.get(pk= 1)
        qrsDetalle.product_code= clsCatalogoProductosMdl.objects.get(pk= 10801)
        qrsDetalle.quantity= 1
        qrsDetalle.unit_price= 100.0
        qrsDetalle.discount= 0.0
        qrsDetalle.taxes= 19
        qrsDetalle.total_price= 119.0
        qrsDetalle.total_amount= 119.0
        qrsDetalle.unitary_cost= 90
        qrsDetalle.total_cost= 90
        qrsDetalle.batch= 'si'
        qrsDetalle.expiration_date= dt.datetime(2023, 1, 30)
        qrsDetalle.state= 'CO'
        qrsDetalle.save()

################################################