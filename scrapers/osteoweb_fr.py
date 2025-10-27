import requests
from bs4 import BeautifulSoup
from api.localisation import get_ville_info

def get_remplacement_links():
    url = "https://www.osteoweb.fr/remplacement/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    liens = set()
    for a in soup.select('a[href^="https://www.osteoweb.fr/"]'):
        href = a.get("href")
        if href and "remplacement" in href and href.endswith(".htm"):
            liens.add(href)
    return list(liens)

def get_info_remplacement():
    liens = get_remplacement_links()
    data = []
    for lien in liens:
        r = requests.get(lien)
        soup = BeautifulSoup(r.text, "html.parser")

        titre = soup.find("title").get_text(strip=True)
        description = soup.find("meta", {"name": "description"})["content"]

        ville_tag = soup.find("b", string=lambda s: s and "Ville" in s)
        ville = ville_tag.next_sibling.strip() if ville_tag else "N/A"

        departement, region, _ = get_ville_info(ville)
        departement = departement or "N/A"
        region = region or "N/A"

        contact_tag = soup.find("b", string=lambda s: s and "Contact" in s)
        contact = contact_tag.next_sibling.strip() if contact_tag else "N/A"
        
        tel_tag = soup.find("font", {"color": "#990000"})
        telephone = tel_tag.get_text(strip=True) if tel_tag else "N/A"

        data.append({
            "Titre": titre,
            "Description": description,
            "Ville": ville,
            "Département": departement,
            "Région": region,
            "Contact": contact,
            "Téléphone": telephone,
            "Source": lien,
        })
    return data

    