

import psycopg2
from getpass import getpass
import time
import pandas as pd
import json
import io
import os
#from tabulate import tabulate


os.makedirs("sorties", exist_ok=True)


#==========================================
## Connexion à la base de donnée Dbeaver
#==========================================

#mot_de_passe = getpass("Mot de passe PostgreSQL : ")
#mot_de_passe = getpass("Mot de passe PostgreSQL : ").encode().decode("utf-8")
mot_de_passe = getpass("Mot de passe PostgreSQL : ").encode('cp1252').decode('utf-8', errors='ignore')

#connexion = psycopg2.connect(host="localhost", port=5432, dbname="Assurrisk 018",
#user="postgres", password=mot_de_passe)
connexion = psycopg2.connect(
    "dbname=Assurrisk017 user=postgres password=2109@&372 host=localhost port=5432 client_encoding=utf8")
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
("01_init.sql", "Reinitialiser la base"),
("02_clean.sql", "Construire la couche propre"),   
("03_tables_meteo.sql", "Creer les tables qui attendent la meteo"),
]



for fichier, libelle in etapes_1:
    debut = time.time ()
    requete = open("sql/" + fichier, encoding="utf-8").read()
    curseur.execute(requete)
    duree=round(time.time() - debut,1)
    journal.append([fichier,libelle,"SQL",duree])
    print(" [SQL]", libelle,"-",duree, "s")




#=================================================
## Etapes PYTHON
#=================================================

## 001 Chargement du fichier json creation DataFrame

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

## 002 Copie du fichier json dans la table meteo_assurrisk

tampon = io.StringIO()
meteo.to_csv(tampon, index=False, header=False)
tampon.seek(0)
curseur.copy_expert("COPY meteo_assurrisk FROM STDIN WITH (FORMAT csv)", tampon)
print(" [PYTHON]", len(meteo), "lignes de meteo chargees")

## 003 Copie des fichiers csv dans table villes_coordonnees_meteo

ville = pd.read_csv ("donnees/villes_coordonnees_meteo.csv")
print(ville.shape)

tampon = io.StringIO ()
ville.to_csv(tampon,index=False,header=False)
tampon.seek(0)
curseur.copy_expert("COPY villes_coordonnees_meteo FROM STDIN WITH (FORMAT csv)",tampon)
print("[PYTHON]", len(ville),"lignes chargees")


#====================================================
# Suite Etapes  Execution des scripts SQL 04 à 06
#====================================================

etapes_2 = []

etapes_2.append(("04_rattachement.sql", "Rattacher les points meteo aux villes"))
etapes_2.append(("05_croisement.sql","Croise les sinistres avec la meteo"))
etapes_2.append(("06_controles.sql","Controle le rapprochement"))


for fichier, libelle in etapes_2:
    debut = time.time()
    requete = open("sql/" + fichier, encoding="utf-8").read()
    curseur.execute(requete)
    duree = round(time.time() - debut, 1)
    journal.append([fichier, libelle, "SQL", duree])
    print(" [SQL]", libelle, "-", duree, "s")


## Controle verification bonne execution sql

    if fichier == "02_clean.sql":
        verification = pd.read_sql(
        "SELECT count(*) AS n FROM clean_fact_sinistre", connexion)
        print(" [CONTRÔLE] clean_fact_sinistre =", verification["n"][0], "lignes")

    

#===========================================
## Creation de fichier journal du Pipeline
#===========================================

suivi = pd.DataFrame(journal, columns=["fichier", "etape", "outil", "secondes"])
suivi.to_csv("sorties/journal_pipeline.csv_version_finale", sep=";", decimal=",",
index=False, encoding="utf-8-sig")



#=======================================
## Execution des différents Contrôles
#=======================================

controles = pd.read_sql("""
    SELECT (SELECT count(*) FROM clean_fact_sinistre)                           AS sinistres_propres,
           (SELECT count(*) FROM meteo_assurrisk)                               AS lignes_meteo,
           (SELECT count(DISTINCT ville) FROM meteo_assurrisk_ville)            AS villes_meteo,
           (SELECT count(*) FROM fact_sinistre_meteo)                           AS lignes_finales,
           (SELECT count(*) FROM fact_sinistre_meteo WHERE weather_code IS NULL) AS sans_meteo,
           (SELECT count(*) FROM (SELECT ville, time FROM meteo_assurrisk_ville
                                  GROUP BY 1,2 HAVING count(*) > 1) z)          AS meteo_en_double
""", connexion)

print()
# print("CONTROLES")
# for colonne in controles.columns:
#     print("   ", colonne, ":", controles[colonne][0])



print("\nCONTROLES")
print(tabulate(controles, headers="keys", tablefmt="psql", showindex=False))

#=============================================
## Creation du fichier journal controle csv
#=============================================


controles.to_csv("sorties/controles.csv_version_finale", sep=";", decimal=",",
                 index=False, encoding="utf-8-sig")

curseur.close()
connexion.close()














# verification = pd.read_sql("SELECT count(*) AS n FROM clean_fact_sinistre", connexion)
# print(" controle : clean_fact_sinistre =", verification["n"][0], "lignes")