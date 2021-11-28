from gurobipy import GRB, Model, quicksum
import os
import json

from parametros_a_probar import GAP_PERMITIDO, MAX_TIEMPO

MAX_TIEMPO = 10 # En minutos
GAP_PERMITIDO = 0.1

# parámetros [Costo fiscalizador, Costo operador, Costo implemento sanitario, 
# Rendimiento implemento, Costo PCR,  Costo antigeno, string_prueba]
base = [600000, 337000, {"guantes": 124, "mascarilla": 240, "pantalla_facial": 590,
    "delantal_quirurgico": 4500, "alcohol_gel": 3353}, 
    {"guantes": 1, "mascarilla": 1, "pantalla_facial": 15, 
    "delantal_quirurgico": 1, "alcohol_gel": 30}, 25000, 28495]

pruebas = [
    [base[0]*1.1, base[1], base[2], base[3], base[4], base[5], "resultados_10positivo_costofi.sol"],
    [base[0], base[1]*1.1, base[2], base[3], base[4], base[5], "resultados_10positivo_costoop.sol"],
    [base[0]*0.9, base[1], base[2], base[3], base[4], base[5], "resultados_10negativo_costof.sol"],
    [base[0], base[1]*0.9, base[2], base[3], base[4], base[5], "resultados_10negativo_costoop.sol"],
    [base[0]*1.2, base[1], base[2], base[3], base[4], base[5], "resultados_20positivo_costof.sol"],
    [base[0], base[1]*1.2, base[2], base[3], base[4], base[5], "resultados_20positivo_costoop.sol"],
    [base[0]*0.8, base[1], base[2], base[3], base[4], base[5], "resultados_20negativo_costof.sol"],
    [base[0], base[1]*0.8, base[2], base[3], base[4], base[5], "resultados_20negativo_costoop.sol"],
    [base[0], base[1], base[2], base[3], base[4]*0.8, base[5], "resultados_20negativo_PCR.sol"],
    [base[0], base[1], base[2], base[3], base[4]*0.9, base[5], "resultados_10negativo_PCR.sol"],
    [base[0], base[1], base[2], base[3], base[4]*1.1, base[5], "resultados_10positivo_PCR.sol"],
    [base[0], base[1], base[2], base[3], base[4]*1.2, base[5], "resultados_20positivo_PCR.sol"],
    [base[0], base[1], base[2], base[3], base[4], base[5]*0.8, "resultados_20negativo_ANT.sol"],
    [base[0], base[1], base[2], base[3], base[4], base[5]*0.9, "resultados_10negativo_ANT.sol"],
    [base[0], base[1], base[2], base[3], base[4], base[5]*1.1, "resultados_10positivo_ANT.sol"],
    [base[0], base[1], base[2], base[3], base[4], base[5]*1.2, "resultados_20positivo_ANT.sol"],
    [base[0], base[1], {"guantes": base[2]["guantes"]*0.8, 
        "mascarilla": base[2]["mascarilla"]*0.8, "pantalla_facial": base[2]["pantalla_facial"]*0.8,
        "delantal_quirurgico": base[2]["delantal_quirurgico"]*0.8,
        "alcohol_gel": base[2]["alcohol_gel"]*0.8}, base[3], base[4], base[5],
        "resultados_20negativo_costoimp.sol"],
    [base[0], base[1], {"guantes": base[2]["guantes"]*0.9, 
        "mascarilla": base[2]["mascarilla"]*0.9, "pantalla_facial": base[2]["pantalla_facial"]*0.9,
        "delantal_quirurgico": base[2]["delantal_quirurgico"]*0.9,
        "alcohol_gel": base[2]["alcohol_gel"]*0.9}, base[3], base[4], base[5],
        "resultados_10negativo_costoimp.sol"],
    [base[0], base[1], {"guantes": base[2]["guantes"]*1.1, 
        "mascarilla": base[2]["mascarilla"]*1.1, "pantalla_facial": base[2]["pantalla_facial"]*1.1,
        "delantal_quirurgico": base[2]["delantal_quirurgico"]*1.1,
        "alcohol_gel": base[2]["alcohol_gel"]*1.1}, base[3], base[4], base[5],
        "resultados_10positivo_costoimp.sol"],
    [base[0], base[1], {"guantes": base[2]["guantes"]*1.2, 
        "mascarilla": base[2]["mascarilla"]*1.2, "pantalla_facial": base[2]["pantalla_facial"]*1.2,
        "delantal_quirurgico": base[2]["delantal_quirurgico"]*1.2,
        "alcohol_gel": base[2]["alcohol_gel"]*1.2}, base[3], base[4], base[5],
        "resultados_20positivo_costoimp.sol"],
    [base[0], base[1], base[2], {"guantes": base[3]["guantes"]*2, 
        "mascarilla": base[3]["mascarilla"]*2, "pantalla_facial": base[3]["pantalla_facial"]*2,
        "delantal_quirurgico": base[3]["delantal_quirurgico"]*2,
        "alcohol_gel": base[3]["alcohol_gel"]*2}, base[4], base[5],
        "resultados_doble_rendimientoimp.sol"]
]



