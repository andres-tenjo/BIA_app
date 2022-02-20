import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.gofplots import qqplot
import sqlite3

# x= 0
# cond= [x<= 5, x> 5]
# choi= [[1, 2], 2]
# y= np.select(cond, choi)
# print(y)
# x= range(0, 31)

# for i in x:
#     if i< 30:
#         print(i)
#     else:
#         print('yea')
# x= False
# x= bool(x)
# irregular= False if x else True
y= [[1], [3, 1, 7]]

def contar(i):
    if len(i['Semana'])>= 12:
        return True
    else:
        return False

# #x = [i+ 1 for j in y for i in j]
# L= []
# for i in y:    
#     l= []
#     for j in i:        
#         l.append(contar(j))
#     L.append(l)
# y=  [i for j in y for i in j]
# print(y)


conn= sqlite3.connect(r'/Users/andres/Desktop/SimEdexa.db')
pedidos= pd.read_sql_query('SELECT *  FROM Pedidos', conn)
conn.commit()

pedidos['Fecha entrega']= pd.to_datetime(pedidos['Fecha entrega'], format= '%Y-%m-%d')

ciudades= pedidos.groupby(['Semana', 'Desc. ciudad'])['Valor total'].sum().reset_index()
divisiones= pedidos.groupby(['Semana', 'DIVISION'])['Valor total'].sum().reset_index()


df1= [i for n, i in ciudades.groupby(pd.Grouper(key= 'Desc. ciudad'))]
df2= [i for n, i in divisiones.groupby(pd.Grouper(key= 'DIVISION'))]
l= [df1, df2]
print(len(df1))
print(len(df2))
print(len(l))
L= []
for i in l:
    l1= []
    for j in i:    
        l1.append(contar(j))
    L.append(l1)
print(L)
print(len(L[0]))
print(len(L[1]))
print(len(L))
