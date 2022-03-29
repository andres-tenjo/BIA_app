# Python libraries
from datetime import time, date
import datetime as dt
import numpy as np
from pandas import pandas as pd
from collections import defaultdict
import re
from pandas import Timestamp
from apps.Modelos.Several_func import fncConsultalst

# BIA Fields
from apps.modulo_configuracion.api.serializers import *
from apps.modulo_configuracion.models import *
from apps.planeacion.models import *


'''Funciones para las vistas de las ventanas'''

# Función que valida las celdas de un archivo de importación
# dtf: Dataframe de la base de datos que sera evaluada
# strNombreColumna: Nombre de la columna que será evaluada
# tplArchivo: Tupla con las validaciones que se debe hacer por cada celda
def fncValidarImportacionlst(df, colname, val):
    l = []
    if val[0][0] == True:
        t = val[0][1]
        error = 'Tipo de dato'
        values = df[colname].tolist()
        for i in range(0, len(values)):
            if values[i] != 0:
                if t == float:
                    d = float(values[i])
                    if type(d) == t:
                        pass
                    else:
                        l.append((colname, i, error, values[i]))
                elif t == str:
                    e = str(values[i])
                    if type(e) == t:
                        pass
                    else:
                        l.append((colname, i, error, values[i]))
                elif t == int:
                    e = values[i]
                    if type(e) == t:
                        pass
                    else:
                        l.append((colname, i, error, values[i]))
                elif t == 'mail':
                    error = 'No es un correo valido'
                    def val_mail(mail):
                        expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
                        return re.match(expresion_regular, mail) is not None
                    validate = val_mail(values[i])
                    if validate == True:
                        pass
                    else:
                        l.append((colname, i, error, values[i]))
                elif t == time:
                    error = 'No es un formato hora'
                    if type(values[i]) == t:
                        pass
                    else:
                        l.append((colname, i, error, values[i]))
                elif t == Timestamp:
                    error = 'No es un formato fecha'
                    if type(values[i]) == t:
                        pass
                    else:
                        l.append((colname, i, error, values[i]))
                elif t == 'identification':
                    db = val[0][2]
                    error = 'Registro ya existe'
                    values = df[colname].tolist()
                    d = db.objects.all()
                    dtf = d.to_dataframe()
                    d = dtf['identification'].tolist()
                    for i in range(0, len(values)):
                        if values[i] in d:
                            l.append((colname, i, error, values[i]))
                        elif type(values[i]) != int:
                            l.append((colname, i, 'Tipo de dato', values[i]))
                        else:
                            pass
                elif t == 'bar_code':
                    db = val[0][2]
                    error = 'Registro ya existe'
                    values = df[colname].tolist()
                    d = db.objects.all()
                    dtf = d.to_dataframe()
                    d = dtf['bar_code'].tolist()
                    for i in range(0, len(values)):
                        if values[i] in d:
                            l.append((colname, i, error, values[i]))
                        elif type(values[i]) == int:
                            pass
                        elif type(values[i]) == float:
                            pass
                        else:
                            l.append((colname, i, 'Tipo de dato', values[i]))
                elif t == 'product_subcat':
                    db = val[0][2]
                    error = 'Registro ya existe'
                    values = df[colname].tolist()
                    d = db.objects.all()
                    dtf = d.to_dataframe()
                    d = dtf['product_subcat'].tolist()
                    for i in range(0, len(values)):
                        if values[i] in d:
                            l.append((colname, i, error, values[i]))
                        else:
                            pass
                else:
                    pass
            else:
                pass
    if val[1][0] == True:
        lm = val[1][1]
        error = 'Longitud max'
        values = df[colname].tolist()
        for i in range(0, len(values)):
            if values[i] != 0:
                if len(str(values[i])) <= lm:
                    pass
                else:
                    l.append((colname, i, error, values[i]))
            else:
                pass
    if val[2][0] == True:
        lmi = val[2][1]
        error = 'Campo obligatorio'
        values = df[colname].tolist()
        for i in range(0, len(values)):
            if len(str(values[i])) >= lmi:
                pass
            else:
                l.append((colname, i, error, values[i]))
    if val[3][0] == True:
        db = val[3][1]
        error = 'No existe en base de datos'
        values = df[colname].tolist()
        d = db.objects.all()
        d = d.to_dataframe()
        d = d['id'].tolist()
        for i in range(0, len(values)):
            if values[i] in d:
                pass
            else:
                l.append((colname, i, error, values[i]))
    if len(val) > 4:
        if val[4][0] == True:
            t = val[4][1]
            error = 'No es una opción valida, recuerde el uso de mayusculas'
            values = df[colname].tolist()
            for i in range(0, len(values)):
                if len(t) == 2:
                    if values[i] == t[0]:
                        pass
                    elif str(values[i]) == t[1]:
                        pass
                    else:
                        l.append((colname, i, error, values[i]))
                elif len(t) > 2:
                    if values[i] == t[0]:
                        pass
                    elif str(values[i]) == t[1]:
                        pass
                    elif str(values[i]) == t[2]:
                        pass
                    else:
                        l.append((colname, i, error, values[i]))
    return l

