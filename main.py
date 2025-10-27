import pandas as pd

from scrapers.osteoweb_fr import get_info_remplacement
from scrapers.osteopathe_syndicat_fr import scrape_osteopathes_de_france



if __name__ == "__main__":
    print("=== Lancement des scrapers ===\n")

    data = []

    # Scraper 
    try:
        print("[1/3] Scraping osteoweb.fr ...")
        data += get_info_remplacement()
        print("Terminé : osteoweb.fr")
    except Exception as e:
        print(f"Erreur sur osteoweb.fr : {e}")

    try:
        print("[2/3] Scraping osteopathe-syndicat.fr ...")
        data += scrape_osteopathes_de_france()
        print("Terminé : osteopathe-syndicat.fr")
    except Exception as e:
        print(f"Erreur sur osteopathe-syndicat.fr : {e}")


    print(f"\nTotal d'annonces collectées : {len(data)}")

    df = pd.DataFrame(data)
    df = df.drop(columns=["id"], errors="ignore")
    df.insert(0, "id", range(1, len(df) + 1))

    # Export CSV
    output_path = r"C:\Users\hugoc\Documents\ECE\Aggregation de données\Projet final\output\annonces.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"\nExport terminé : {output_path}")
    print("\nAperçu du fichier généré :")
    print(df.head())
