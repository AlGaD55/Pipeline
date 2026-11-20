import psycopg2
from getpass import getpass
import json
import pandas as pd
import io





meteo_brute = json.load(open("donnees/meteo_30_villes.json", encoding="utf-8"))
print(type(meteo_brute)) # une LISTE
print(len(meteo_brute)) # de combien d'objets ?
print(meteo_brute[0].keys()) # que contient le premier ?

morceaux = []

for localisation in meteo_brute:
    tableau = pd.DataFrame(localisation["daily"])
    tableau["latitude"] = localisation["latitude"]
    tableau["longitude"] = localisation["longitude"]
    morceaux.append(tableau)

meteo = pd.concat(morceaux, ignore_index=True)
print(meteo.shape)
nbre_ligne = len(meteo)
print(nbre_ligne)

## connexion à la base de données

# mot_de_passe = getpass("Mot de passe PostgreSQL : ")

# connexion = psycopg2.connect(host="localhost", port=5432, dbname="Assurrisk08",
# user="postgres", password=mot_de_passe)

# connexion.autocommit = True
# curseur = connexion.cursor()
# print("connexion ouverte")

# tampon = io.StringIO()
# meteo.to_csv(tampon, index=False, header=False)
# tampon.seek(0)
# curseur.copy_expert("COPY meteo_assurrisk FROM STDIN WITH (FORMAT csv)", tampon)
# print(" [PYTHON]", len(meteo), "lignes de meteo chargees")

# tampon = io.StringIO()
# meteo.to_csv(tampon, index=False, header=False)
# tampon.seek(0)
# curseur.copy_expert("COPY meteo_assurrisk FROM STDIN WITH (FORMAT csv)", tampon)
# print(" [PYTHON]", len(meteo), "lignes de meteo chargees")