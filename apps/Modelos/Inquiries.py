import pandas as pd
import datetime as dt
from apps.Modelos.Several_func import *
import sqlite3

# Filtra la fecha de inicio para una consulta en una tabla de datos con fechas
# datFecha: Fecha de inicio para el filtro de la consulta (dt.datetime)
# dtfDatos: Cuadro de datos para realizar el filtro (pandas.DataFrame)
# Retorna el cuadro de datos filtrado (pandas.DataFrame)
def fncFiltroIniciodtf(datFecha, dtfDatos):
    dtfFiltrado= None
    if datFecha!= None:            
        if datFecha< dtfDatos['Creation_Date'].min(): dtfFiltrado= dtfDatos
        else: dtfFiltrado= dtfDatos.loc[dtfDatos['Creation_Date']>= datFecha]
    else: dtfFiltrado= dtfDatos
    return dtfFiltrado

# Filtra la fecha de final para una consulta en una tabla de datos con fechas
# datFecha: Fecha de corte para el filtro de la consulta (dt.datetime)
# dtfDatos: Cuadro de datos para realizar el filtro (pandas.DataFrame)
# Retorna el cuadro de datos filtrado (pandas.DataFrame)
def fncFiltradoFindtf(datFecha, dtfDatos):
    dtfFiltrado= None
    if datFecha!= None:
        if datFecha<= dtfDatos['Creation_Date'].max(): dtfFiltrado= dtfDatos.loc[dtfDatos['Creation_Date']<= datFecha]
        else: dtfFiltrado= dtfDatos
    else: dtfFiltrado= dtfDatos
    return dtfFiltrado

# Filtra en una columna especifica con un filtro específico
# lstFiltros: Lista que contiene el o los valores para realizar el filtro (list)
# strNombreCol: Es el nombre de la columna en donde se va a realizar el filtro (str)
# dtfDatos: Cuadro de datos para realizar el filtro (pandas.DataFrame)
# Retorna el cuadro de datos filtrado (pandas.DataFrame)
def fncFiltroOtrodtf(lstFiltros, strNombreCol, dtfDatos):
    if lstFiltros!= None: return pd.concat([dtfDatos.loc[dtfDatos[strNombreCol]== i] for i in lstFiltros])
    else: return dtfDatos

# Filtra la tabla de datos de histórico de movimientos según los las opciones de filtrado
# intCodigoProducto: Código del producto a consultar el movimiento (int)
# lstBodega: lista que contiene los códigos de la(s) bodega(s) para realizar filtro si aplica, predeterminado None (list(int))
# datInicio: Fecha de inicio para visualizar los movimientos del producto, predeterminado None (dt.datetime)
# datFin: Fecha de cierre para visualizar los movimientos del producto, predeterminado None (dt.datetime)
# lstLote: lista que contiene los lotes por los cuales se va a realizar el filtro si aplica, predeterminado None (list(str))
# dtfDatosMovimiento: Archivo de datos del histórico de movimiento, por defecto None (pd.DataFrame)
# Retorna un cuadro de datos con el histórico del producto filtrado por las fechas correspondientes (pandas.DataFrame)
def fncFiltraHistóricodtf(
        intCodigoProducto, lstBodega= None, datInicio= None, datFin= None, lstLote= None, dtfDatosMovimiento= None):
    if dtfDatosMovimiento is None: dtfMovimientoHistorico= data_consulting(['Historical_Movement'])
    else: dtfMovimientoHistorico= dtfDatosMovimiento
    dtfMovimientoHistorico= datetype(dtfMovimientoHistorico, 'Creation_Date')
    dtfMovimientoHistorico= dtfMovimientoHistorico.loc[dtfMovimientoHistorico['Product_Code']== intCodigoProducto]
    dtfFiltrado= fncFiltroOtrodtf(lstBodega, 'Store', dtfMovimientoHistorico)
    dtfFiltrado= fncFiltroOtrodtf(lstLote, 'Batch', dtfFiltrado)
    dtfFiltrado= fncFiltroIniciodtf(datInicio, dtfFiltrado)
    dtfFiltrado= fncFiltradoFindtf(datFin, dtfFiltrado)    
    dtfFiltrado= dtfFiltrado.drop(['Identification', 'Unit_Price', 'Total_Price', 'Crossing_Doc',
                        'Condition', 'Order_Number', 'Return_Type', 'PO_Number', 'Discount', 'Pre_bal'], axis= 1)
    cols= dtfFiltrado.columns.tolist()
    cols= [cols[3], cols[6], cols[8], cols[7], cols[10], cols[2], cols[4], cols[9], cols[12], cols[13], cols[11]]
    final_hist= dtfFiltrado[cols]
    return final_hist.sort_values(['Creation_Date', 'Batch'])


