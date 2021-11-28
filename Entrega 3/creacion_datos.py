from faker import Faker
import pandas as pd
import os
import random 
import json

fake = Faker()

# primero crearemos los fiscalizadores
ruta_fisc_csv = os.path.join("Excel", "nombres_fiscalizadores.json") 
lista_nombres_fiscalizadores = []
for i in range(0 , 1000):
    lista_nombres_fiscalizadores.append(fake.name())
dict_fiscalizadores = {"Nombre" : lista_nombres_fiscalizadores}
dataframe = pd.DataFrame(data = dict_fiscalizadores)
# los guardamos en un csv
dataframe.to_csv(ruta_fisc_csv)


# creamos la versión 2 de los fiscalizadores, los guardamos en un json. A cada uno le damos
# un nombre (con faker) y una comuna al azar (con random). 
ruta_fisc_json = os.path.join("Json", "fiscalizadores.json")
dict_fiscalizadores = {}
for i in range(0, 50):
    nombre_fisc = fake.name()
    comuna_fisc = random.randint(1,32)
    dict_individual = {"nombre": nombre_fisc, "comuna": comuna_fisc}
    dict_fiscalizadores[int(i)] = dict_individual
with open(ruta_fisc_json, "w") as outfile:
    json.dump(dict_fiscalizadores, outfile)


# ahora crearemos a los operadores
ruta_operator_csv = os.path.join("Excel", "nombres_operadores.csv") 
lista_nombres_operadores = []
for i in range (0 , 500):
    lista_nombres_operadores.append(fake.name())
dict_operadores = {"Nombre" : lista_nombres_operadores}
dataframe = pd.DataFrame(data = dict_operadores)
# los guardamos en un csv
dataframe.to_csv(ruta_operator_csv)


# creamos la versión 2 de los operadores, los guardamos en un json. A cada uno le damos
# un nombre (con faker). 
ruta_oper_json = os.path.join("Json", "operadores.json")
dict_operadores = {}
for a in range(0, 25):
    nombre_opera = fake.name()
    dict_individual = {"nombre": nombre_opera}
    dict_operadores[int(a)] = dict_individual
with open(ruta_oper_json, "w") as outfile:
    json.dump(dict_operadores, outfile)
