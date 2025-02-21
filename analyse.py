import csv
import re
from datetime import datetime

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
        return f"01/01/{date}"  # Ajoute jour et mois

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

# Chargement des personnes
personnes = {}
with open('personnes.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Ignorer l'en-tête
    for row in csv_reader:
        personne_id, nom, prenom, id_pere, id_mere = row
        if personne_id.lower() != "n/a":
            personnes[(nom, prenom)] = int(personne_id)

# Chargement des communes
communes = {}
with open('communes.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Ignorer l'en-tête
    for row in csv_reader:
        commune_id, nom_commune, _ = row
        if commune_id.lower() != "n/a":
            communes[nom_commune] = int(commune_id)

# Lecture du fichier des mariages
with open('mariages_L3.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    rows = list(csv_reader)

actes = []

for row in rows:
    if len(row) < 16:
        continue

    identifiant, type_acte, nom_A, prenom_A, _, _, _, nom_B, prenom_B, _, _, _, nom_commune, _, date, num_vue = row

    id_personneA = personnes.get((nom_A, prenom_A), None) if nom_A.lower() != "n/a" and prenom_A.lower() != "n/a" else None
    id_personneB = personnes.get((nom_B, prenom_B), None) if nom_B.lower() != "n/a" and prenom_B.lower() != "n/a" else None
    id_commune = communes.get(nom_commune, None) if nom_commune.lower() != "n/a" else None

    date_corrigee = corriger_date(date)

    if id_personneA and id_commune:
        actes.append([
            identifiant if identifiant.lower() != "n/a" else "",
            id_personneA,
            id_personneB if id_personneB else "",
            id_commune,
            type_acte if type_acte.lower() != "n/a" else "",
            date_corrigee,
            num_vue if num_vue.lower() != "n/a" else ""
        ])

# Écriture du fichier actes.csv
with open('actes.csv', mode='w', encoding='utf-8', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerows(actes)

print(f"Fichier actes.csv généré avec {len(actes)} enregistrements.")