# Calcula el saldo final en una tabla de datos para un producto
# dtfDatos: Tabla de datos para calcular el saldo (pd.DataFrame)
# Retorna el valor del saldo del producto (int)
def fncSaldoFinint(dtfDatos):
    dtfDatos= dtfDatos.assign(balances= dtfDatos['Pre_bal'].cumsum())
    lstSaldos= dtfDatos['balances'].tolist()
    return lstSaldos[- 1]

# Calcula el saldo general para uno o varios productos
# lstCodigo: lista que contiene el(los) código(s) de producto(s) al(los) que se calcula el saldo de inventario (list(int))
# datConsulta: Fecha de consulta para el saldo de inventario (dt.datetime)
# lstBodega: lista que contiene los códigos de la(s) bodega(s) para realizar filtro si aplica, predeterminado None (list(int))
# dtfDatosMovimiento: Archivo de datos del histórico de movimiento, por defecto None (pd.DataFrame)
# Retorna un cuadro de datos con los saldos de inventario según los filtros (pandas.DataFrame)
def fncSaldoInventariodtf(lstCodigo, datConsulta= None, lstBodega= None, dtfDatosMovimiento= None):
    if dtfDatosMovimiento is None: dtfMovimientoHistorico= data_consulting(['Historical_Movement'])
    else:  dtfMovimientoHistorico= dtfDatosMovimiento
    dtfMovimientoHistorico= datetype(dtfMovimientoHistorico, 'Creation_Date')
    dtfMovimientoHistorico= [dtfMovimientoHistorico.loc[dtfMovimientoHistorico['Product_Code']== i] for i in lstCodigo]
    dtfFiltrado= [fncFiltroOtrodtf(lstBodega, 'Store', i) for i in dtfMovimientoHistorico]
    lstLote= [val.loc[val['Batch']== i] for j, val in enumerate(dtfFiltrado) for i in val['Batch'].unique()]
    if datConsulta!= None: lstLote= [fncFiltradoFindtf(datConsulta, i) for i in lstLote]
    else: pass
    lstCodigos= [val.iloc[0]['Product_Code'] for i, val in enumerate(lstLote)]
    lstLotes= [val.iloc[0]['Batch'] for i, val in enumerate(lstLote)]
    lstVencimiento= [val.iloc[0]['Expiration_Date'] for i, val in enumerate(lstLote)]
    lstSaldos= [fncSaldoFinint(val) if not val.empty else 0 for i, val in enumerate(lstLote)]
    lstBOdega= [val.iloc[0]['Store'] for i, val in enumerate(lstLote)]
    return pd.DataFrame(
        {'Product_Code': lstCodigos, 'Batch': lstLotes, 'Inventory_Avail': lstSaldos, 
         'Expiration_Date': lstVencimiento, 'Store': lstBOdega},
                        index= [i for i, num in enumerate(lstCodigos)])    
       
# Filtra únicamente los movimientos que existen en el histórico de movimiento para los productos con registro de lote
# dtfDatosMovimiento: Archivo de datos del histórico de movimiento, por defecto None (pd.DataFrame)
# Retorna un cuadro de datos con el filtro del lote (pandas.DataFrame)
def fncFiltraLotedtf(dtfDatosMovimiento= None):
    if dtfDatosMovimiento is None: dtfMovimientoHistorico= data_consulting(['Historical_Movement'])
    else: dtfMovimientoHistorico= dtfDatosMovimiento
    dtfMovimientoHistorico= datetype(dtfMovimientoHistorico, 'Creation_Date')
    return dtfMovimientoHistorico.loc[dtfMovimientoHistorico['Batch']!= '0']

# Construye un cuadro de datos que contiene únicamente el saldo de un producto por lote
# intCodigo: Corresponde al código del producto a consultar (int)
# intBodega: Corresponde al código de la bodega donde se va a consultar el saldo del producto por lote (int)
# Retorna un cuadro de datos con los lotes correspondientes al producto de consulta (pandas.DataFrame
def fncSaldoLotedtf(intCodigo, intBodega):
    dtfSaldoBodega= data_consulting(['Store_Inventory_Balance'])
    dtfFiltrado= dtfSaldoBodega.loc[(dtfSaldoBodega['Product_Code']== intCodigo)\
                                    & (dtfSaldoBodega['Store']== intBodega)].drop(['Product_Desc'], axis= 1)      
    return dtfFiltrado

# Calcula la diferencia exacta que se requiere para llegar al nivel objetivo de inventario
# srsVerde: Corresponde a la columna del cuadro de datos del nivel verde del amortiguador (pandas.Series)
# srsDisponible: Corresponde a la columna del cuadro de datos del saldo disponible del inventario (pandas.Series)
# srsTransito: Corresponde a la columna del cuadro de datos de las unidades que están por ingresar (pandas.Series)
# Retorna el valor de las unidades a abastecer para llegar al nivel del amortiguador verde (int)
def fncComprarint(srsVerde, srsDisponible, srsTransito):
    if srsVerde- (srsDisponible+ srsTransito)> 0: return srsVerde- (srsDisponible+ srsTransito)
    else: return 0

