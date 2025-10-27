import requests
from bs4 import BeautifulSoup
import re
from api.localisation import get_ville_info


def get_remplacement_links():
    url = "https://osteofrance.com/petites-annonces/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    liens = set()
    # On cible tous les liens d'annonces dans le tableau
    for a in soup.select("table.annonces td.title a[href^='/petite-annonce/']"):
        href = a.get("href")
        if href:
            liens.add("https://osteofrance.com" + href)

    return list(liens)


def scrape_osteopathes_de_france():
    liens = get_remplacement_links()
    annonces = []

    for lien in liens:
        try:
            r = requests.get(lien)
            soup = BeautifulSoup(r.text, "html.parser")

            #  Extraction des informations 
            titre_tag = soup.select_one("h1.title")
            titre = titre_tag.get_text(strip=True) if titre_tag else ""

            type_offre_tag = soup.select_one("p.section-head.meta")
            type_offre = type_offre_tag.get_text(strip=True) if type_offre_tag else ""

            description_bloc = soup.select_one("div.entry-body")
            description = description_bloc.get_text(separator="\n", strip=True) if description_bloc else ""

           
            date_tag = soup.select_one("p.meta time")
            if date_tag and date_tag.get("datetime"):
                date_publication = date_tag["datetime"]
            else:
                date_publication = ""

            
            ville_tag = soup.select_one("div.address p span.uc")
            ville = ville_tag.get_text(strip=True) if ville_tag else "N/A"

            
            contact_tag = soup.select_one("div.name strong")
            contact = contact_tag.get_text(strip=True) if contact_tag else ""

           
            telephone_tag = soup.select_one("div.name")
            telephone = ""
            if telephone_tag:
                tel_match = re.search(r"(0[1-9](?:[\s.-]?\d{2}){4})", telephone_tag.get_text())
                telephone = tel_match.group(1) if tel_match else ""

            
            departement, region, _ = get_ville_info(ville)
            departement = departement or "N/A"
            region = region or "N/A"

            annonces.append({
                "titre": titre,
                "type_offre": type_offre,
                "description": description,
                "ville": ville,
                "departement": departement,
                "region": region,
                "contact": contact,
                "telephone": telephone,
                "lien_annonce": lien,
                "date_publication": date_publication,
                "source": "osteofrance.com"
            })

        except Exception as e:
            print(f"Erreur sur {lien} : {e}")
            continue

    # Ajout d'un ID 
    for i, annonce in enumerate(annonces, start=1):
        annonce["id"] = i

    return annonces


# Extraction via regex 
def extract_telephone(text):
    match = re.search(r"(0[1-9](?:[\s.-]?\d{2}){4})", text)
    return match.group(1) if match else ""
