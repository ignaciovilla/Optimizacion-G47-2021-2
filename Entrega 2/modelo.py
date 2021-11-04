from gurobipy import GRB, Model, quicksum
import os
import json

#### CONJUNTOS ####
# 1) Hogares a fiscalizar
ruta_hogares_json = os.path.join("Entrega 2", "hogares.json")
with open(ruta_hogares_json, "r") as file:
    hogares = json.load(file)   
    # diccionario de la forma {numero_hogar: {"comuna" : comuna, "cant_personas": numero}}


# 2) Horas del día
horas = [n for n in range (8, 19)]

# 3) Días de la semana
dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# 4) Comunas de Santiago

# 5) Fiscalizadores contratables
path_fiscalizadores = os.path.join("Entrega 2", "nombres_fiscalizadores.csv")
fiscalizadores = []
with open(path_fiscalizadores, "r") as archivo:
    lineas = archivo.readlines()
    for linea in lineas:
        linea = linea.strip().split(",")
        fiscalizadores.append(linea[1])


# 6) Operadores de llamadas contratables
path_operadores = os.path.join("Entrega 2", "nombres_operadores.csv")
operadores = []
with open(path_operadores, "r") as archivo:
    lineas = archivo.readlines()
    for linea in lineas:
        linea = linea.strip().split(",")
        operadores.append(linea[1])


#### PARÁMTEROS ####
# Calidad
qual = 10

# Valor de calidad de la fiscalización
quality_f = 1

# Valor de calidad de la llamada
quality_l = 5

# Costo de movilización entre comunas

# Comuna de hogar "h"

# Costo fijo asociado al fiscalizador "f" (sueldo, colación, etc.)
cost_f = 1000000

# Costo fijo asociado al operador "o" (sueldo, colación, etc.)
cost_o = 1000000

# Máximo de llamadas por hora por operador
max_call_o_h = 5

# Máximo de llamadas a una casa por día
max_call_h_d = 5


#### MODELO ####
model = Model()


#### VARIABLES ####

model.update()


#### RESTRICCIONES ####


#### FUNCIÓN OBJETIVO ####
# obj = funcion y sumas
model.setObjective(obj, GRB.MINIMIZE)


#### CORRER MODELO ####

model.optimize()

#### MOSTRAR LOS RESULTADOS ####
model.printAttr("X")
