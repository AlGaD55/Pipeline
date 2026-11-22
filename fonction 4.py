
import psycopg2
from getpass import getpass

mot_de_passe = getpass("Mot de passe PostgreSQL : ").encode('cp1252').decode('utf-8', errors='ignore')
connexion = psycopg2.connect(host="localhost", port=5432, dbname="Assurrisk 018",
user="postgres", password=mot_de_passe)

connexion.autocommit = True
curseur = connexion.cursor()


nom_de_table = input("nom de table :")
def combien(nom_de_table):
    curseur.execute("SELECT count(*) FROM " + nom_de_table)
    return curseur.fetchone()

print (nom_de_table, "contient", combien(nom_de_table), "lignes")