# Funciones para agregar columna de validación
# dtf: Dataframe de la base de datos que sera evaluada
# strError: Cadena de texto 'Error' si existe error en la fila o 'Coorrecto' de lo contrario 
def fncAgregarColumnaValidaciondtf(dtf, lst, strError):
    dtf.at[lst, 'Validación'] = strError

# Funciones para agregar errores a la fila
# dtf: Dataframe de la base de datos que sera evaluada
# lstFilasError: Lista de filas con error
def fncAgregarErrorFilastr(dtf, lstFilasError):
    for i in range(0, len(dtf)):
        if i in lstFilasError:
            return 'Error'

# Funciones para agregar error al dataframe evaluado
# dtf: Dataframe de la base de datos que sera evaluada
# lstFilasError: Lista de filas con error
def fncAgregarErroresDataframedtf(dtf, lstValidacion, lstFilasError):
    dtf = dtf.assign(Validación='')
    for i in lstValidacion:
        fncAgregarColumnaValidaciondtf(dtf, i[1], fncAgregarErrorFilastr(dtf, lstFilasError))
    success_row = [ i for i in range(0, len(dtf)) if i not in lstFilasError ]
    for i in success_row:
        fncAgregarColumnaValidaciondtf(dtf, i, 'Correcto')
    return dtf

# Función para ajustar el ancho de las columnas de una hoja de excel writer
# excWritter: Libro de excel writer 
# bolNumeroHojas: True si la hoja del libro no es plantilla (solo columnas) False de lo contrario
# dtf: Dataframe de la hoja que se debe configurar el ancho de la columna
# strNombreHoja: Cadena con el nombre de la hoja que sera configurada
def fncAgregarAnchoColumna(excWriter, bolNumeroHojas, dtf, strNombreHoja):
    if bolNumeroHojas == True:
        for i in dtf:
            intAnchoColumna = max(dtf[i].astype(str).map(len).max(), len(i))
            strColumna = dtf.columns.get_loc(i)
            excWriter.sheets[strNombreHoja].set_column(strColumna, strColumna, intAnchoColumna)
    else:
        for i in dtf:
            intAnchoColumna = len(i)
            strColumna = dtf.columns.get_loc(i)
            excWriter.sheets[strNombreHoja].set_column(strColumna, strColumna, intAnchoColumna)

# Función que agrega comentarios a una celda
# excWritter: Libro de excel writer 
# strHojaExcel: Cadena con el nombre de la hoja que sera configurada
# lstCeldas: Lista con las celdas que llevaran el comentario
# lstComentarios: Lista con los comentarios que llevara cada celda
def fncAgregarComentarioCeldas(excWriter, strHojaExcel, lstCeldas, lstComentarios):
    for i, j in zip(lstCeldas, lstComentarios):
        excWriter.sheets[strHojaExcel].write_comment(str(i), str(j))

