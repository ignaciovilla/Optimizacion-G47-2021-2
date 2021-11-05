import json
import os
import random

dict_hogares = {}
# como el promedio de personas por hogar en Chile es de 3.1, le daremos más probabilidad a que 
# las casas tengan 1, 2, 3, 4 y 5 personas 
# lista_cantidad_gente = [1] * 13 + [2] * 17 + [3] * 20 + [4] * 17 + [5] * 10 + [6] * 7 + [7] * 5 + [8] * 5 + [9] * 3 + [10] * 3
for i in range(0, 10):
    comuna_hogar = random.randint(1,32)
    lista_parametros_comunas = []
    for a in range(1, 33):
        if a == comuna_hogar:
            lista_parametros_comunas.append(1)
        else:
            lista_parametros_comunas.append(0)
    dict_hogares[int(i)] = lista_parametros_comunas
ruta_hogares_json = os.path.join("Entrega 2", "hogares.json")
with open(ruta_hogares_json, "w") as outfile:
    json.dump(dict_hogares, outfile)

