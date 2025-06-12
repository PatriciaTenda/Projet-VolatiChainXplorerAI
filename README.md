# Projet-VolatiChainXplorerAI
VolatiChainXplorer AI est un projet d’analyse de la volatilité du Bitcoin basé sur la collecte de données multi-sources (API, CSV, articles, réseaux sociaux). Les données sont stockées dans PostgreSQL/MongoDB et exposées via une API FastAPI pour des analyses sémantiques et prédictives.

# Les sources de données
     https://www.coingecko.com/en/api
     https://github.com/ranaroussi/yfinance
     https://www.reddit.com/dev/api/
     https://sdw.ecb.europa.eu/ ou https://data-api.ecb.europa.eu/
     https://cryptoast.fr


# Structure du projet 
```bash
PROJET-VOLATICHAINXPLORERAI/
├── api/                                ← Application FastAPI (routes REST, schémas, auth)
│   └── ...
├── data/                               ← Données du projet (brutes, nettoyées, exportées)
│   ├── cleaned/                        ← Données prêtes à l’analyse ou au chargement
│   ├── exports/                        ← Données enrichies ou résultats exportés
│   └── raw/                            ← Données collectées (scraping, API, CSV, etc.)
├── database/                           ← Gestion des bases de données (PostgreSQL et Mongo)
│   ├── conn_db/
│   │   └── postgres_client.py          ← Connexion SQLAlchemy à PostgreSQL
│   ├── models/                         ← Modèles ORM PostgreSQL (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user_model.py               ← Table t_user (authentification)
│   │   ├── bitcoin_model.py            ← Table t_bitcoin_price (prix BTC)
│   │   └── mro_model.py                ← Table t_mro_rate (taux MRO)
│   └── init_db.py                      ← Script pour créer toutes les tables en BDD
├── scripts/                            ← Scripts de traitement et import de données
│   ├── clean/                          ← Nettoyage des données
│   ├── collect/                        ← Récupération (scraping/API)
│   └── import_db/
│       ├── import_postgres.py          ← Insertion des données nettoyées dans PostgreSQL
│       └── import_mongo.py             ← Insertion future dans MongoDB
├── notebooks/                          ← Notebooks Jupyter pour analyses exploratoires
│   ├── scrape_reddit.ipynb             ← Scraping Reddit
│   └── scrape_twitter.ipynb            ← Scraping Twitter
├── docker-compose.yml                  ← Fichier Docker Compose pour lancer les services
├── Dockerfile                          ← Dockerisation de l’API (FastAPI par ex.)
├── .env                                ← Variables d’environnement (PostgreSQL URL, etc.)
├── .gitignore                          ← Fichiers ignorés par Git (env, cache, etc.)
├── README.md                           ← Documentation et guide du projet
└── requirements.txt                    ← Liste des dépendances Python

```


# Installations des librairies 
## Configuration de l'environemment du projet
```bash
    # Mise en place de l' environnement python 
    py -3.12 -m venv env

    # Activtion de l'environnement 
    .\env\Scripts\activate

    # Activtion du fichier requirements.txt 
    pip freeze > requirements.txt
``` 
## Installation des librairies utile pour l'extraction des données

### Librairie utiles
```bash
    pip install requests pandas
    pip install dateparser # parser la date
    pip install python-slugify # Pour formater le nom du fichier 

``` 

### Extraction via les API coingecko et Yfinance 
```bash
    # API  coingecko
   pip install pycoingecko

    # API  Yfinance ou 
    pip install yfinance

    # Celui_ci si on rencontre des soucis de certificats  
    pip install --upgrade yfinance

``` 
### Extraction via le scraping web
```bash
    # Parser HTML pour BeautifulSoup 
    pip install lxml

    # installer beautifulsoup4
    pip install beautifulsoup4 html5lib
``` 

### Extraction via le scraping  de X (anciennement Tweeter)
```bash
    # Bibliothèque pour interagir avec l'API de X 
    pip install tweepy
    
    # Bibliothèque pour interagir sans API de X avec une version de python à partir de 3.11 et descandant
    pip install git+https://github.com/JustAnotherArchivist/snscrape.git


```