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
        
        
        data.append({
            "titre": titre,
            "description": desription,
            "lien": lien,
        })

    for item in data:
        print(item["titre"])
        print(item["lien"])
        print(item["description"])
        print("-" * 40)
            
    return data


    get_info_remplacement() 