import os
import json

path_comunas = os.path.join("Entrega 2", "comunas_santiago.csv")

dict_comunas = {}
dict_comunas_vetadas = {}
with open(path_comunas, "r") as file:
    lineas = file.readlines()
    for linea in lineas:
        linea = linea.strip().split(",")
        if "Comuna" in linea[1]:
            pass
        
        else:
            dict_comunas[int(linea[0])] = linea[1]
            linea[2] = linea[2].replace('\"', "")
            linea[-1] = linea[-1].replace('\"', "")

            lista_vetada = []
            for i in range(2, len(linea)):
                lista_vetada.append(int(linea[i]))
            dict_comunas_vetadas[int(linea[0])] = lista_vetada

ruta_comunas = os.path.join("Entrega 2", "comunas.json")
ruta_comunas_vetadas = os.path.join("Entrega 2", "comunas_vetadas.json")

with open(ruta_comunas, "w") as outfile:
    json.dump(dict_comunas, outfile)

with open(ruta_comunas_vetadas, "w") as chaofile:
    json.dump(dict_comunas_vetadas, chaofile)
