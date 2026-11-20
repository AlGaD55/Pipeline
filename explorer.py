# import pandas as pd
# import psycopg2
# import warnings
# from getpass import getpass



# warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")
# pd.set_option("display.width", 200)
# pd.set_option("display.max_columns", 30)

# #mot_de_passe = getpass.getpass("Mot de passe PostgreSQL : ")


# mot_de_passe = getpass.getpass("Mot de passe PostgreSQL : ").encode('cp1252').decode('utf-8', errors='ignore')
# # mot_de_passe = getpass.getpass("Mot de passe PostgreSQL : ").encode('cp1252').decode('utf-8', errors='ignore')
# # mot_de_passe = getpass("Mot de passe PostgreSQL : ").encode('cp1252').decode('utf-8', errors='ignore')

# #connexion = psycopg2.connect(host="localhost", port=5432, dbname="Assurrisk017",
# #user="postgres", password=mot_de_passe)
# #client_encoding=utf8
# mot_de_passe = getpass("Mot de passe PostgreSQL : ").encode('cp1252').decode('utf-8', errors='ignore')
# df = pd.read_sql("SELECT * FROM fact_sinistre_meteo", connexion)
# connexion = psycopg2.connect(
#     "dbname=Assurrisk017 user=postgres password=2109@&372 host=localhost port=5432 client_encoding=utf8")

# df["montant_estime"] = df["montant_estime"].astype(float)
# df["franchise"] = df["franchise"].astype(float)
# df["date_survenance"] = pd.to_datetime(df["date_survenance"])
# df["date_declaration"] = pd.to_datetime(df["date_declaration"])



import pandas as pd
import psycopg2
import warnings
from getpass import getpass

warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)
mot_de_passe = getpass("Mot de passe PostgreSQL : ")
import psycopg2
connexion = psycopg2.connect(host="localhost", port=5432, dbname="Assurrisk010",
user="postgres", password=mot_de_passe)

# connexion.autocommit = True
# connexion = psycopg2.connect(
#     "dbname=Assurrisk017 user=postgres password=2109@&372 host=localhost port=5432 client_encoding=utf8"
# )
df = pd.read_sql("SELECT * FROM fact_sinistre_meteo", connexion)
df["montant_estime"] = df["montant_estime"].astype(float)
df["franchise"] = df["franchise"].astype(float)
df["date_survenance"] = pd.to_datetime(df["date_survenance"])
df["date_declaration"] = pd.to_datetime(df["date_declaration"])

#1. Combien de lignes et combien de colonnes compte la table ?
#-------------------------------------------------------------

#print(df.shape)
#(12098, 18)

#2. Y a-t-il des valeurs manquantes ? Si oui, dans quelles colonnes ?
#--------------------------------------------------------------------

# print(df.isna().sum())
# print("Total valeurs manquantes :", df.isna().sum().sum())


#print(df.isna().sum())

# sinistre_id             0
# contrat_id              0
# agence_id               0
# garantie_id             0
# date_survenance         0
# date_declaration        0
# type_sinistre           0
# statut_sinistre         0
# montant_estime          0
# franchise               0
# ville_sinistre          0
# departement_sinistre    0
# region_sinistre         0
# weather_code            0
# temperature_2m_max      0
# temperature_2m_min      0
# precipitation_sum       0
# wind_gusts_10m_max      0

#3. Quel est le montant le plus faible de la table, et le plus élevé ?
#---------------------------------------------------------------------

# montant_min = df["montant_estime"].min()
# montant_max = df["montant_estime"].max()
# print(montant_min)
# print(montant_max)


# 80.0
# 49912.0

#4. Combien de types de sinistre différents y a-t-il ?
#------------------------------------------------------


# nb_types = df["type_sinistre"].value_counts()
# print(f"Nombre de types de sinistres différents : {nb_types}")

# Nombre de types de sinistres différents : type_sinistre
# Dégât des eaux           3526
# Vol                      2115
# Grêle                    1608
# Tempête                  1526
# Bris de glace            1416
# Responsabilité civile     899
# Incendie                  608
# Inondation                400
# Name: count, dtype: int64



# Nombre de types de sinistres différents : 8


#5. Quelle est la moyenne et la médiane de la colonne franchise ?
#----------------------------------------------------------------

# moyenne_franchise = df["franchise"].mean()
# mediane_franchise = df["franchise"].median()

# print(f"Franchise moyenne : {moyenne_franchise:,.2f} €")
# print(f"Franchise médiane : {mediane_franchise:,.2f} €")

# Franchise moyenne : 228.70 €
# Franchise médiane : 200.00 €

# group by sur la franchise
#---------------------------


# stats_franchise = df.groupby("type_sinistre")["franchise"].agg(
#     Moyenne="mean",
#     Mediane="median"
# ).reset_index()

# # Afficher le résultat
# print(stats_franchise)

#  type_sinistre     Moyenne  Mediane
# 0          Bris de glace   81.355932     80.0
# 1         Dégât des eaux  299.262621    300.0
# 2                  Grêle  200.000000    200.0
# 3               Incendie  496.052632    500.0
# 4             Inondation  500.000000    500.0
# 5  Responsabilité civile    0.000000      0.0
# 6                Tempête  298.296199    300.0
# 7                    Vol  150.378251    150.0


# Observations : au niveau global la moyenne est supérieur à la médiane, ce qui signifie
#qu'il existe des valeurs extremes qui la tirent à la hausse. Mais dans le détail, la moyenne et médianne 
# sont équivalentes

# stat_montant_estime = df.groupby("type_sinistre")["montant_estime"].agg(
#     Moyenne="mean",
#     Mediane="median"
# ).reset_index()

# print(stat_montant_estime)


# type_sinistre       Moyenne  Mediane
# 0          Bris de glace    677.911017    671.5
# 1         Dégât des eaux   4478.319909   4464.5
# 2                  Grêle   3333.384950   3255.0
# 3               Incendie  27548.103618  26957.0
# 4             Inondation  18111.012500  18306.5
# 5  Responsabilité civile   2597.454950   2543.0
# 6                Tempête  11477.944954  11288.5
# 7                    Vol   7688.765957   7611.0
#print(df.value_counts())


# Exercice 2
#-------------

#print(df.shape)
#print(df.head())
#print(df.isna().sum())
#df["type_sinistre"].describe()

# df.groupby("type_sinistre")["montant_estime"].agg(["count","mean","median"])\
# .sort_values("median",ascending=False)
# print(df)