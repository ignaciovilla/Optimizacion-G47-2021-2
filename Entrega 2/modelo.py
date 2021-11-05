from gurobipy import GRB, Model, quicksum
import os
import json

##### Comentarios Generales ####
# Omitimos los tildes y ñ, para evitar posibles errores. Por el mismo motivo, algunas cosas 
# están escritas en inglés

# Enlas restricciones 8,9,13,16,21,22



#### CONJUNTOS ####
# 1) Hogares a fiscalizar
ruta_hogares_json = os.path.join("Entrega 2", "hogares.json")
with open(ruta_hogares_json, "r") as file:
    hogares = json.load(file)   
    # diccionario de la forma {numero_hogar: {"comuna" : comuna, "cant_personas": numero}}
print(hogares)


# 2) Horas del día
horas = [n for n in range (8, 19)]  # lista de números del 8 al 18 representando las horas del día disponibles
                                    # para trabajar

# 3) Días de la semana
dias = [n for n in range (1, 8)]    # lista de números del 1 al 7 representando los días para fiscalizar

# 4) Comunas de Santiago
ruta_comunas = os.path.join("Entrega 2", "comunas.json")
with open(ruta_comunas, "r") as file:
    comunas_santiago = json.load(file)   

# 5) Fiscalizadores contratables
# path_fiscalizadores = os.path.join("Entrega 2", "nombres_fiscalizadores.csv")
# fiscalizadores = []
# with open(path_fiscalizadores, "r") as archivo:
#     lineas = archivo.readlines()
#     for linea in lineas:
#         linea = linea.strip().split(",")
#         fiscalizadores.append(linea[1])
fiscalizadores = [n for n in range (1, 5)]

# 6) Operadores de llamadas contratables
# path_operadores = os.path.join("Entrega 2", "nombres_operadores.csv")
# operadores = []
# with open(path_operadores, "r") as archivo:
#     lineas = archivo.readlines()
#     for linea in lineas:
#         linea = linea.strip().split(",")
#         operadores.append(linea[1])
operadores = [n for n in range (1, 3)]

# 7) Implementos sanitarios
implementos = ["guantes", "mascarilla", "pantalla_facial", "delantal_quirurgico", "alcohol_gel"]

# 8) Comunas restringidas
ruta_comunas_vetadas = os.path.join("Entrega 2", "comunas_vetadas.json")
with open(ruta_comunas_vetadas, "r") as file:
    comunas_vetadas = json.load(file)   




#### PARÁMETROS ####
# Calidad
qual = 10

# Valor de calidad de la fiscalización
calf = 5

# Valor de calidad de la llamada
call = 1

# Valor de calidad del test PCR
calpcr = 9

# Valor de calidad del test de antígeno
calant = 6

# Costo de movilización entre comunas
ruta_costos_desp_json = os.path.join("Entrega 2", "costos_desplazamientos.json")
with open(ruta_costos_desp_json, "r") as file:
    costos_desp = json.load(file)       ## este es CM_i,j

costos_desp_oficial = {}
for key in costos_desp.keys():
    key_prov = key.split(", ")
    costos_desp_oficial[(key_prov[0]), (key_prov[1])] = costos_desp[key]

# Costo fijo asociado al fiscalizador "f" (sueldo, colación, etc.)
caf_f = 600000

# Costo fijo asociado al operador "o" (sueldo, colación, etc.)
cof_o = 337000

# Máximo de llamadas por hora por operador
maxc = 5

# Máximo de llamadas a una vivienda por día
maxh = 2

# Máximo de visitas a una vivienda por día
maxv = 2

# Costo de comprar el implemento sanitario, precio unitario
cims = {"guantes": 124, "mascarilla": 240, "pantalla_facial": 590,
    "delantal_quirurgico": 4500, "alcohol_gel": 3353}

# Rendimiento específico por visita de cada implemento
alpha = {"guantes": 1, "mascarilla": 1, "pantalla_facial": 15, 
    "delantal_quirurgico": 1, "alcohol_gel": 30}

# Costo asociado a la compra y uso de test PCR
beta = 25000

# Costo asociado a la compra y uso de test de antigeno
gamma = 28495

# Big M
M = 1000000000

#### MODELO ####
model = Model("Distribucion Fiscalizadores de Viajeros")


