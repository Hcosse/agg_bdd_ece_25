# Projet d’Agrégation de Données — Ostéopathie

**ECE 2025 – Agrégation de données**

---

## Objectif du projet

Ce projet a pour but de **collecter, nettoyer et agréger des annonces d’ostéopathie** provenant de plusieurs sites web, puis de les **stocker dans une base de données commune** ou un fichier CSV.

---

## Équipe


| Étudiant | Rôle                             | Sites attribués                               |
| --------- | --------------------------------- | ---------------------------------------------- |
| **Hugo**  | Web scraping                      | osteoweb.fr, entreosteos.com                   |
| **Ryan**  | Web scraping                      | osteofrance.com, osteodispo.fr                 |
| **Robin** | Web scraping                      | osteopathe-syndicat.fr, annonces-medicales.com |
| **Tous**  | Enrichissement via API & OpenData | OpenStreetMap, INSEE                           |

---

## Structure du projet

````bashC:\Users\hugoc\Documents\ECE\Aggregation

  │
├── api/
│   └── geoloc_api.py
│
├── config/
│   └── sites.yaml
│
├── opendata/
│   └── insee_import.py
│
├── output/
│   └── annonces.csv
│
├── scrapers/
│   ├── osteoweb_fr.py
│   ├── entreosteos_com.py
│   ├── osteofrance_com.py
│   ├── osteodispo_fr.py
│   ├── osteopathe_syndicat_fr.py
│   └── annonces_medicales_com.py
│
├── storage/
│   └── storage.py
│
├── utils/
│   └── robots.py
│
├── runner.py
├── README.md
├── .gitignore
└── requirements.txt

```
````

### **api/**

Contient les scripts qui appellent des API externes (géolocalisation, météo…).
→ Sert à enrichir les annonces avec des infos comme la région, la latitude, etc.

### **config/**

Regroupe les fichiers de configuration.
→ Le fichier `sites.yaml` décrit les sites à scraper (URL, délais, paramètres).

### **opendata/**

Scripts pour importer des données publiques (INSEE, data.gouv…).
→ Permet d’ajouter du contexte : densité d’ostéopathes, population, etc.

### **output/**

Dossier de sortie.
→ Contient le fichier `annonces.csv` avec toutes les données nettoyées et agrégées.

### **scrapers/**

C’est le cœur du projet : un script par site web.
→ Chaque fichier `.py` gère l’extraction des annonces d’un site spécifique.

### **storage/**

Fonctions liées au stockage des données.
→ Enregistrement en CSV ou base de données.

### **utils/**

Contient les outils communs (ex : vérification du robots.txt).
→ Facilite le respect des règles de scraping.

### **runner.py**

Script principal du projet.
→ Lance les scrapers, agrège les résultats et génère le CSV final.

### **requirements.txt**

Liste les dépendances Python nécessaires (requests, BeautifulSoup, pandas…).

### **.gitignore**

Fichiers à exclure du dépôt Git (cache, CSV, etc.).

### **README.md**

Présentation du projet, de son fonctionnement et de son organisation.
