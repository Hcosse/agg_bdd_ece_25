import csv
from unidecode import unidecode


# Fonction pour uniformiser les données dans un fichier CSV
def save_to_csv(data, filename="output/annonces.csv"):
    if not data:
        print("Aucune donnée à enregistrer.")
        return
    # Clés dans l'ordre souhaité
    keys = [
        "id",
        "source",
        "titre",
        "ville",
        "region",
        "type_offre",
        "telephone",
        "date_publication",
        "contact",
        "description",
        "lien_annonce",
    ]

    # Supprimer les accents
    cleaned_data = []
    for d in data:
        row = {k: unidecode(str(d.get(k, ""))) for k in keys}
        cleaned_data.append(row)
    # Écriture dans le fichier CSV
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(cleaned_data)
