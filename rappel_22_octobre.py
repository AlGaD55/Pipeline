# -*- coding: utf-8 -*-
# =====================================================================
# Rappel du 22 octobre — la liste, le dictionnaire, la boucle
#
# Ce fichier ne se connecte a RIEN : ni base, ni internet, ni pandas.
# Il tourne meme si votre installation Python est cassee ce matin.
#
# Lancez-le, lisez la sortie a cote du fichier, puis modifiez-le.
# =====================================================================
print()
print()
print()
print()

## La liste

print("=" * 58)
print(" 1. LA LISTE — plusieurs valeurs, dans l'ordre")
print("=" * 58)

print()
print()

etapes = ["Reinitialiser la base",
          "Construire la couche propre",
          "Charger la meteo",
          "Croiser sinistres et meteo"]
print()
print("la liste entiere :", etapes)
print("combien          :", len(etapes))
print("la premiere      :", etapes[0])      # on compte a partir de ZERO
print("la derniere      :", etapes[-1])

etapes.append("Controler le resultat")
etapes.append("generer rapport BI")

print()
print("apres append     :", len(etapes), "etapes")
print("apres append dernière etape :",etapes[-1])
print()
print("etapes[0] :",etapes[0])
print("etapes[1] :",etapes[1])
print("etapes[4] :",etapes[4])
#print("etapes[12]) :",etapes[12])

print()
print()
print()

## Le dictionnaire

print("=" * 58)
print(" 2. LE DICTIONNAIRE — une cle, une valeur")
print("=" * 58)

print()
print()


fichiers = {"Reinitialiser la base":       "assurrisk_init_2024_2025.sql",
            "Construire la couche propre": "assurrisk_clean.sql",
            "Croiser sinistres et meteo":  "croisement_meteo.sql"}

fichiers["controle le rapprochement"]="controle_rapprochement.sql"

print("combien de paires :", len(fichiers))
print("fichier pour 'Construire la couche propre' :",
      fichiers["Construire la couche propre"])
print()
print("toutes les cles   :", list(fichiers.keys()))


print()
print()

## La boucle

print("=" * 58)
print(" 3. LA BOUCLE — faire la meme chose pour chaque valeur")
print("=" * 58)
print()
print()


print("\n-- sur une liste --")
for etape in etapes:
    print("   a faire :", etape)

print("\n-- sur un dictionnaire : il faut .items() --")
for etape, fichier in fichiers.items():
    print("  ", etape, "->", fichier)


print()
print()
print()

## Utilité de la boucle

print("=" * 58)
print(" 4. CE QUE LA BOUCLE REMPLACE")
print("=" * 58)

print("\nSANS boucle, il faudrait ecrire une ligne par etape :")
print("   print(etapes[0])")
print("   print(etapes[1])")
print("   print(etapes[2])   ... et ainsi de suite")

print()
print()

print("\nAVEC la boucle, on ecrit la ligne UNE fois.")
print("-> Ajouter une 6e etape coute UNE ligne dans la liste,")
print("   et rien du tout dans la boucle.")

print()
print()

print("Cette semaine, chaque 'etape' sera un fichier .sql")
print("que Python ira executer. La structure, elle, ne change pas.")

