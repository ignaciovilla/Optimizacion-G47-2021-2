from faker import Faker
import pandas as pd
import os
import random 
import json

fake = Faker()

# primero crearemos los fiscalizadores
ruta_fisc_csv = os.path.join("Entrega 2", "nombres_fiscalizadores.csv") 
lista_nombres_fiscalizadores = []
for i in range (0 ,1000):
    lista_nombres_fiscalizadores.append(fake.name())

dict_fiscalizadores = {"Nombre" : lista_nombres_fiscalizadores}
dataframe = pd.DataFrame(data = dict_fiscalizadores)
# los guardamos en un csv
dataframe.to_csv(ruta_fisc_csv)


# ahora crearemos a los operadores
ruta_operator_csv = os.path.join("Entrega 2", "nombres_operadores.csv") 
lista_nombres_operadores = []
for i in range (0 , 500):
    lista_nombres_operadores.append(fake.name())

dict_operadores = {"Nombre" : lista_nombres_operadores}
dataframe = pd.DataFrame(data = dict_operadores)
# los guardamos en un csv
dataframe.to_csv(ruta_operator_csv)


# ahora crearemos los hogares, tienen que tener comuna y numero de personas
comunas_santiago = ["Santiago", "Conchali", "Huechuraba", "Independencia", "Quilicura", "Recoleta",
    "Renca", "Las Condes", "Lo Barnechea", "Providencia", "Vitacura", "La Reina", "Macul", "Nunoa",
    "Penalolen", "La Florida", "La Granja", "El Bosque", "La Cisterna", "La Pintana", "San Ramon",
    "Lo Espejo", "Pedro Aguirre Cerda", "San Joaquin", "San Miguel", "Cerrillos", 
    "Estacion Central", "Maipu", "Cerro Navia", "Lo Prado", "Pudahuel", "Quinta Normal"]

dict_hogares = {}
# como el promedio de personas por hogar en Chile es de 3.1, le daremos más probabilidad a que 
# las casas tengan 1, 2, 3, 4 y 5 personas 
lista_cantidad_gente = [1] * 13 + [2] * 17 + [3] * 20 + [4] * 17 + [5] * 10 + [6] * 7 + [7] * 5 + [8] * 5 + [9] * 3 + [10] * 3
for i in range(0, 10000):
    dict_hogares[i] = {"comuna" : random.choice(comunas_santiago), 
        "cant_personas" : random.choice(lista_cantidad_gente)}
ruta_hogares_json = os.path.join("Entrega 2", "hogares.json")
with open(ruta_hogares_json, "w") as outfile:
    json.dump(dict_hogares, outfile)

