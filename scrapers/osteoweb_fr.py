import requests
from bs4 import BeautifulSoup


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
    liens  = get_remplacement_links()

    data = []

    for lien in liens:
        r = requests.get(lien)
        soup = BeautifulSoup(r.text, "html.parser")

        titre = soup.find("title").get_text()
        desription = soup.find("meta", {"name": "description"})["content"]

        departement = soup.find("b",string=lambda s: s and "Localisation" in s)
        departement= departement.next_sibling.strip() if departement else "N/A"

        ville = soup.find("b",string=lambda s: s and "Ville" in s)
        ville= ville.next_sibling.strip() if ville else "N/A"

        contact = soup.find("b",string=lambda s: s and "Contact" in s)
        contact= contact.next_sibling.strip() if contact else "N/A"
        
        telephone = soup.find("font", {"color": "#990000"})
        telephone = telephone.get_text(strip=True) if telephone else ""

        
        data.append({
            "Titre": titre,
            "Description": desription,
            "Département": departement,
            "Ville": ville,
            "Contact": contact,
            "Téléphone": telephone,
            "Source": lien,
        })

    for item in data:
        print(item["Titre"])
        print(item["Source"])
        print(item["Description"])
        print(item["Département"])
        print(item["Ville"])
        print(item["Contact"])
        print(item["Téléphone"])
        print("-" * 40)
            
    return data


    get_info_remplacement() 