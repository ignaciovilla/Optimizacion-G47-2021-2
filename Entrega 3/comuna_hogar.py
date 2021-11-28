import json
import os
import random


# ahora crearemos los hogares, tienen que tener comuna y numero de personas
comunas_santiago = ["Santiago", "Conchali", "Huechuraba", "Independencia", "Quilicura", "Recoleta",
    "Renca", "Las Condes", "Lo Barnechea", "Providencia", "Vitacura", "La Reina", "Macul", "Nunoa",
    "Penalolen", "La Florida", "La Granja", "El Bosque", "La Cisterna", "La Pintana", "San Ramon",
    "Lo Espejo", "Pedro Aguirre Cerda", "San Joaquin", "San Miguel", "Cerrillos", 
    "Estacion Central", "Maipu", "Cerro Navia", "Lo Prado", "Pudahuel", "Quinta Normal"]


dict_hogares = {}
# como el promedio de personas por hogar en Chile es de 3.1, le daremos más probabilidad a que 
# las casas tengan 1, 2, 3, 4 y 5 personas 
# lista_cantidad_gente = [1] * 13 + [2] * 17 + [3] * 20 + [4] * 17 + [5] * 10 + [6] * 7 + [7] * 5 + [8] * 5 + [9] * 3 + [10] * 3
for i in range(0, 3000):
    comuna_hogar = random.randint(1,32)
    lista_parametros_comunas = []
    for a in range(1, 33):
        if a == comuna_hogar:
            lista_parametros_comunas.append(1)
        else:
            lista_parametros_comunas.append(0)
    dict_hogares[int(i)] = lista_parametros_comunas
ruta_hogares_json = os.path.join("Json", "hogares.json")
with open(ruta_hogares_json, "w") as outfile:
    json.dump(dict_hogares, outfile)

dict_hogares = {}
# como el promedio de personas por hogar en Chile es de 3.1, le daremos más probabilidad a que 
# las casas tengan 1, 2, 3, 4 y 5 personas 
lista_cantidad_gente = [1] * 13 + [2] * 17 + [3] * 20 + [4] * 17 + [5] * 10 + [6] * 7 + [7] * 5 + [8] * 5 + [9] * 3 + [10] * 3
for i in range(0, 4000):
    dict_hogares[i] = {"comuna" : random.choice(comunas_santiago), 
        "cant_personas" : random.choice(lista_cantidad_gente)}
ruta_hogares_json = os.path.join("Json", "hogares_v1.json")
with open(ruta_hogares_json, "w") as outfile:
    json.dump(dict_hogares, outfile)

dict_hogares = {}
for i in range(0, 125):
    comuna_hogar = int(random.randint(1,32))
    dict_individual = {"comuna": comuna_hogar}
    dict_hogares[int(i)] = dict_individual
ruta_hogares_json = os.path.join("Json", "hogares_v2.json")
with open(ruta_hogares_json, "w") as outfile:
    json.dump(dict_hogares, outfile)
