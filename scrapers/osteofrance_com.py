import requests 
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import re
from datetime import datetime
from pathlib import Path

def get_job_links(job):
    links = set()  
    base = 'https://osteofrance.com'
    if job.find_all("a", href=True):
        for link in job.find_all("a", href=True):
            href = link['href']
            if href.startswith('#') or href.startswith('mailto:') or href.startswith('javascript:'):
                continue
            full = urljoin(base, href)
            if '/petite-annonce' in full:
                links.add(full)
    return list(links)


def parse_detail_page(detail_url):
    """Fetch a detail page and extract structured fields."""
    try:
        r = requests.get(detail_url, timeout=15)
        r.raise_for_status()
        s = BeautifulSoup(r.text, 'html.parser')

        titre = s.select_one('h1')
        titre = titre.get_text(strip=True) if titre else ''

        article = s.select_one('article') or s.select_one('.annonce') or s
        p_texts = [p.get_text(' ', strip=True) for p in article.select('p')]

        date_publication = ''
        for t in p_texts:
            m = re.search(r'Publi[eé]e\s+le\s*([0-9]{1,2}[\.\-/][0-9]{1,2}[\.\-/][0-9]{4})', t)
            if m:
                raw = m.group(1)
                try:
                    dt = datetime.strptime(raw.replace('-', '.').replace('/', '.'), '%d.%m.%Y')
                    date_publication = dt.date().isoformat()
                except Exception:
                    date_publication = raw
                break

        telephone = ''
        tel_re = re.compile(r'(?:\+33|0)[\d .\-]{8,}\d')
        for t in p_texts:
            m = tel_re.search(t)
            if m:
                telephone = re.sub(r'[^+0-9]', '', m.group(0))
                break

        contact = ''
        for t in p_texts:
            if 'Tél' in t or 'Tel' in t or 'Téléphone' in t:
                contact = t.split('Tél')[0].split('Tel')[0].split('Téléphone')[0].strip(' -:')
                break
        if not contact:
            for t in p_texts:
                if 1 < len(t.split()) <= 4 and any(w and w[0].isupper() for w in t.split()):
                    contact = t.strip()
                    break

        ville = ''
        if p_texts:
            first = p_texts[0]
            m = re.search(r'\bà\s+([A-ZÉÈÀÎÏÙÂÙÇÃÉÔÎÉ\-\'"\w ]+)', first)
            if m:
                ville = m.group(1).strip()
        if not ville:
            for t in reversed(p_texts[-4:]):
                if 1 <= len(t) <= 60 and re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ' .-]+$", t):
                    ville = t.strip()
                    break

        region = ''
        desc_blob = ' '.join(p_texts)
        mreg = re.search(r"([A-Za-zÀ-ÿ \-']+?)\s*\(\s*\d{2,3}\s*\)", desc_blob)
        if mreg:
            region = mreg.group(1).strip()

        desc_parts = []
        for t in p_texts:
            if not t:
                continue
            if 'Publi' in t and 'le' in t:
                continue
            if 'Tél' in t or 'Tel' in t or 'Téléphone' in t:
                continue
            if len(t) < 3:
                continue
            if ville and t.strip() == ville:
                continue
            desc_parts.append(t)
        description = ' '.join(desc_parts).strip()  

        type_offre = ''
        if p_texts and ('Offre' in p_texts[0] or 'Remplacement' in p_texts[0] or 'Collaboration' in p_texts[0]):
            type_offre = p_texts[0]

        return {
            'titre': titre,
            'description': description,
            'ville': ville,
            'region': region,
            'contact': contact,
            'telephone': telephone,
            'source': 'osteofrance.com',
            'lien_annonce': detail_url,
            'date_publication': date_publication,
            'type_offre': type_offre,
        }
    except requests.RequestException as e:
        print('Error fetching detail page', detail_url, e)
        return {
            'titre': '', 'description': '', 'ville': '', 'region': '', 'contact': '',
            'telephone': '', 'source': 'https://osteofrance.com/', 'lien_annonce': detail_url,
            'date_publication': '', 'type_offre': ''
        }


def scrape_osteofrance():
    url = 'https://osteofrance.com/petites-annonces'
    scraped_data = []
    id_counter = 51

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        job_listings = soup.select('tbody.list tr')

        for job in job_listings:
            job_element = job.find("td", class_="type")
            if job_element:
                job_type = job_element.get_text(strip=True)
            else:
                job_type = ""

            if 'rempla' in job_type.lower():
                info_urls = get_job_links(job)
                for info_url in info_urls:
                    detail = parse_detail_page(info_url)
                    if not detail.get('type_offre'):
                        detail['type_offre'] = job_type
                    detail['id'] = id_counter
                    id_counter += 1
                    scraped_data.append(detail)

        return scraped_data

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

job_listings = scrape_osteofrance()