# Construye la información por cada producto correspondiente al saldo de inventario en la fecha de consulta, 
# los niveles de amortiguador y las cantidades a gestionar en compras
# intBodega: Corresponde al código de la bodega donde se va a consultar el saldo del producto por lote (int)
# Retorna el cuadro de datos con la información correspondiente a los amoriguadores (pandas.DataFrame)
def fncAmortiguadoresdtf(intBodega):
    lstTablaDatos= data_consulting(
        ['Purchase_Orders', 'Levels_of_Inventory_Store', 'Store_Inventory_Balance'])
    dtfOrdenCompra, dtfNoi, dtfSaldoBodega= lstTablaDatos[0], lstTablaDatos[1], lstTablaDatos[2]
    dtfNoi= dtfNoi.loc[dtfSaldoBodega['Store']== intBodega]
    dtfSaldoBodega= dtfSaldoBodega.loc[dtfSaldoBodega['Store']== intBodega]
    dtfSaldoBodega= dtfSaldoBodega.groupby(['Product_Code', 'Product_Desc'])['Inventory_Avail'].sum()
    dtfOrdenAbierta= dtfOrdenCompra.loc[dtfOrdenCompra['Condition']== 'open']
    if not dtfOrdenAbierta.empty:
        dtfOrdenAgrupada= dtfOrdenAbierta.groupby(['Product_Code'])['Quantity'].sum().reset_index()
        dtfOrdenAgrupada.rename(columns= {'Quantity': 'In_Transit'}, inplace= True)
    else: dtfOrdenAgrupada= pd.DataFrame({'Product_Code': [], 'In_Transit': []}, index= [0])
    dtfNoiFiltrado= dtfNoi.loc[dtfNoi['Cut_Date']== dtfNoi['Cut_Date'].max()]
    dtfAmortiguador= dtfNoiFiltrado.merge(dtfOrdenAgrupada, how= 'left', on= 'Product_Code').fillna(0)
    dtfAmortiguador= dtfAmortiguador.merge(dtfSaldoBodega, how= 'outer', on= ['Product_Code']).fillna(0)
    dtfAmortiguador= dtfAmortiguador.assign(To_Manage= dtfAmortiguador.apply(lambda x: fncComprarint(x['Green'], 
                                    x['Inventory_Avail'], x['In_Transit']), axis= 1))
    lstColumnas= dtfAmortiguador.columns.tolist()
    lstColumnas= [lstColumnas[0], lstColumnas[1], lstColumnas[9], lstColumnas[10], lstColumnas[6], 
                  lstColumnas[5], lstColumnas[4], lstColumnas[7], lstColumnas[11]]    
    return dtfAmortiguador[lstColumnas]


# Función para calcular los saldos de inventario actuales por bodega desde el histórico de movimiento
def fncSaldosBodega():
    lstTablaDatos= data_consulting(['Historical_Movement', 'Catálogo'])
    dtfMovimientoHistorico, dtfCatalogoProductos= lstTablaDatos[0], lstTablaDatos[1]    
    lstBodegas= dtfMovimientoHistorico['Store'].unique()
    lstHistoriBodegas= [dtfMovimientoHistorico.loc[dtfMovimientoHistorico['Store']== i] for i in lstBodegas]
    lstCodigoBodega= [i['Product_Code'].unique() for i in lstHistoriBodegas]
    dtfCatalogoProductos= dtfCatalogoProductos.drop(['Product_Cat', 'Product_SubCat','Trademark', 'Purchase_Unit', 'Quantity_PU', 
                                    'Cost_PU', 'Sales_Unit', 'Quantity_SU', 'Full_Sale_Price', 'Barcode', 
                                    'Split_(PU/SU)', 'IVA', 'Creation_Date', 'Supplier_Lead_Time'], axis= 1)
    conn= sqlite3.connect(r'C:\Users\FULERO\Desktop\Convergencia\BIA\DailyWork\BasesparaCotizador\DDBBactualized.db')
    lstSaldos= []
    for i, val in enumerate(lstBodegas):
        dtf= fncSaldoInventariodtf(
            lstCodigoBodega[i], 
            datConsulta= dt.datetime.now(), 
            lstBodega= [val], 
            dtfDatosMovimiento= lstHistoriBodegas[i]).merge(dtfCatalogoProductos, how= 'left', on= 'Product_Code')
        lstSaldos.append(dtf)
    dtfConcatenado= pd.concat(lstSaldos)
    dtfConcatenado= dtfConcatenado.to_sql('Store_Inventory_Balance', con= conn, index= False)
    conn.commit()

