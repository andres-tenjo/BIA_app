import pandas as pd
import numpy as np
import sqlite3
import math
import time

def unique_order(df):
    item_count= df.drop(columns= ['Unnamed: 0', 'Nro documento', 'Fecha', 'Estado movto.', 'Bodega',
                                    'Cant. pedida', 'Cant. pendiente', 'Cant. comprom.', 'Cant. remision',
                                    'Cant. factura', 'Razón social cliente factura',
                                    'Desc. ciudad', 'Nombre vendedor cliente', 'DIVISION', 'Fecha entrega',
                                    'Precio unit.', 'Mes', 'Valor total', 'Semana'])
    item_probability= item_count.assign(Prob= 100)
    return item_probability

def prob_new_bases(df1, df2, var, filt):
    if filt== 'SUBCATEGORIA':
        df1= df1.merge(df2, on= 'Item', how= 'left')\
            .drop(columns= ['Fecha creación', 'Referencia', 'Ubicación', 'Desc. item_y', 'LINEA',  
                            'Compra', 'Venta', 'Cant. disponible', 'Ultimo costo uni.', 'IVA',     
                            'Costo prom. uni.', 'Código barra principal', 'Fecha última compra',   
                            'Fecha última venta', 'TIPO DE PRODUCTO', 'CATEGORIA'])
    else:
        df1= df1.merge(df2, on= 'Item', how= 'left')\
            .drop(columns= ['Fecha creación', 'Referencia', 'Ubicación', 'Desc. item_y', 'LINEA',  
                            'Compra', 'Venta', 'Cant. disponible', 'Ultimo costo uni.', 'IVA',     
                            'Costo prom. uni.', 'Código barra principal', 'Fecha última compra',   
                            'Fecha última venta', 'TIPO DE PRODUCTO', 'SUBCATEGORIA'])
    df1.rename(columns= {'Desc. item_x': 'Desc. item'}, inplace= True)
    new_a= df1[df1[filt]== var]
    return calculated_probability(new_a, new_a)

def calculated_probability(df1, df2):    
    item_count= df1.groupby(['Item', 'Desc. item'])['Nro documento'].count().reset_index()\
        .sort_values(by= 'Nro documento', ascending= False)
    item_probability= item_count.assign(Prob= item_count['Nro documento']/ df2['Nro documento']\
        .nunique()* 100)
    item_probability.drop(columns= ['Nro documento'], inplace= True)
    return item_probability

def prob_per_item(df1, df2, l):
    base_item_probability= None
    complete_orders= [df2[df2['Nro documento']== i] for i in df1['Nro documento']]
    if len(complete_orders)== 1:        
        complete_orders= complete_orders[0]
        item_probability= unique_order(complete_orders)
    elif len(complete_orders)> 1:
        complete_orders= pd.concat(complete_orders)
        item_probability= calculated_probability(complete_orders, df1)
    return item_probability

def two_bases_concatenated(df1, df2, l):
    item_probability= pd.concat([df1, df2])
    item_probability.drop_duplicates(subset= 'Item', keep= 'first', inplace= True)
    item_probability= [item_probability[item_probability['Item']== i] for i in \
        item_probability['Item'] if i not in l]
    return item_probability

def prob_list(l):
    var= None
    if len(l)== 1:
        var= l[0]
    elif len(l)> 1:
        var= pd.concat(l)
        var.sort_values(by= 'Prob', ascending= False, inplace= True)
    return var

def actualized_bases(df, l):
    orders_numbers= df[df['Item']== l[0]]
    filter_recursion= [df[df['Nro documento']== i] for i in orders_numbers['Nro documento']]
    if len(filter_recursion)== 1:
        filter_recursion= filter_recursion[0]
    elif len(filter_recursion)> 1:
        filter_recursion= pd.concat(filter_recursion)
    return filter_recursion

def filter_results(df1, df2):
    new_a= [df1[df1['Item']== i] for i in df1['Item'] if i not in df2]
    return prob_list(new_a)

def new_bases(l1, df, l2, added):
    new_a= None
    n= 0
    var= df[df['Item']== l1[0]]    
    var= var.iloc[0]['SUBCATEGORIA']
    if var== '':
        var= df[df['Item']== l1[0]]
        var= var['CATEGORIA']
        if var== '':
            new_a= calculated_probability(l2[2], l2[2])
            return filter_results(new_a, added)
        else:
            filt= 'CATEGORIA'
            new_a= prob_new_bases(l2[0], df, var, filt)
            new_a= filter_results(new_a, added)
            if new_a is not None:
                return new_a
            else:
                n+= 1
                return new_bases(l1, df, l2[n: ], added)
    else:
        filt= 'SUBCATEGORIA'
        new_a= prob_new_bases(l2[0], df, var, filt)
        new_a= filter_results(new_a, added)
        if new_a is not None:
            return new_a
        else:
            n+= 1
            return new_bases(l1, df, l2[n: ], added)    
    
def validated_bases(l1, l2, df, memo= None):
    memo= memo
    item_probability= None
    n= 0
    if len(l1)== 1:
        if len(l1[0])!= 0:
            orders_numbers= l1[0][l1[0]['Item']== l2[0]]
            if len(orders_numbers['Nro documento'])>= 1:
                item_probability= prob_per_item(orders_numbers, l1[0], added)
                item_probability= pd.concat([item_probability, memo])
                item_probability.drop_duplicates(subset= 'Item', keep= 'first', inplace= True)
                if df is not None:
                    item_probability= two_bases_concatenated(item_probability, df, added)
                    item_probability= prob_list(item_probability)
            else:
                item_probability= two_bases_concatenated(df, memo, added)
                item_probability= prob_list(item_probability)
        else:
            if df is not None:
                if memo is not None:
                    item_probability= two_bases_concatenated(df, memo, added)
                    item_probability= prob_list(item_probability)
                else:
                    item_probability= df
        return item_probability
    elif len(l1)> 1:
        n-= 1
        base_orders_numbers= l1[1][l1[1]['Item']== l2[0]]
        if len(base_orders_numbers['Nro documento'])>= 1:
            memo= prob_per_item(base_orders_numbers, l1[1], added)            
        return validated_bases(l1[: n], l2, df, memo)

def helper(rec_added, recursion, added, cust_base, cat_base, gen_base, memo= None):    
    added= added
    cust_base= cust_base
    cat_base= cat_base
    gen_base= gen_base
    memo= memo
    item_probability, filter_recursion= None, None
    n= 0
    if len(rec_added)== 1:
        item_probability= validated_bases([recursion, cust_base], rec_added, memo)
        if item_probability is not None:
            item_probability= filter_results(item_probability, added)
            if item_probability is not None:
                return item_probability
            else:
                new_a= new_bases(rec_added, catalogo, [cust_base, cat_base, gen_base], added)
                return filter_results(new_a, added)
        else:
            item_probability= new_bases(rec_added, catalogo, [cust_base, cat_base, gen_base], added)
            return item_probability
    else:
        n+= 1
        if len(recursion)== 0:
            filter_recursion= actualized_bases(cust_base, rec_added)
        else:
            filter_recursion= actualized_bases(recursion, rec_added)
        memo= validated_bases([recursion, cust_base], rec_added, memo)
        return helper(rec_added[n: ], filter_recursion, added, cust_base, cat_base, gen_base, memo)