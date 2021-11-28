###### Fórmula y código extraído de 
# https://www.kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python

import math
import os
import json

def formula_haversine(x_1, y_1, x_2, y_2):
    R = 6373                # radio de la tierra en km

    lat1 = math.radians(x_1)
    lon1 = math.radians(y_1)

    lat2 = math.radians(x_2)
    lon2 = math.radians(y_2)

    dlon = lon2 - lon1
    
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distancia = R*c

    return distancia


lista_coordenadas = []
path_coordenadas = os.path.join("Excel", "coordenadas_comunas.csv")
with open(path_coordenadas, "r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip().split(",")
        line[1] = line[1].replace('\"', '')
        line[2] = line[2].replace('\"', '')
        if "lat" in line[1]:
            pass
        else:
            lista_coordenadas.append([line[0], float(line[1]), float(line[2])])

dict_distancias = {}
for i in range(0, len(lista_coordenadas)):
    for a in range (0, len(lista_coordenadas)):
        dict_distancias[f"{lista_coordenadas[i][0]}, {lista_coordenadas[a][0]}"] = formula_haversine(
            lista_coordenadas[i][1], lista_coordenadas[i][2], lista_coordenadas[a][1],
            lista_coordenadas[a][2])

# precio original 78.767 pesos por km
pesos_por_km = 78.767
dict_costos_por_desp = {}
for key in dict_distancias.keys():
    dict_costos_por_desp[key] = dict_distancias[key] * pesos_por_km


ruta_costos_desp_json = os.path.join("Json", "costos_desplazamientos.json")
with open(ruta_costos_desp_json, "w") as outfile:
    json.dump(dict_costos_por_desp, outfile)