# Función que agrega un formato a las celdas que tienen errores
# excWriter: Libro de excel writer 
# lstValidar: Lista con las celdas que se validaron y tuvieron error
# strHojaExcel: Cadena con el nombre de la hoja que sera configurada
# lstNombresColumnas: Lista con el nombre de las columnas
def fncAgregarFormatoColumnasError(excWriter, lstValidar, strHojaExcel, lstNombresColumnas):
    workbook = excWriter.book
    plantilla = excWriter.sheets[strHojaExcel]
    e_type = workbook.add_format({
        'bold': True,
        'fg_color': '#f10a0a',
        })
    for i in lstValidar:
        if i[2] == 'Registro ya existe':
            plantilla.write(i[1] + 1, lstNombresColumnas.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_type)
        elif i[2] == 'Tipo de dato':
            plantilla.write(i[1] + 1, lstNombresColumnas.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_type)
        elif i[2] == 'No es un correo valido':
            plantilla.write(i[1] + 1, lstNombresColumnas.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_type)
        elif i[2] == 'No es un formato hora':
            plantilla.write(i[1] + 1, lstNombresColumnas.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_type)
        elif i[2] == 'No es un formato fecha':
            plantilla.write(i[1] + 1, lstNombresColumnas.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_type)
        elif i[2] == 'Longitud max':
            plantilla.write(i[1]+ 1, lstNombresColumnas.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_type)
        elif i[2] == 'Campo obligatorio':
            plantilla.write(i[1]+ 1, lstNombresColumnas.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_type)
        elif i[2] == 'No existe en base de datos':
            plantilla.write(i[1]+ 1, lstNombresColumnas.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_type)
        elif i[2] == 'No es una opción valida, recuerde el uso de mayusculas':
            plantilla.write(i[1]+ 1, lstNombresColumnas.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_type)
        else: plantilla.write(i[1]+ 1, lstNombresColumnas.index(i[0]), str(i[3]) + ' Error: ' +  i[2], e_type)

# Función que retorna un consulta django en dataframe
# tblDatos: Clase del modelo (tabla de datos) django que se quiere consultar
# srlTabla: Clase que serializa una consulta y la convierte en formato json
# strClave: Nombre de la columna que tiene la clave de relación con otra tabla
# strClave: Nuevo nombre que se asigna a la clave para que posteriormente se pueda unir a la tabla que tiene relación
def fncRetornarDataframe(tblDatos, srlTabla, strClave, strNuevaClave):
    tblDatos = tblDatos.objects.all()
    if tblDatos:
        jsnTabla = srlTabla(tblDatos, many=True)
        dtfTabla = pd.DataFrame(jsnTabla.data)
        dtfTabla = dtfTabla.rename(columns={strClave:strNuevaClave})
    else:
        dtfTabla = tblDatos.to_dataframe()
        dtfTabla = dtfTabla.rename(columns={strClave:strNuevaClave})
    return dtfTabla

# Función que recibe un listado de consultas django y retorna un listado de dataframes
# lstConsultas: Listado con clases de los modelos (tabla de datos) django que se quieren consultar
# lstSerializadores: Listado con clases que serializan las consultas y las convierte en formato json
# lstClaves: Listado con el nombre de la columna que tiene la clave de relación con otra tabla
# lstNuevasClaves: Listado con el nuevo nombre que se asigna a la clave para que posteriormente se pueda unir a la tabla que tiene relación
def fncRetornarListaDataFrame(lstConsultas, lstSerializadores, lstClaves, lstNuevasClaves):
    lstDataframes = []
    for i in range(0, len(lstConsultas)):
        qrsConsulta = lstConsultas[i]
        jsnSerializador = lstSerializadores[i]
        strClave = lstClaves[i]
        strClaveNueva = lstNuevasClaves[i]
        lstDataframes.append(fncRetornarDataframe(qrsConsulta, jsnSerializador, strClave, strClaveNueva))
    return lstDataframes

