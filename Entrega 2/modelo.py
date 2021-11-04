from gurobipy import GRB, Model, quicksum
import os
import json

##### Comentarios Generales ####
# Omitimos los tildes y ñ, para evitar posibles errores. Por el mismo motivo, algunas cosas 
# están escritas en inglés



#### CONJUNTOS ####
# 1) Hogares a fiscalizar
ruta_hogares_json = os.path.join("Entrega 2", "hogares.json")
with open(ruta_hogares_json, "r") as file:
    hogares = json.load(file)   
    # diccionario de la forma {numero_hogar: {"comuna" : comuna, "cant_personas": numero}}


# 2) Horas del día
horas = [n for n in range (8, 19)]

# 3) Días de la semana
dias = [n for n in range (1, 8)]

# 4) Comunas de Santiago
ruta_comunas = os.path.join("Entrega 2", "comunas.json")
with open(ruta_comunas, "r") as file:
    comunas = json.load(file)   

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

# 7) Implementos sanitarios
implementos = ["guante", "mascarilla", "pantallas faciales", "alcohol gel"]

# 8) Comunas restringidas
ruta_comunas_vetadas = os.path.join("Entrega 2", "comunas_vetadas.json")
with open(ruta_comunas_vetadas, "r") as file:
    comunas_vetadas = json.load(file)   


#### PARÁMETROS ####
# Calidad
qual = 10

# Valor de calidad de la fiscalización
quality_f = 1

# Valor de calidad de la llamada
quality_l = 5

# Costo de movilización entre comunas
ruta_costos_desp_json = os.path.join("Entrega 2", "costos_desplazamientos.json")
with open(ruta_costos_desp_json, "r") as file:
    costos_desp = json.load(file)


# Costo fijo asociado al fiscalizador "f" (sueldo, colación, etc.)
cost_f = 1000000

# Costo fijo asociado al operador "o" (sueldo, colación, etc.)
cost_o = 1000000

# Máximo de llamadas por hora por operador
max_call_o_h = 5

# Máximo de llamadas a una casa por día
max_call_h_d = 5

# Cantidad maxima a adquirir del implemento sanitario a el dia d
max_a_d = 10
maxInv_a_d = 100



#### MODELO ####
model = Model("Distribucion Fiscalizadores de Viajeros")


#### VARIABLES ####
K_f = model.addVars(fiscalizadores, vtype=GRB.BINARY, name="K_f")
M_o = model.addVars(operadores, vtype=GRB.BINARY, name="M_o")
R_htdf = model.addVars(hogares.keys(), horas, dias, fiscalizadores, vtype=GRB.BINARY, name="R_htdf")
L_htdo = model.addVars(hogares.keys(), horas, dias, operadores, vtype=GRB.BINARY, name="L_htdo")
V_tdfks = model.addVars(horas, dias, fiscalizadores, comunas_santiago, comunas_santiago, vtype=GRB.BINARY, name="V_tdfks")
PCR_htdf =  model.addVars(hogares, horas, dias, fiscalizadores, vtype=GRB.BINARY, name="PCR_htdf")
P_tdfs = model.addVars(horas, dias, fiscalizadores, comunas_santiago, vtype=GRB.BINARY, name="P_tdfs")
E_tdo = model.addVars(horas, dias, operadores, vtype=GRB.INTEGER, name="E_tdo")
I_ad = model.addVars(implementos, dias, vtype=GRB.INTEGER, name="I_ad", ub=max_a_d)
iI_ad = model.addVars(implementos, dias, vtype=GRB.INTEGER, name="iI_ad", ub=maxInv_a_d)

model.update()


#### RESTRICCIONES ####
# 1) Horario de trabajo de fiscalizadores
model.addConstrs((quicksum(R_htdf[hogar, hora, dia, fiscalizador] == 0 
    for hogar in hogares for hora in horas if (hora == 13 or hora == 14) for dia in dias
    for fiscalizador in fiscalizadores)), name="horario_fisc")

# 2) Horario de trabajo de operadores
model.addConstrs((quicksum(L_htdo[hogar, hora, dia, operador] == 0 
    for hogar in hogares for hora in horas if (hora == 13 or hora == 14) for dia in dias
    for operador in operadores)), name="horario_operador")

# 3) Restricción de que la cantidad de implementos sanitarios a adquirir debe igualar o superar a la cantidadde fiscalizadores contratados
model.addConstrs((quicksum(K_f[fiscalizador] for fiscalizador in fiscalizadores) <=
                  I_ad[implemento, dia] for implemento in implementos for dia in dias), name="min_implementos")

# Restriccion de no sobrepasar maximo de horas disponibles
model.addConstrs((quicksum(L_htdo[hogar, hora, dia, operador] for hora in horas for operador in operadores) <=
                  max_call_h_d for hogar in hogares for dia in dias), name="max_hogares")


#### FUNCIÓN OBJETIVO ####
# obj = funcion y sumas
# model.setObjective(obj, GRB.MINIMIZE)


#### CORRER MODELO ####

model.optimize()

#### MOSTRAR LOS RESULTADOS ####
model.printAttr("X")
