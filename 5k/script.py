import csv
import re
from datetime import datetime

### 🔹 Fonction de correction des dates
def corriger_date(date):
    if not date or date.lower() == "n/a":
        return ""

    # Vérifier si la date est une plage (ex: "1668-1669")
    match = re.match(r"(\d{4})-(\d{4})", date)
    if match:
        annee1, annee2 = map(int, match.groups())
        annee_moyenne = str((annee1 + annee2) // 2)
        return f"01/01/{annee_moyenne}"

    # Vérifier si la date est seulement une année (ex: "1675")
    match = re.match(r"^\d{4}$", date)
    if match:
        return f"01/01/{date}"

    # Vérifier le format JJ/MM/AAAA
    match = re.match(r"(\d{2})/(\d{2})/(\d{4})", date)
    if match:
        jour, mois, annee = map(int, match.groups())

        # Corriger jour ou mois à 01 si c'est 00
        if jour == 0:
            jour = 1
        if mois == 0:
            mois = 1

        # Vérifier si la date est valide
        try:
            datetime(annee, mois, jour)  # Test si la date est valide
        except ValueError:
            return ""

        return f"{jour:02d}/{mois:02d}/{annee}"
    else:
        return ""

### 🔹 Lecture du fichier des mariages et extraction des données
personnes = {}
person_id = 1

communes = {}
commune_id = 1

departements = {}
departement_id = 1

commune_to_departement = {}  # Associe chaque id_commune à son id_departement

actes = []

with open('mariages_L3_5k.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    rows = list(csv_reader)

    for row in rows:
        if len(row) < 16:
            continue

        identifiant, type_acte, nom_A, prenom_A, prenom_pere_A, nom_mere_A, prenom_mere_A, \
        nom_B, prenom_B, prenom_pere_B, nom_mere_B, prenom_mere_B, nom_commune, departement, date, num_vue = row[:16]

        ### 🔹 Gestion des personnes
        def ajouter_personne(nom, prenom, prenom_pere, nom_mere, prenom_mere):
            global person_id
            key = (nom, prenom, nom_mere, prenom_mere)

            if key not in personnes:
                personnes[key] = person_id  # Stocke seulement l'ID
                person_id += 1

        ajouter_personne(nom_A, prenom_A, prenom_pere_A, nom_mere_A, prenom_mere_A)
        ajouter_personne(nom_B, prenom_B, prenom_pere_B, nom_mere_B, prenom_mere_B)

        id_personneA = personnes.get((nom_A, prenom_A, nom_mere_A, prenom_mere_A), None)
        id_personneB = personnes.get((nom_B, prenom_B, nom_mere_B, prenom_mere_B), None)

        ### 🔹 Gestion des communes et départements
        if nom_commune.lower() != "n/a":
            if nom_commune not in communes:
                communes[nom_commune] = commune_id  # Stocke l'ID
                commune_to_departement[commune_id] = int(departement) if departement.lower() != "n/a" else None
                commune_id += 1

        id_commune = communes.get(nom_commune, None)

        if departement.lower() != "n/a" and departement not in departements:
            departements[departement] = departement_id
            departement_id += 1

        ### 🔹 Correction des dates
        date_corrigee = corriger_date(date)

        ### 🔹 Ajout des actes si le département est valide
        if id_personneA and id_commune and id_commune in commune_to_departement:
            id_departement = commune_to_departement[id_commune]

            if id_departement in [44, 49, 79, 85]:  # Vérifie si le département est valide
                actes.append([
                    identifiant if identifiant.lower() != "n/a" else "",
                    id_personneA,
                    id_personneB if id_personneB else "",
                    id_commune,
                    type_acte if type_acte.lower() != "n/a" else "",
                    date_corrigee,
                    num_vue if num_vue.lower() != "n/a" else ""
                ])

### 🔹 Écriture des fichiers

# 🔸 Sauvegarde des personnes
with open('personnes.csv', mode='w', encoding='utf-8', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    for (nom, prenom, _, _), id_personne in personnes.items():
        csv_writer.writerow([id_personne, nom, prenom])

print(f"Fichier personnes.csv généré avec {len(personnes)} personnes.")

# 🔸 Sauvegarde des communes
with open('communes.csv', mode='w', encoding='utf-8', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    for nom_commune, id_commune in communes.items():
        csv_writer.writerow([id_commune, nom_commune, commune_to_departement[id_commune]])

print(f"Fichier communes.csv généré avec {len(communes)} communes.")

# 🔸 Sauvegarde des départements
with open('departements.csv', mode='w', encoding='utf-8', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    for nom_departement, id_departement in departements.items():
        csv_writer.writerow([id_departement, nom_departement])

print(f"Fichier departements.csv généré avec {len(departements)} départements.")

# 🔸 Sauvegarde des actes
with open('actes.csv', mode='w', encoding='utf-8', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerows(actes)

print(f"Fichier actes.csv généré avec {len(actes)} enregistrements.")