# Función que recibe los filtros para retornar una lista con la data para los gráficos de indicadores
# strSet: Cadena de texto del nombre del conjunto al que corresponde el indicador (General o nombre de la categoría)
# strIndicador: Cadena de texto con el nombre del indicador (Total_Sales_Objetive)
# intSubset: Entero con el pk del subconjunto en relación al conjunto que quiere consultar
def fncRetornarDataGraficolst(strSet, strIndicator, intSubset=None):
    lstDataGrafico = []
    lstCategorias = []
    lstIndicador = []
    if intSubset == None:
        qrsIndicador = clsIndicadoresComercialesMdl.objects.filter(set=strSet, indicator=strIndicator)
    else:
        qrsIndicador = clsIndicadoresComercialesMdl.objects.filter(set=strSet, indicator=strIndicator, subset=intSubset)
    if qrsIndicador:
        dctVentaReal = {}
        dctObjetivoVenta = {}
        lstDataVentaReal = []
        lstObjetivoVenta = []
        for i in qrsIndicador:
            lstCategorias.append(i.measurement_date.strftime("%b"))
            lstDataVentaReal.append(float(i.real) / float(1000000))
            lstObjetivoVenta.append(float(i.objetive) / float(1000000))
        dctVentaReal["name"] = 'Venta Real'
        dctVentaReal["data"] = lstDataVentaReal
        dctObjetivoVenta["name"] = 'Objetivo de venta'
        dctObjetivoVenta["data"] = lstObjetivoVenta
        lstIndicador.append(dctVentaReal)
        lstIndicador.append(dctObjetivoVenta)
        lstDataGrafico.append(lstCategorias)
        lstDataGrafico.append(lstIndicador)
    else:
        lstDataGrafico = False
    return lstDataGrafico

def fncRetornarDataSelectdct(strNombreTabla, StrColumnaDescripcion=None):
    lstIndicador = []
    if strNombreTabla == 'modulo_configuracion_clssalidasalmacenmdl':
        strConsultaSalidas = f'SELECT identification_id FROM {strNombreTabla}'
        strConsultaCatalogoClientes = 'SELECT id, city_id FROM modulo_configuracion_clscatalogoclientesmdl'
        strConsultaCiudades = 'SELECT id, city_name FROM modulo_configuracion_clsciudadesmdl'
        lstConsultaSalidas = fncConsultalst(strConsultaSalidas, [])
        lstConsultaCatalogoClientes = fncConsultalst(strConsultaCatalogoClientes, [])
        lstConsultaCiudades = fncConsultalst(strConsultaCiudades, [])
        dtfConsultaSalidas = pd.DataFrame(lstConsultaSalidas, columns=['id'])
        dtfCatalogoClientes = pd.DataFrame(lstConsultaCatalogoClientes, columns=['id', 'city'])
        dtfCiudades = pd.DataFrame(lstConsultaCiudades, columns=['city', 'city_name'])
        dtfUnidos = dtfConsultaSalidas.merge(dtfCatalogoClientes, how='left', on='id')
        dtfUnidos = dtfUnidos.merge(dtfCiudades, how='left', on='city')
        lstCodigosCiudades = dtfUnidos['city'].unique()
        lstCodigosCiudades = [ int(i) for i in lstCodigosCiudades]
        if len(lstCodigosCiudades) > 1:
            lstNombresCiudades = dtfUnidos['city_name'].unique()
            lstNombresCiudades = [ str(i) for i in lstNombresCiudades]
            for i, j in zip(lstCodigosCiudades, lstNombresCiudades):
                dctDataSelect = {}
                dctDataSelect['id'] = i
                dctDataSelect['text'] = j
                lstIndicador.append(dctDataSelect)
        else:
            lstIndicador = 'No puede establecer indicadores para esta categoría ya que no tiene creadas mas de 1'
    else:
        strConsulta = f'SELECT id, {StrColumnaDescripcion} FROM {strNombreTabla}'
        lstConsulta = fncConsultalst(strConsulta, [])
        if len(lstConsulta) > 1:
            for i in lstConsulta:
                dctDataSelect = {}
                dctDataSelect['id'] = i[0]
                dctDataSelect['text'] = i[1]
                lstIndicador.append(dctDataSelect)
        else:
            lstIndicador = 'No puede establecer indicadores para esta categoría ya que no tiene creadas mas de 1'
    return lstIndicador