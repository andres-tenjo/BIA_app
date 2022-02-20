import numpy as np
from numpy.lib.function_base import average
import pandas as pd
import datetime as dt
import sqlite3
from scipy.linalg.special_matrices import invpascal
import datetime as dt

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
    intTotalDias= intTamaño* 31
    lstFechas= [dt.datetime.strptime(str(dtfDatos['Fecha de creación'].max()), 
                                     '%Y-%m-%d %H:%M:%S').date()- dt.timedelta(days= i) for i in range(intTotalDias)]
    dtfCortado= pd.concat([dtfDatos.loc[dtfDatos['Fecha de creación']== dt.datetime.strptime(str(i), '%Y-%m-%d')]\
                           for i in lstFechas])
    return dtfCortado

            
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
        dtfDatos= dtfDatos.groupby(['Product_Code', pd.Grouper(key= strNombreColumnaFecha, freq= strFrecuencia)])\
            .agg({strNombreColumnaValor: [strFuncion]}).reset_index()
        dtfDatos= pd.concat([fncNumeroPeriodosdtf(dtfDatos.loc[dtfDatos['Product_Code']== i], 
                                                  strNombreColumnaFecha, strNombreColumnaValor, strFrecuencia)\
                             for i in dtfDatos['Product_Code'].unique()])
        dtfDatos['Product_Code']= dtfDatos['Product_Code'].astype(int)
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
def fncValidaAjustebol(dtfSaldosBodega, intCodigoProducto, intBodega, strLote, intCantidad, bolTipoAjuste= False):
    dtfSaldoProducto= dtfSaldosBodega.loc[(dtfSaldosBodega['product_code']== intCodigoProducto)\
                                          & (dtfSaldosBodega['batch']== strLote) & (dtfSaldosBodega['store']== intBodega)]
    if dtfSaldoProducto.empty: 
        if (dtfSaldoProducto.empty) & (bolTipoAjuste== False): return False
        else: return True
    else:
        if bolTipoAjuste== False:
            if int(dtfSaldoProducto.iloc[0]['inventory_avail'])- int(intCantidad)< 0: return False
            else: return True
        else: return True

# Conecta con la base de datos sqlite3 y ejecuta una consulta específica
# strConsulta: Es la consulta a realizar en la tabla de datos (str)
# varParametro: Es el párametro de consulta en la tabla, puede ser int, dt.datetime, float, str
# Retorna una lista con la información de la consulta realizada (list)
def fncConsultalst(strConsulta, varParametro):
    with sqlite3.connect(r'C:\Users\FULERO\Desktop\Convergencia\BIA\DailyWork\BasesparaCotizador\DDBBactualized.db') as conn:
        sqlite3.register_adapter(np.int64, lambda val: int(val))
        sqlite3.register_adapter(np.int32, lambda val: int(val))
        crs= conn.cursor()
        try:
            lstConsulta= crs.execute(strConsulta, varParametro).fetchall()
            conn.commit()
            return lstConsulta
        except:
            return 'No existe tabla de datos'

# Conecta con la base de datos sqlite3 sin realizar ningúna consulta
def fncConecta():
    conn= sqlite3.connect(r'C:\Users\FULERO\Desktop\Convergencia\BIA\DailyWork\BasesparaCotizador\DDBBactualized.db')
    sqlite3.register_adapter(np.int64, lambda val: int(val))
    sqlite3.register_adapter(np.int32, lambda val: int(val))
    return conn
    