#### VARIABLES ####
K_f = model.addVars(fiscalizadores, vtype=GRB.BINARY, name="K_f")
M_o = model.addVars(operadores, vtype=GRB.BINARY, name="M_o")
R_htdf = model.addVars(hogares.keys(), horas, dias, fiscalizadores, vtype=GRB.BINARY, name="R_htdf")
L_htdo = model.addVars(hogares.keys(), horas, dias, operadores, vtype=GRB.BINARY, name="L_htdo")
V_tdfky = model.addVars(horas, dias, fiscalizadores, comunas_santiago.keys(), comunas_santiago.keys(), vtype=GRB.BINARY, name="V_tdfky")
PCR_htdf =  model.addVars(hogares.keys(), horas, dias, fiscalizadores, vtype=GRB.BINARY, name="PCR_htdf")
ANT_htdf = model.addVars(hogares.keys(), horas, dias, fiscalizadores, vtype=GRB.BINARY, name="ANT_htdf")
P_tdfs = model.addVars(horas, dias, fiscalizadores, comunas_santiago.keys(), vtype=GRB.BINARY, name="P_tdfs")
I_ad = model.addVars(implementos, dias, vtype=GRB.INTEGER, name="I_ad")
iI_ad = model.addVars(implementos, dias, vtype=GRB.INTEGER, name="iI_ad")

model.update()


### RESTRICCIONES ####
# 1) Un fiscalizador solo puede realizar acciones si es que fue contratado
model.addConstrs((quicksum(quicksum(R_htdf[hogar, hora, dia, fiscalizador] + PCR_htdf[hogar, hora, dia, fiscalizador]
                  + ANT_htdf[hogar, hora, dia, fiscalizador] for hogar in hogares.keys()) + 
                  quicksum(V_tdfky[hora, dia, fiscalizador, comuna1, comuna2]
                  for comuna1 in comunas_santiago.keys() for comuna2 in comunas_santiago.keys()) for hora in horas for dia in dias)
                  <= M * K_f[fiscalizador] for fiscalizador in fiscalizadores), name="f_contratado")

# 2) Un operador solo puede llamar si es que fue contradado
model.addConstrs((quicksum(L_htdo[hogar, hora, dia, operador] for dia in dias for hora in horas 
                  for hogar in hogares.keys()) <= M * M_o[operador] for operador in operadores), name="op_contratado")

# 3) Horario de trabajo de fiscalizadores
model.addConstrs((quicksum(R_htdf[hogar, 13, dia, fiscalizador] + R_htdf[hogar, 14, dia, fiscalizador] 
    for hogar in hogares.keys()) == 0 for dia in dias
    for fiscalizador in fiscalizadores), name="horario_fisc")

# 4) Horario de trabajo de operadores
model.addConstrs((quicksum(L_htdo[hogar, 13, dia, operador] + L_htdo[hogar, 14, dia, operador]   
    for hogar in hogares.keys()) == 0 for dia in dias
    for operador in operadores), name="horario_operador")

# 5) Cantidad maxima de llamadas a una vivienda en un dia
model.addConstrs((quicksum(L_htdo[hogar, hora, dia, operador] for hora in horas for operador in operadores) <=
                  maxh for hogar in hogares.keys() for dia in dias), name="max_hogares")

# 6) La cantidad de implementos sanitarios a adquirir debe igualar o superar a la cantidad necesitada de estos por visita.
model.addConstrs((quicksum(R_htdf[hogar, hora, dia, fiscalizador] for hogar in hogares.keys() for fiscalizador in fiscalizadores 
                  for hora in horas) * alpha[implemento] <= I_ad[implemento, dia] 
                  for implemento in implementos for dia in dias), name="op_contratado")

# 7) Inventario inicial #### d = 1
model.addConstrs((iI_ad[implemento, 1] == 0 for implemento in implementos), name="initial_stock")

# 8) Flujo inventario
model.addConstrs((quicksum(R_htdf[hogar, hora, dia, fiscalizador] for hogar in hogares.keys() for fiscalizador in fiscalizadores 
                  for hora in horas) * alpha[implemento] + iI_ad[implemento, dia] <= 
                  iI_ad[implemento, dia-1] + I_ad[implemento, dia] for implemento in implementos 
                  for dia in [2, 3, 4, 5, 6, 7]), name="flujo")

# 9) Un fiscalizador no puede estar en dos comunas distintas en horas contiguas
model.addConstrs((quicksum(P_tdfs[hora, dia, fiscalizador, comuna1]for comuna1 in comunas_santiago.keys())
                   + quicksum(P_tdfs[hora+1, dia, fiscalizador, comuna2] for comuna2 in comunas_santiago.keys())<= 1 
                   for hora in [8,9,10,11,12,13,14,15,16,17] for dia in dias for fiscalizador in fiscalizadores)
                   ,name="disponibilidad_fisc")

