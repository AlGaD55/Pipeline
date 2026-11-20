import psycopg2
from getpass import getpass
import time
import pandas as pd
import json
import io


mot_de_passe = getpass("Mot de passe PostgreSQL : ")

connexion = psycopg2.connect(host="localhost", port=5432, dbname="Assurrisk010",
user="postgres", password=mot_de_passe)

connexion.autocommit = True
curseur = connexion.cursor()
print("connexion ouverte")

requete = open("sql/01_init.sql", encoding="utf-8").read()
curseur.execute(requete)
print("base reinitialisee")



etapes = [
("01_init.sql", "Reinitialiser la base"),
("02_clean.sql", "Construire la couche propre"),
("03_tables_meteo.sql", "Creer les tables qui attendent la meteo"),
]

#etapes.append(("04_rattachement.sql", "Rattacher les points meteo aux villes"))
#etapes.append(("05_croisement.sql","Croise les sinistres avec la meteo"))
#etapes.append(("06_controles.sql","Controle le rapprochement"))

for fichier, libelle in etapes:
    requete = open("sql/" + fichier, encoding="utf-8").read()
    curseur.execute(requete)
    print(" [SQL]", libelle)

##
## Etapes PYTHON
## Chargement du fichier json

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

## copie du fichier json

tampon = io.StringIO()
meteo.to_csv(tampon, index=False, header=False)
tampon.seek(0)
curseur.copy_expert("COPY meteo_assurrisk FROM STDIN WITH (FORMAT csv)", tampon)
print(" [PYTHON]", len(meteo), "lignes de meteo chargees")

## copie des fichiers csv

ville = pd.read_csv ("donnees/villes_coordonnees_meteo.csv")
print(ville.shape)

tampon = io.StringIO ()
ville.to_csv(tampon,index=False,header=False)
tampon.seek(0)
curseur.copy_expert("COPY villes_coordonnees_meteo FROM STDIN WITH (FORMAT csv)",tampon)
print("[PYTHON]", len(ville),"lignes chargees")

#### Suite Etapes

etapes = []

etapes.append(("04_rattachement.sql", "Rattacher les points meteo aux villes"))
etapes.append(("05_croisement.sql","Croise les sinistres avec la meteo"))
etapes.append(("06_controles.sql","Controle le rapprochement"))

for fichier, libelle in etapes:
    requete = open("sql/" + fichier, encoding="utf-8").read()
    curseur.execute(requete)
    print(" [SQL]", libelle)


journal = []

for fichier, libelle in etapes:
    debut = time.time()
    requete = open("sql/" + fichier, encoding="utf-8").read()
    curseur.execute(requete)
    duree = round(time.time() - debut, 1)
    journal.append([fichier, libelle, "SQL", duree])
    print(" [SQL]", libelle, "-", duree, "s")

    if fichier == "02_clean.sql":
        verification = pd.read_sql(
        "SELECT count(*) AS n FROM clean_fact_sinistre", connexion)
        print(" [CONTRÔLE] clean_fact_sinistre =", verification["n"][0], "lignes")

    # if fichier == "04_rattachement.sql":
    #     verification = pd.read_sql("SELECT count(*) AS n FROM ", connexion)
    #     print(" [CONTRÔLE] rattachement =", verification["n"][0], "lignes")

suivi = pd.DataFrame(journal, columns=["fichier", "etape", "outil", "secondes"])
suivi.to_csv("sorties/journal_pipeline.csv02", sep=";", decimal=",",
index=False, encoding="utf-8-sig")











# suivi = pd.DataFrame(journal, columns=["fichier", "etape", "outil", "secondes"])
# suivi.to_csv("sorties/journal_pipeline.csv", sep=";", decimal=",",
# index=False, encoding="utf-8-sig")

# verification = pd.read_sql("SELECT count(*) AS n FROM clean_fact_sinistre", connexion)
# print(" controle : clean_fact_sinistre =", verification["n"][0], "lignes")