# Análiza si para una fecha específica existen rangos de horario disponibles
# strFechaConsulta: Corresponde a la fecha en la que el usuario desea asignar una actividad (datetime.datetime)
# strNombreTabla: Corresponde al nombre de la tabla en donde se almacenan las actividades (str)
# intUsuario: Corresponde al código de identificacion del usuario que hace la consuta (int)
# intDuracionTarea: Corresponde al tiempo de duración de la tarea en minutos, (int)
# Retorna una tupla con una cadena de texto según el evento y con una lista de textos tuple(str, list(str))
def fncDisponibilidadHorariotpl(strFechaConsulta, strNombreTabla, intUsuario, intDuracionTarea):
    strConsulta= 'SELECT * FROM '+strNombreTabla+' WHERE Task_Date= ? AND User_ID= ?'
    varParametro= [strFechaConsulta, intUsuario]
    lstTareasFecha= fncConsultalst(strConsulta, varParametro)
    if (lstTareasFecha== 'No existe tabla de datos') | (len(lstTareasFecha)== 0): return 'Todos los horarios disponibles',
    else: 
        lstHorariosInicio= [dt.datetime.strptime(i[1][: 11]+' '+i[2], '%Y-%m-%d %H:%M' )\
                            for i in lstTareasFecha]
        lstHorariosFin= [dt.datetime.strptime(i[1][: 11]+' '+i[3], '%Y-%m-%d %H:%M' )\
                          for i in lstTareasFecha]
        datInicioFecha=dt.datetime.strptime(lstTareasFecha[0][1], '%Y-%m-%d %H:%M:%S').replace(hour= 0, minute= 0, second= 0)
        datFinFecha= datInicioFecha.replace(hour= 23, minute= 59, second= 59)
        lstRangoHorario= [int((lstHorariosInicio[0]- datInicioFecha).seconds/ 60)]
        lstPosibleHorario= [(datInicioFecha.strftime('%Y-%m-%d %H:%M')[11: ], lstHorariosInicio[0].strftime('%Y-%m-%d %H:%M')[11: ])]
        if len(lstHorariosInicio)> 1:
            for i in range(0, len(lstHorariosInicio)):
                if (i< len(lstHorariosInicio)- 1):
                    lstRangoHorario.append(int((lstHorariosInicio[i+ 1]- lstHorariosFin[i]).seconds/ 60))
                    lstPosibleHorario.append((lstHorariosFin[i].strftime('%Y-%m-%d %H:%M')[11: ], 
                                         lstHorariosInicio[i+ 1].strftime('%Y-%m-%d %H:%M')[11: ]))
                else: pass
            lstRangoHorario.append(int((datFinFecha- lstHorariosFin[- 1]).seconds/ 60))
            lstPosibleHorario.append((lstHorariosFin[- 1].strftime('%Y-%m-%d %H:%M')[11: ], 
                                      datFinFecha.strftime('%Y-%m-%d %H:%M')[11: ]))
        else:
            lstRangoHorario.append(int((datFinFecha- lstHorariosFin[- 1]).seconds/ 60))
            lstPosibleHorario.append((lstHorariosFin[- 1].strftime('%Y-%m-%d %H:%M')[11: ], 
                                      datFinFecha.strftime('%Y-%m-%d %H:%M')[11: ]))
        lstValidacion= [True if i/ intDuracionTarea>= 1 else False for i in lstRangoHorario]
        lstHorarioDisponible= [lstPosibleHorario[i] for i in range(0, len(lstValidacion)) if lstValidacion[i]== True]
        if len(lstHorarioDisponible)== 0: return 'No hay horario disponible', lstHorarioDisponible
        else: return 'Horarios disponibles', lstHorarioDisponible


# Convierte una columna de un cuadro de datos al tipo objeto fecha (datetime.datetime)
# dtfDatos: Cuadro de datos en donde se encuentra la columna a modificar el formato (pandas.DataFrame)
# strNombreColumna: Nombre de la columna a la cual se le dará formato fecha (str)
# Retorna el cuadro de datos con la columna modificada (pandas.DataFrame)
def fncFormatoFechadtf(dtfDatos, strNombreColumna):
    dtfDatos[strNombreColumna]= pd.to_datetime(dtfDatos[strNombreColumna], format= '%Y-%m-%d')
    return dtfDatos
'''-------------------------------------------------------------------------------------------------------------------------------''' 
# Función para importar de sqlite3 la base de datos de los movimientos históricos (¿TEMPORAL': Verificar en la integración)
# dfname: Listado con el nombre de las bases de datos a importar (list)
def data_consulting(dfname):    
     conn= sqlite3.connect(r'C:\Users\FULERO\Desktop\Convergencia\BIA\DailyWork\BasesparaCotizador\DDBBactualized.db')
     if len(dfname)> 1: df_list= [pd.read_sql_query(f'SELECT * FROM {i}', conn) for i in dfname]
     else: df_list= pd.read_sql_query(f'SELECT * FROM {dfname[0]}', conn)
     conn.commit()
     return df_list
    
# Función para incluir las fechas en días que no están dentro del cuadro de datos
# df: Cuadro de datos al cual se le van a incluir los días    
def complete_days(df):
     numdays= (df['Creation_Date'].max()- df['Creation_Date'].min()).days
     cdays= [df['Creation_Date'].min()+ dt.timedelta(days= i) for i in range(numdays+ 1)]
     datedf= pd.DataFrame({'Creation_Date': cdays}, index= [i for i in range(0, len(cdays))])
     ndf= datedf.merge(df, how= 'outer', on= 'Creation_Date')
     ndf['Product_Code']= ndf['Product_Code'].fillna(method= 'ffill')
     ndf['value']= ndf['value'].fillna(0)
     return ndf
 
# Confirma si una base de datos es consecutiva cronológicamente con la fecha actual
# dtfDatos: Corresponde al cuadro de datos que se desea cortar (pandas.DataFrame)
# Retorna un valor booleano confirmando si hay continuidad (True Continuidad, False lo contrario) (bool)
def fncFechaConsecutivabol(dtfDatos):
    datUltimo= dtfDatos['Fecha de creación'].max().month
    datActual= dt.datetime.now().month
    if (datUltimo== datActual) | (datActual- 1== datUltimo): return True
    else: return False