# 10) No puede haber una llamada y una fiscalizacion a la misma hora en una misma casa
model.addConstrs((quicksum(R_htdf[hogar, hora, dia, fiscalizador] for fiscalizador in fiscalizadores) +
                  quicksum(L_htdo[hogar, hora, dia, operador] for operador in operadores) <= 1
                  for hora in horas for hogar in hogares.keys() for dia in dias), name="redundancia")

# 11) Un fiscalizador no puede estar en dos comunas a la vez
model.addConstrs((quicksum(P_tdfs[hora, dia, fiscalizador, comuna] for comuna in comunas_santiago.keys())
                 <= 1 for hora in horas for dia in dias for fiscalizador in fiscalizadores), name="logica_fisc")

# 12) El fiscalizador puede comenzar el viaje solo si se encuentra en la comuna
model.addConstrs((V_tdfky[hora, dia, fiscalizador, comuna1, comuna2] == P_tdfs[hora, dia, fiscalizador, comuna1]
                 for hora in horas for dia in dias for fiscalizador in fiscalizadores 
                 for comuna1 in comunas_santiago.keys() for comuna2 in comunas_santiago.keys()), name="inicio_viaje_fisc")

# 13) Al finalizar el viaje, el fiscalizador debe encontrarse en la cual estaba viajando
model.addConstrs((V_tdfky[hora, dia, fiscalizador, comuna1, comuna2] == P_tdfs[hora+1, dia, fiscalizador, comuna2]
                 for hora in [8,9,10,11,12,13,14,15,16,17] for dia in dias for fiscalizador in fiscalizadores
                 for comuna1 in comunas_santiago.keys() for comuna2 in comunas_santiago.keys()), name="fin_viaje_fisc")

# 14) Un fiscalizador solo puede hacer una actividad por hora
model.addConstrs((quicksum(R_htdf[hogar, hora, dia, fiscalizador] + quicksum(V_tdfky[hora, dia, fiscalizador, comuna1, comuna2] 
                  for comuna1 in comunas_santiago.keys() for comuna2 in comunas_santiago.keys()) 
                  for hogar in hogares.keys()) <= 1 for hora in horas for dia in dias 
                  for fiscalizador in fiscalizadores), name="acc_max_fisc")


# 15) Numero maximo de llamadas por hora por operador
model.addConstrs((quicksum(L_htdo[hogar, hora, dia, operador] for hogar in hogares.keys()) <= 
                  maxc for operador in operadores for dia in dias for hora in horas), name="max_llamadas_ph")

# 16) Restriccion fiscalizacion cada 2 dias maximo
model.addConstrs((quicksum(R_htdf[hogar, hora, dia, fiscalizador] + R_htdf[hogar, hora-1, dia, fiscalizador] 
                  for fiscalizador in fiscalizadores for hora in [9,10,11,12,13,14,15,16,17,18]) >= 1 
                  for hogar in hogares.keys() for dia in dias), name="temp_entre_fisc")

# 17) Maximo de visitas por cada vivienda a fiscalizar
model.addConstrs((quicksum(R_htdf[hogar, hora, dia, fiscalizador] for fiscalizador in fiscalizadores 
                  for hora in horas) <= maxv for hogar in hogares.keys() for dia in dias),
                  name="max_visitas_por_hogar_a_fisc")
    
# 18) Si se hace un test PCR a un hogar h tiene que hacerse una 
        #visita a la misma hora t del dia d por el fiscalizador f
model.addConstrs((PCR_htdf[hogar, hora, dia, fiscalizador] <= R_htdf[hogar, hora, dia, fiscalizador]
                  for hogar in hogares.keys() for hora in horas for dia in dias
                  for fiscalizador in fiscalizadores), name="PCR_visita")

# 19) Si se hace un test de antigenos a un hogar h tiene que hacerse
        # una visita a la misma hora t del dia d por el fiscalizador f:
model.addConstrs((ANT_htdf[hogar, hora, dia, fiscalizador] <= R_htdf[hogar, hora, dia, fiscalizador]
                  for hogar in hogares.keys() for hora in horas for dia in dias
                  for fiscalizador in fiscalizadores), name="ANT_visita")

# 20) Se puede hacer solo una de las siguientes fiscalizaciones por hogar $h$ en cada hora $t$ 
# en cada día d: Test PCR, test de antígeno, llamada telefónica:
model.addConstrs((quicksum(PCR_htdf[hogar, hora, dia, fiscalizador] + ANT_htdf[hogar, hora, dia, fiscalizador] 
                  for fiscalizador in fiscalizadores) + quicksum(L_htdo[hogar, hora, dia, operador] for operador 
                  in operadores) <= 1 for hogar in hogares.keys() for hora in horas for dia in dias), name="tipo_visita")

