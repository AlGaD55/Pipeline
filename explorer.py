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

print(df.shape)
print()
print(df.isna().sum())
print()
print(df["montant_estime"].describe())
print()
print(df["type_sinistre"].value_counts())
print()
print("la moyenne de la franchise")
print(df["franchise"].mean())
print()
print("Le mediane de la franchise")
print(df["franchise"].median())

# print(df.groupby("type_sinistre")["franchise"].agg(["mean", "median"]))
# print(df.groupby("type_sinistre")["montant_estime"].agg(["mean", "median"]))


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
#qu'il existe des valeurs extremes qui la tirent à la hausse. Mais dans l'analyse par type, la moyenne et médianne 
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

print(df["type_sinistre"].value_counts(normalize=True).mul(100).round(1))

print()
print()

print("verification hypothese groupee")
part = (df.groupby("ville_sinistre")["type_sinistre"]
          .apply(lambda s: s.value_counts(normalize=True).mul(100).round(1)))
print(part.xs("Dégât des eaux", level=1).describe())

print()
print()

print("Lille")
lille = df[df["ville_sinistre"]=="lille"]
print(lille["type_sinistre"].value_counts(normalize=True).mul(100).round(1))

print()
print("Metz")
Metz = df[df["ville_sinistre"]=="Metz"]
print(Metz["type_sinistre"].value_counts(normalize=True).mul(100).round(1))

print()
print()

print("Nice")
Nice = df[df["ville_sinistre"]=="Nice"]
print(Nice["type_sinistre"].value_counts(normalize=True).mul(100).round(1))


print()
print()

print("Rennes")
Rennes = df[df["ville_sinistre"]=="Rennes"]
print(Rennes["type_sinistre"].value_counts(normalize=True).mul(100).round(1))

print()
print()
print("Enquetes octobre")


octobre = df[(df["date_survenance"] >= "2025-10-01") & 
             (df["date_survenance"] <= "2025-10-31")]
reste = df[~df.index.isin(octobre.index)]

# Vérification des effectifs (doit afficher 1940 et 10158)
print(len(octobre), len(reste))

#Étape 2 : Comparer les proportions (%) de chaque type de sinistre
# Calcul des parts en % pour octobre et pour le reste
octobre_pct = octobre["type_sinistre"].value_counts(normalize=True).mul(100).round(1)
reste_pct = reste["type_sinistre"].value_counts(normalize=True).mul(100).round(1)

# Tableau comparatif côte à côte
comparaison_types = pd.DataFrame({
    "Octobre 2025 (%)": octobre_pct,
    "Reste de l'année (%)": reste_pct
})
print("comparaison_types",comparaison_types)

# 2. Comparaison des statistiques météo (moyenne, max, quartiles)

print("--- Métriques météo en Octobre 2025 ---")
print(octobre[["precipitation_sum", "wind_gusts_10m_max"]].describe())

print("\n--- Métriques météo le Reste de l'année ---")
print(reste[["precipitation_sum", "wind_gusts_10m_max"]].describe())

# Exploration du Point 3 : La distribution jour par jour

# Comptage du nombre de sinistres par jour du mois (du 1er au 31 octobre)

par_jour = octobre.groupby(octobre["date_survenance"].dt.day).size()

print("--- Nombre de sinistres par jour en octobre ---")
print(par_jour)

print("\n--- Statistiques sur la distribution quotidienne ---")
print(par_jour.describe())

# Exploration du Point bonus : comparaison geographique repartition par region

#  Calcul des parts (%) par région
octobre_reg = octobre["region_sinistre"].value_counts(normalize=True).mul(100).round(1)
reste_reg = reste["region_sinistre"].value_counts(normalize=True).mul(100).round(1)

#  Tableau comparatif
comparaison_regions = pd.DataFrame({
    "Octobre 2025 (%)": octobre_reg,
    "Reste de l'année (%)": reste_reg
})
print(comparaison_regions)



# Mercredi 18 Novembre Exercice 2
#--------------------------------

# Enquete personnelle : choix date declaration

###  ** Calcul du délai en jours entre la survenance et la déclaration
delai = (df["date_declaration"] - df["date_survenance"]).dt.days
print()
print()
print("calcul des delais")
print(delai.describe())

### **2. Ce qu'il faut observer dans les résultats**

# calcul des delais
#---------------------

# count    12098.000000
# mean        13.867664
# std          7.847060
# min          1.000000
# 25%          7.000000
# 50%         14.000000
# 75%         21.000000
# max         27.000000

print()
print()

print(df[["montant_estime", "precipitation_sum", 
    "wind_gusts_10m_max", "temperature_2m_max"]].corr())

print()
