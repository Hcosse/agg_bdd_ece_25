import csv
from unidecode import unidecode


def save_to_csv(data, filename="output/annonces.csv"):
    if not data:
        print("Aucune donnée à enregistrer.")
        return

    keys = ["id", "source", "titre", "ville", "region", "type_offre", "date_debut", "date_publication", "duree", "description", "lien_annonce"]

    # Supprimer les accents
    cleaned_data = []
    for d in data:
        row = {k: unidecode(str(d.get(k, ""))) for k in keys}
        cleaned_data.append(row)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(cleaned_data)
