import csv

personnes = {}
with open('personnes.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        personne_id, nom, prenom, id_pere, id_mere = row
        personnes[(nom, prenom)] = int(personne_id)

communes = {}
with open('communes.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        commune_id,_,nom_commune = row
        communes[nom_commune] = int(commune_id)

with open('mariages_L3.csv', mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    rows = list(csv_reader)

actes = []

for row in rows:
    if len(row) < 16:
        continue

    identifiant, type_acte, nom_A, prenom_A, _, _, _, nom_B, prenom_B, _, _, _, nom_commune, _, date, num_vue = row

    id_personneA = personnes.get((nom_A, prenom_A), None)
    id_personneB = personnes.get((nom_B, prenom_B), None)
    id_commune = communes.get(nom_commune, None)

    if id_personneA and id_commune:
        actes.append([identifiant, id_personneA, id_personneB, id_commune, type_acte, date, num_vue])

with open('actes.csv', mode='w', encoding='utf-8', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerow(["id", "id_personneA", "id_personneB", "id_commune", "type", "date", "num_vue"])
    csv_writer.writerows(actes)

print(f"Fichier actes.csv généré avec {len(actes)} enregistrements.")
