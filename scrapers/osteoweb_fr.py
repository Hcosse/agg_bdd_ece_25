import yaml
import requests
from bs4 import BeautifulSoup
import yaml
import os 
import dotenv

dotenv.load_dotenv()


def scrape_osteoweb():
    url = os.getenv('BASE_URL_OSTEOWEB')
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    annonces = []
    for article in soup.select("article"):
        titre = article.select_one("h2").get_text(strip=True)
        ville = article.select_one(".ville").get_text(strip=True)
        lien = article.select_one("a")["href"]
        annonces.append({
            "source": "osteoweb.fr",
            "titre": titre,
            "ville": ville,
            "lien_annonce": lien
        })
    return annonces