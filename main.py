import numpy as np
from som import SOM
from mongoInterface import MongoInterface
from dataTreatment import *

# Recupera la data de la BD
print("...Conectado a la base de datos...")
conn = MongoInterface(dbname='video')

# Filtro y proyección MONGO
filtro = {
    '$and': [
        { 
            'tomato.rating': { '$exists': True  },
            'awards.wins': { '$exists': True }
        }
    ] 
}

projection = {
    '_id': False,
    'title': True,
    'runtime': True,
    'metacritic': True,
    'tomato.rating': True,
    'year': True,
    'awards.wins': True
}

brute_data = conn.find_docs(collec='movieDetails', f=filtro, p=projection)
print("...Recuperados datos en bruto...")

# Limpia y estandariza la data
clean_data = cleaner(brute_data)
data = [list(map(standarize, lst)) for lst in clean_data]

print("...Creando una SOM...")
topo = len(data[0])
red = SOM(100, 100, topo)

print("...Entrenando la red...")
red.train(clean_data, L0=0.8, lam=1e2, sigma0=10)

print("...Construyendo gráfico en 2D...")
for p in red.som:
    build_JSON_coor(p, 'son_map')

print("...Calculando el error de cálculo...")
print(red.quant_err())