for prueba in pruebas:
    try:
        #### CONJUNTOS ####
        # 1) Hogares a fiscalizar
        ruta_hogares_json = os.path.join("Json", "hogares_v2.json")
        with open(ruta_hogares_json, "r") as file:
            hogares = json.load(file)   
            # diccionario de la forma {numero_hogar: {"comuna" : número_comuna}}

        # 2) Horas del día
        horas = [n for n in range (8, 19)]  # lista de números del 8 al 18 representando las horas del día disponibles
                                            # para trabajar

        # 3) Días de la semana
        dias = [n for n in range (1, 8)]    # lista de números del 1 al 7 representando los días para fiscalizar

        # 4) Comunas de Santiago
        ruta_comunas = os.path.join("Json", "comunas.json")
        with open(ruta_comunas, "r") as file:
            comunas_santiago = json.load(file)   
            # diccionario de la forma {numero_comuna: nombre_comuna}}

        # 5) Fiscalizadores contratables
        ruta_fiscalizadores = os.path.join("Json", "fiscalizadores.json")
        with open(ruta_fiscalizadores, "r") as archivo:
            fiscalizadores = json.load(archivo)
            # diccionario de la forma {numero_fiscalizador: {"nombre" : nombre_fiscalizador,
            #   "comuna": número_comuna}}

        # 6) Operadores de llamadas contratables
        ruta_operadores = os.path.join("Json", "operadores.json")
        with open(ruta_operadores, "r") as archivo:
            operadores = json.load(archivo)
            # diccionario de la forma {numero_operador: {"nombre" : nombre_fiscalizador}}

        # 7) Implementos sanitarios
        implementos = ["guantes", "mascarilla", "pantalla_facial", "delantal_quirurgico", "alcohol_gel"]

        # 8) Comunas restringidas
        ruta_comunas_vetadas = os.path.join("Json", "comunas_vetadas.json")
        with open(ruta_comunas_vetadas, "r") as file:
            comunas_vetadas = json.load(file)   
            # diccionario de la forma {numero_comuna: lista_comunas_vetadas}}



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
        ruta_costos_desp_json = os.path.join("Json", "costos_desplazamientos.json")
        with open(ruta_costos_desp_json, "r") as file:
            costos_desp = json.load(file)       ## este es CM_i,j

        costos_desp_oficial = {}
        for key in costos_desp.keys():
            key_prov = key.split(", ")
            costos_desp_oficial[(key_prov[0]), (key_prov[1])] = costos_desp[key]

        # Costo fijo asociado al fiscalizador "f" (sueldo, colación, etc.)
        caf_f = prueba[0]

        # Costo fijo asociado al operador "o" (sueldo, colación, etc.)
        cof_o = prueba[1]

        # Máximo de llamadas por hora por operador
        maxc = 5

        # Máximo de llamadas a una vivienda por día
        maxh = 2

        # Máximo de visitas a una vivienda por día
        maxv = 2

        # Costo de comprar el implemento sanitario, precio unitario
        cims = prueba[2]

        # Rendimiento específico por visita de cada implemento
        alpha = prueba[3]

        # Costo asociado a la compra y uso de test PCR
        beta = prueba[4]

        # Costo asociado a la compra y uso de test de antigeno
        gamma = prueba[5]

        # Big M
        M = 1000000000

        #### MODELO ####
        model = Model("Distribucion Fiscalizadores de Viajeros")


        #### VARIABLES ####
        K_f = model.addVars(fiscalizadores.keys(), vtype=GRB.BINARY, name="K_f")
        M_o = model.addVars(operadores.keys(), vtype=GRB.BINARY, name="M_o")
        R_htdf = model.addVars(hogares.keys(), horas, dias, fiscalizadores.keys(), vtype=GRB.BINARY, name="R_htdf")
        L_htdo = model.addVars(hogares.keys(), horas, dias, operadores.keys(), vtype=GRB.BINARY, name="L_htdo")
        V_tdfky = model.addVars(horas, dias, fiscalizadores.keys(), comunas_santiago.keys(), comunas_santiago.keys(), vtype=GRB.BINARY, name="V_tdfky")
        PCR_htdf =  model.addVars(hogares.keys(), horas, dias, fiscalizadores.keys(), vtype=GRB.BINARY, name="PCR_htdf")
        ANT_htdf = model.addVars(hogares.keys(), horas, dias, fiscalizadores.keys(), vtype=GRB.BINARY, name="ANT_htdf")
        P_tdfs = model.addVars(horas, dias, fiscalizadores.keys(), comunas_santiago.keys(), vtype=GRB.BINARY, name="P_tdfs")
        I_ad = model.addVars(implementos, dias, vtype=GRB.INTEGER, name="I_ad")
        iI_ad = model.addVars(implementos, dias, vtype=GRB.INTEGER, name="iI_ad")

        model.update()


        ### RESTRICCIONES ####
        # 1) Un fiscalizador solo puede realizar acciones si es que fue contratado
        model.addConstrs((quicksum(quicksum(R_htdf[hogar, hora, dia, fiscalizador] + PCR_htdf[hogar, hora, dia, fiscalizador]
                        + ANT_htdf[hogar, hora, dia, fiscalizador] for hogar in hogares.keys())
                        for hora in horas for dia in dias)
                        <= M * K_f[fiscalizador] for fiscalizador in fiscalizadores.keys()), name="f_contratado")

        # 2) Un operador solo puede llamar si es que fue contradado
        model.addConstrs((quicksum(L_htdo[hogar, hora, dia, operador] for dia in dias for hora in horas 
                        for hogar in hogares.keys()) <= M * M_o[operador] for operador in operadores.keys()), name="op_contratado")

        # 3) Horario de trabajo de fiscalizadores
        model.addConstrs((quicksum(R_htdf[hogar, 13, dia, fiscalizador] + R_htdf[hogar, 14, dia, fiscalizador] 
            for hogar in hogares.keys()) == 0 for dia in dias
            for fiscalizador in fiscalizadores.keys()), name="horario_fisc")

        # 4) Horario de trabajo de operadores
        model.addConstrs((quicksum(L_htdo[hogar, 13, dia, operador] + L_htdo[hogar, 14, dia, operador]   
            for hogar in hogares.keys()) == 0 for dia in dias
            for operador in operadores.keys()), name="horario_operador")

        # 5) Cantidad maxima de llamadas a una vivienda en un dia
        model.addConstrs((quicksum(L_htdo[hogar, hora, dia, operador] for hora in horas for operador in operadores.keys()) <=
                        maxh for hogar in hogares.keys() for dia in dias), name="max_hogares")

        # 6) La cantidad de implementos sanitarios a adquirir debe igualar o superar a la cantidad necesitada de estos por visita.
        model.addConstrs((quicksum(R_htdf[hogar, hora, dia, fiscalizador] for hogar in hogares.keys() for fiscalizador in fiscalizadores.keys() 
                        for hora in horas) * (1/(alpha[implemento])) <= I_ad[implemento, dia] 
                        for implemento in implementos for dia in dias), name="op_contratado")

        # 7) Inventario inicial #### d = 1
        model.addConstrs((iI_ad[implemento, 1] == 0 for implemento in implementos), name="initial_stock")

        # 8) Flujo inventario
        model.addConstrs((quicksum(R_htdf[hogar, hora, dia, fiscalizador] for hogar in hogares.keys() for fiscalizador in fiscalizadores.keys() 
                        for hora in horas) * (1/(alpha[implemento])) + iI_ad[implemento, dia] <= 
                        iI_ad[implemento, dia-1] + I_ad[implemento, dia] for implemento in implementos 
                        for dia in [2, 3, 4, 5, 6, 7]), name="flujo")

        # 9) No puede haber una llamada y una fiscalizacion a la misma hora en una misma casa
        model.addConstrs((quicksum(R_htdf[hogar, hora, dia, fiscalizador] for fiscalizador in fiscalizadores.keys()) +
                        quicksum(L_htdo[hogar, hora, dia, operador] for operador in operadores.keys()) <= 1
                        for hora in horas for hogar in hogares.keys() for dia in dias), name="redundancia")

        # 10) Un fiscalizador solo puede estar en una comuna a la vez
        model.addConstrs((quicksum(P_tdfs[hora, dia, fiscalizador, comuna] for comuna in comunas_santiago.keys())
                        == 1 for hora in horas for dia in dias for fiscalizador in fiscalizadores.keys()), name="logica_fisc")

        # 11) VAMOS A VER SI FUNCIONA
        model.addConstrs((P_tdfs[hora, dia, fiscalizador, comuna1] + P_tdfs[hora+1, dia, fiscalizador, comuna2] <= 
                        V_tdfky[hora, dia, fiscalizador, comuna1, comuna2] + 1 for hora in [8,9,10,11,12,13,14,15,16,17] 
                        for dia in dias for fiscalizador in fiscalizadores.keys() for comuna1 in comunas_santiago.keys() 
                        for comuna2 in comunas_santiago.keys() if comuna1 != comuna2), name="inicio_viaje_fisc")

        # # 14) Un fiscalizador solo puede hacer una actividad por hora
        # model.addConstrs((quicksum(R_htdf[hogar, hora, dia, fiscalizador] + quicksum(V_tdfky[hora, dia, fiscalizador, comuna1, comuna2] 
        #                   for comuna1 in comunas_santiago.keys() for comuna2 in comunas_santiago.keys()) 
        #                   for hogar in hogares.keys()) <= 1 for hora in horas for dia in dias 
        #                   for fiscalizador in fiscalizadores.keys()), name="acc_max_fisc")

        # 15) Numero maximo de llamadas por hora por operador
        model.addConstrs((quicksum(L_htdo[hogar, hora, dia, operador] for hogar in hogares.keys()) <= 
                        maxc for operador in operadores.keys() for dia in dias for hora in horas), name="max_llamadas_ph")

        # 16*) Tienen que visitar todos los días  #### NUEVA
        model.addConstrs((quicksum(R_htdf[hogar, hora, dia, fiscalizador] for hora in horas for fiscalizador
                        in fiscalizadores.keys()) == 1 for hogar in hogares.keys() for dia in dias),
                        name="temp_entre_fisc")

        # 17) Maximo de visitas por cada vivienda a fiscalizar
        model.addConstrs((quicksum(R_htdf[hogar, hora, dia, fiscalizador] for fiscalizador in fiscalizadores.keys() 
                        for hora in horas) <= maxv for hogar in hogares.keys() for dia in dias),
                        name="max_visitas_por_hogar_a_fisc")
            
        # 18) Si se hace un test PCR a un hogar h tiene que hacerse una 
        # visita a la misma hora t del dia d por el fiscalizador f
        model.addConstrs((PCR_htdf[hogar, hora, dia, fiscalizador] <= R_htdf[hogar, hora, dia, fiscalizador]
                        for hogar in hogares.keys() for hora in horas for dia in dias
                        for fiscalizador in fiscalizadores.keys()), name="PCR_visita")

        # 19) Si se hace un test de antigenos a un hogar h tiene que hacerse
        # una visita a la misma hora t del dia d por el fiscalizador f:
        model.addConstrs((ANT_htdf[hogar, hora, dia, fiscalizador] <= R_htdf[hogar, hora, dia, fiscalizador]
                        for hogar in hogares.keys() for hora in horas for dia in dias
                        for fiscalizador in fiscalizadores.keys()), name="ANT_visita")

        # 20) Se puede hacer solo una de las siguientes fiscalizaciones por hogar $h$ en cada hora $t$ 
        # en cada día d: Test PCR, test de antígeno:
        model.addConstrs((quicksum(PCR_htdf[hogar, hora, dia, fiscalizador] + ANT_htdf[hogar, hora, dia, fiscalizador] 
                        for fiscalizador in fiscalizadores.keys()) <= 1 for hogar in hogares.keys() for hora in horas for dia in dias), name="tipo_visita")

        # 21) Si se hace un test PCR en el dia x, la casa no debe recibir mas fiscalizaciones desde el dia x+2
        model.addConstrs((quicksum(quicksum(R_htdf[hogar, hora, dia + 2, fiscalizador]
            + PCR_htdf[hogar, hora, dia + 2, fiscalizador] + ANT_htdf[hogar, hora, dia + 2, fiscalizador]
            for fiscalizador in fiscalizadores.keys()) + quicksum(L_htdo[hogar, hora, dia + 2, operador]
            for operador in operadores.keys()) for hora in horas for dia in [1, 2, 3, 4, 5])
            <= M * quicksum(PCR_htdf[hogar, hora, dia, fiscalizador] for hora in horas 
            for fiscalizador in fiscalizadores.keys() for dia in [1, 2, 3, 4, 5]) 
            for hogar in hogares.keys()), name="veto_PCR")

        # 22) Si se hace un test de antígenos en el día $x$, la casa no debe recibir más fiscalizaciones desde el día x+1
        model.addConstrs((quicksum(quicksum(R_htdf[hogar, hora, dia + 1, fiscalizador]
            + PCR_htdf[hogar, hora, dia + 1, fiscalizador] + ANT_htdf[hogar, hora, dia + 1, fiscalizador]
            for fiscalizador in fiscalizadores.keys()) + quicksum(L_htdo[hogar, hora, dia + 1, operador]
            for operador in operadores.keys()) for hora in horas for dia in [1, 2, 3, 4, 5, 6])
            <= M * quicksum(ANT_htdf[hogar, hora, dia, fiscalizador]for hora in horas 
            for fiscalizador in fiscalizadores.keys() for dia in [1, 2, 3, 4, 5, 6]) 
            for hogar in hogares.keys()), name="veto_ANT")

        # 24) La suma de fiscalizaciones y llamadas debe alcanzar, al menos, el umbral de calidad
        model.addConstrs((quicksum(quicksum(R_htdf[hogar, hora, dia, fiscalizador]*calf + 
            PCR_htdf[hogar, hora, dia, fiscalizador]*calpcr +
            ANT_htdf[hogar, hora, dia, fiscalizador]*calant for fiscalizador in fiscalizadores.keys()) + 
            quicksum(L_htdo[hogar, hora, dia, operador]*call for operador in operadores.keys())
            for hora in horas for dia in dias) >= qual for hogar in hogares.keys()), name="qual_fis_llam")

        # 25) Comuna inicial de cada fizcalizador (es asignada al azar)
        model.addConstrs((P_tdfs[8, 1, fiscalizador, comuna] == 1 for comuna in comunas_santiago.keys()
            for fiscalizador in fiscalizadores if str(fiscalizadores[fiscalizador]["comuna"]) == comuna),
            name="comuna_inicial") # check

        # 26) Conexión P con R
        model.addConstrs((R_htdf[hogar, hora, dia, fiscalizador] <= P_tdfs[hora, dia, fiscalizador, comuna1]
                        for hogar in hogares.keys() for hora in horas for dia in dias for fiscalizador in fiscalizadores.keys() 
                        for comuna1 in comunas_santiago.keys() if str(hogares[hogar]["comuna"]) == comuna1),
                        name="conexion_PR")

        # 27) Llamadas mínimas a un hogar
        model.addConstrs((quicksum(L_htdo[hogar, hora, dia, operador] + L_htdo[hogar, hora, dia+1, operador] 
                for operador in operadores.keys() for hora in horas) >= 1 
                for hogar in hogares.keys() for dia in [1, 2, 3, 4, 5, 6]), name="llamadas_min")


        #### FUNCIÓN OBJETIVO ####
        obj = (quicksum(K_f[fiscalizador] * caf_f for fiscalizador in fiscalizadores.keys()) +
            quicksum(M_o[operador] * cof_o for operador in operadores.keys()) + 
            (quicksum(PCR_htdf[hogar, hora, dia, fiscalizador] for hogar in hogares.keys() for hora in horas 
            for dia in dias for fiscalizador in fiscalizadores.keys()))*beta + 
            (quicksum(ANT_htdf[hogar, hora, dia, fiscalizador] for hogar in hogares.keys() for hora in horas 
            for dia in dias for fiscalizador in fiscalizadores.keys()))*gamma + 
            quicksum(V_tdfky[hora, dia, fiscalizador, comuna_i, comuna_f] * costos_desp_oficial[(comuna_i, comuna_f)] 
            for hora in horas for dia in dias for fiscalizador in fiscalizadores.keys() for comuna_i in comunas_santiago.keys() 
            for comuna_f in comunas_santiago.keys() if comuna_i != comuna_f) + 
            quicksum(I_ad[implemento, dia] * cims[implemento] for dia in dias for implemento in implementos))
            
        model.setObjective(obj, GRB.MINIMIZE)


        #### CORRER MODELO ####
        model.Params.MIPGap = GAP_PERMITIDO 
        model.Params.TimeLimit = MAX_TIEMPO * 60
        model.optimize()


        #### MOSTRAR LOS RESULTADOS ####
        string_resultado = prueba[6]
        ruta_resultados = os.path.join("Resultados", string_resultado)
        model.write(ruta_resultados)
    except:
        print("HUBO UN ERROR")
