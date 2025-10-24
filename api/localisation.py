import requests
import re
import unicodedata

def slugify(nom: str) -> str:
    nom = nom.lower()
    nom = unicodedata.normalize('NFD', nom)
    nom = nom.encode('ascii', 'ignore').decode('utf-8')
    nom = re.sub(r'[^a-z0-9]+', '-', nom)
    nom = nom.strip('-')
    return nom

def get_ville_info(ville: str):
    try:
        data = requests.get(f"https://geo.api.gouv.fr/communes?nom={ville}").json()
        if not data:
            return None, None, slugify(ville)
        code_dept = data[0].get("codeDepartement")
        code_region = data[0].get("codeRegion")
        dept_name = requests.get(f"https://geo.api.gouv.fr/departements/{code_dept}").json().get("nom")
        region_name = requests.get(f"https://geo.api.gouv.fr/regions/{code_region}").json().get("nom")
        return dept_name, region_name, slugify(ville)
    except Exception:
        return None, None, slugify(ville)