# 21) Si se hace un test PCR en el dia x, la casa no debe recibir mas fiscalizaciones desde el dia x+2
model.addConstrs((quicksum(quicksum(R_htdf[hogar, hora, dia + 2, fiscalizador]
                + PCR_htdf[hogar, hora, dia + 2, fiscalizador]
                + ANT_htdf[hogar, hora, dia + 2, fiscalizador] for fiscalizador in fiscalizadores) + 
                quicksum(L_htdo[hogar, hora, dia + 2, operador]
                for operador in operadores) for hora in horas for dia in [1, 2, 3, 4, 5])
                <= M * quicksum(PCR_htdf[hogar, hora, dia, fiscalizador] for hora in horas 
                for fiscalizador in fiscalizadores for dia in [1, 2, 3, 4, 5]) 
                for hogar in hogares.keys()), name="veto_PCR")

# 22) Si se hace un test de antígenos en el día $x$, la casa no debe recibir más fiscalizaciones desde el día x+1
model.addConstrs((quicksum(quicksum(R_htdf[hogar, hora, dia + 1, fiscalizador]
                + PCR_htdf[hogar, hora, dia + 1, fiscalizador]
                + ANT_htdf[hogar, hora, dia + 1, fiscalizador] for fiscalizador in fiscalizadores) + 
                quicksum(L_htdo[hogar, hora, dia + 1, operador]
                for operador in operadores) for hora in horas for dia in [1, 2, 3, 4, 5, 6])
                <= M * quicksum(ANT_htdf[hogar, hora, dia, fiscalizador]for hora in horas 
                for fiscalizador in fiscalizadores for dia in [1, 2, 3, 4, 5, 6]) 
                for hogar in hogares.keys()), name="veto_ANT")
                
# 23) No se puede realizar un viaje desde una comuna "y" a una comuna "k", si es que "y" pertenece a  RES_{k}, 
#     con $RES_{k}=comunas restringidas de "k"
model.addConstrs((quicksum(V_tdfky[hora, dia, fiscalizador, comuna1, str(comuna2)] 
                for comuna2 in comunas_vetadas[comuna1]) == 0 
                for hora in horas for dia in dias for fiscalizador in fiscalizadores 
                for comuna1 in comunas_santiago.keys()), name="comunas_vetadas")

# 24) La suma de fiscalizaciones y llamadas debe alcanzar, al menos, el umbral de calidad
model.addConstrs((quicksum(quicksum(R_htdf[hogar, hora, dia, fiscalizador]*calf + 
                  PCR_htdf[hogar, hora, dia, fiscalizador]*calpcr +
                  ANT_htdf[hogar, hora, dia, fiscalizador]*calant for fiscalizador in fiscalizadores) + 
                  quicksum(L_htdo[hogar, hora, dia, operador]*call
                  for operador in operadores) for hora in horas for dia in dias)
                  >= qual for hogar in hogares.keys()), name="qual_fis_llam")

#### FUNCIÓN OBJETIVO ####
obj = (quicksum(K_f[fiscalizador] * caf_f for fiscalizador in fiscalizadores) +
      quicksum(M_o[operador] * cof_o for operador in operadores) + 
      (quicksum(PCR_htdf[hogar, hora, dia, fiscalizador] for hogar in hogares.keys() for hora in horas 
      for dia in dias for fiscalizador in fiscalizadores))*beta + 
      (quicksum(ANT_htdf[hogar, hora, dia, fiscalizador] for hogar in hogares.keys() for hora in horas 
      for dia in dias for fiscalizador in fiscalizadores))*gamma + 
      quicksum(V_tdfky[hora, dia, fiscalizador, comuna_i, comuna_f] * costos_desp_oficial[(comuna_i, comuna_f)] 
      for hora in horas for dia in dias for fiscalizador in fiscalizadores for comuna_i in comunas_santiago.keys() 
      for comuna_f in comunas_santiago.keys() if comuna_i != comuna_f) + 
      quicksum(I_ad[implemento, dia] * cims[implemento] for dia in dias for implemento in implementos))
      
model.setObjective(obj, GRB.MINIMIZE)


#### CORRER MODELO ####

model.optimize()

#### MOSTRAR LOS RESULTADOS ####
# model.printAttr("X")
model.write("resultados.sol")