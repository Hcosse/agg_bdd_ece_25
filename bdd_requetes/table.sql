

-- Table temporaire (staging)
DROP TABLE IF EXISTS staging_annonces;
CREATE TABLE staging_annonces (
    id INT,
    source TEXT,
    titre TEXT,
    ville TEXT,
    region TEXT,
    type_offre TEXT,
    telephone TEXT,
    date_publication TEXT,
    contact TEXT,
    description TEXT,
    lien_annonce TEXT
);

-- Import du CSV nettoyé (dans le conteneur Docker : /mnt/output/annonces_clean.csv)
COPY staging_annonces 
FROM '/mnt/output/annonces_clean.csv' 
DELIMITER ',' 
CSV HEADER;

-- Table principale (base propre)
DROP TABLE IF EXISTS annonces;

CREATE TABLE annonces (
    id SERIAL PRIMARY KEY,
    source VARCHAR(100),
    titre TEXT,
    ville VARCHAR(100),
    region VARCHAR(100),
    type_offre VARCHAR(100),
    telephone VARCHAR(20),
    date_publication DATE,
    contact VARCHAR(100),
    description TEXT,
    lien_annonce TEXT UNIQUE
);

-- Transfert des données nettoyées depuis le staging

INSERT INTO annonces (
    source, titre, ville, region, type_offre, telephone,
    date_publication, contact, description, lien_annonce
)
SELECT
    NULLIF(source, ''),
    NULLIF(titre, ''),
    NULLIF(ville, ''),
    NULLIF(region, ''),
    NULLIF(type_offre, ''),
    NULLIF(telephone, ''),
    CASE 
        WHEN date_publication ~ '^\d{4}-\d{2}-\d{2}$' THEN date_publication::date
        ELSE NULL
    END,
    NULLIF(contact, ''),
    NULLIF(description, ''),
    NULLIF(lien_annonce, '')
FROM staging_annonces
WHERE lien_annonce IS NOT NULL;

-- Vue : annonces par région
CREATE OR REPLACE VIEW v_annonces_par_region AS
SELECT region, COUNT(*) AS total
FROM annonces
WHERE region IS NOT NULL
GROUP BY region
ORDER BY total DESC;

-- Vue : annonces par type d'offre
CREATE OR REPLACE VIEW v_annonces_par_type AS
SELECT type_offre, COUNT(*) AS total
FROM annonces
WHERE type_offre IS NOT NULL
GROUP BY type_offre
ORDER BY total DESC;

-- Vue : annonces récentes 
CREATE OR REPLACE VIEW v_annonces_recent AS
SELECT titre, ville, region, type_offre, date_publication
FROM annonces
WHERE date_publication >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY date_publication DESC;
