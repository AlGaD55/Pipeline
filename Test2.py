import psycopg2
from getpass import getpass
import time
import pandas as pd
import json
import io
import os
from tabulate import tabulate

os.makedirs("sorties", exist_ok=True)


#==========================================
## Connexion à la base de donnée Dbeaver
#==========================================

mot_de_passe = getpass("Mot de passe PostgreSQL : ")

connexion = psycopg2.connect(host="localhost", port=5432, dbname="Assurrisk018",
user="postgres", password=mot_de_passe)

connexion.autocommit = True
curseur = connexion.cursor()
print("connexion ouverte")

requete = open("sql/01_init.sql", encoding="utf-8").read()
curseur.execute(requete)
print("base reinitialisee")



#===============================================
## Execution des scripts SQL 01 à 03
#===============================================

journal = []


etapes_1 = [
("02_clean.sql", "Construire la couche propre"),
("01_init.sql", "Reinitialiser la base"),
("03_tables_meteo.sql", "Creer les tables qui attendent la meteo"),
]



for fichier, libelle in etapes_1:
    debut = time.time ()
    requete = open("sql/" + fichier, encoding="utf-8").read()
    curseur.execute(requete)
    duree=round(time.time() - debut,1)
    journal.append([fichier,libelle,"SQL",duree])
    print(" [SQL]", libelle,"-",duree, "s")