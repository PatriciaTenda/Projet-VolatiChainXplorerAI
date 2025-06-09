# Projet-VolatiChainXplorerAI
VolatiChainXplorer AI est un projet d’analyse de la volatilité du Bitcoin basé sur la collecte de données multi-sources (API, CSV, articles, réseaux sociaux). Les données sont stockées dans PostgreSQL/MongoDB et exposées via une API FastAPI pour des analyses sémantiques et prédictives.

# Les sources de données
     https://www.coingecko.com/en/api
     https://github.com/ranaroussi/yfinance
     https://www.reddit.com/dev/api/
     https://sdw.ecb.europa.eu/ ou https://data-api.ecb.europa.eu/
     https://cryptoast.fr


# Structure du projet 
VolatiChainXplorerAI/
├── data/
│   ├── raw/               ← données brutes collectées
│   ├── cleaned/           ← données nettoyées et prêtes à être utilisées
│   └── exports/           ← fichiers exportés ou transformés (CSV, JSON, etc.)
├── scripts/
│   ├── collect/           ← scripts de collecte (API, scraping, etc.)
│   ├── clean/             ← scripts de nettoyage
│   └── import_db/         ← scripts d’import vers PostgreSQL/MongoDB
├── notebooks/             ← analyses exploratoires (Jupyter)
├── api/                   ← ton projet FastAPI (REST)
├── database/              ← schémas SQL, scripts d’init, index
└── README.md              ← explication du projet



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