import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from api.localisation import get_ville_info

def scrape_osteopathe_syndicat():
    base_url = "https://www.osteopathe-syndicat.fr"
    start_url = f"{base_url}/annonces-osteopathe"

    r = requests.get(start_url)
    soup = BeautifulSoup(r.text, "html.parser")

    annonces = []

    # tous les <li>
    for li in soup.select("ul.listingAnnonce li"):
        try:
            date_bloc = li.select_one("div.date")
            lignes = date_bloc.get_text(separator="\n", strip=True).split("\n")
            date_publication = datetime.strptime(lignes[0], "%d/%m/%Y").date().isoformat() if lignes else ""
            type_offre = lignes[1] if len(lignes) > 1 else ""
            region = lignes[2] if len(lignes) > 2 else ""

            titre_tag = li.select_one("h2 a")
            titre = titre_tag.get_text(strip=True)
            lien_annonce = titre_tag["href"]

            r_detail = requests.get(lien_annonce)
            soup_detail = BeautifulSoup(r_detail.text, "html.parser")
            description_bloc = soup_detail.select_one("div.texte")
            description = description_bloc.get_text(separator="\n", strip=True) if description_bloc else ""

            ville = extract_ville(description)
            departement, region, _ = get_ville_info(ville)
            departement = departement or "N/A"
            region = region or "N/A"
            telephone = extract_telephone(description)
            contact = extract_contact(description)

            annonces.append({
                "titre": titre,
                "description": description,
                "ville": ville,
                "departement": departement,  # enrichir API
                "region": region,
                "contact": contact,
                "telephone": telephone,
                "source": "osteopathe-syndicat.fr",
                "lien_annonce": lien_annonce,
                "date_publication": date_publication,
                "type_offre": type_offre
            })
        except Exception as e:
            print(f"Erreur sur une annonce : {e}")
            continue
        for i, annonce in enumerate(annonces, start=1):
            annonce["id"] = i
    return annonces

#extraction via regex
def extract_telephone(text):
    match = re.search(r"(0[1-9](?:[\s.-]?\d{2}){4})", text)
    return match.group(1) if match else ""

def extract_contact(text):
    match = re.search(r"(Dr|Monsieur|Madame|Mlle|M.)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?", text)
    return match.group(0) if match else ""

def extract_ville(text):
    match = re.search(r"\b(?:à|sur|près de)\s+([A-Z][a-zéèêëîïôöûü-]+)", text)
    return match.group(1) if match else ""



# Test local
#if __name__ == "__main__":
    #from pprint import pprint
    #annonces = scrape_osteopathe_syndicat()
    #pprint(annonces[:6])
