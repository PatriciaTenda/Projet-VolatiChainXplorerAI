# Projet-VolatiChainXplorerAI
VolatiChainXplorer AI est un projet d’analyse de la volatilité du Bitcoin basé sur la collecte de données multi-sources (API, CSV, articles, réseaux sociaux). Les données sont stockées dans PostgreSQL/MongoDB et exposées via une API FastAPI pour des analyses sémantiques et prédictives.

# Les sources de données
     https://www.coingecko.com/en/api
     https://coinmarketcap.com/currencies/bitcoin/historical-data/
     https://github.com/ranaroussi/yfinance
     https://www.reddit.com/dev/api/
     https://sdw.ecb.europa.eu/             # Pour les articles
     https://data-api.ecb.europa.eu/        # Pour les indicateurs macroéconomiques
     https://cryptoast.fr                   # Pour les articles


# Structure du projet 
```bash
PROJET-VOLATICHAINXPLORERAI/
│
├── alembic/                             ← Fichiers de migration PostgreSQL (générés par Alembic)
│
├── api/                                 ← Backend FastAPI
│   ├── auths/                           ← Gestion de l'authentification (routes sécurisées)
│   ├── routers/                         ← Routes de l’API
│   └── main.py                          ← Point d’entrée de l’application FastAPI
│
├── data/                                ← Données brutes ou transformées
│   └── raw/
│       ├── articles_financiers/         ← Articles scrappés (.json)
│       └── logs/                        ← Fichiers logs (.log)
│
├── database/                            ← Connexion et structure des bases de données
│   ├── conn_db/                         ← Scripts de connexion
│   │   ├── connect_mongodb.py
│   │   ├── connect_postgresql.py
│   │   └── __init__.py
│   │
│   ├── mongo/                           ← Scripts MongoDB
│   │   ├── create_collections.py
│   │   └── __init__.py
│   │
│   └── postgres/                        ← Définition des tables et schémas PostgreSQL
│       ├── models/
│       │   ├── bitcoin_prices.py
│       │   ├── macro_indicators.py
│       │   ├── users.py
│       │   └── __init__.py
│       └── schemas/
│           ├── bitcoin_prices.py
│           ├── macro_indicators.py
│           ├── users.py
│           └── __init__.py
│
├── env/                                 ← Environnement virtuel local (à ne pas versionner)
│
├── notebooks/                           ← Analyses exploratoires & tests en Jupyter Notebook
│
├── scripts/                             ← Scripts de traitement, collecte, injection 
│   ├── collect/                         ← Scripts de collecte (scraping/API)
│   │   ├── collect_btc_api_coingecko.py
│   │   ├── collect_btc_api_kraken.py
│   │   ├── Collect_btc_api_yfinance.py
│   │   ├── download_bce_HICP_Inflation.py
│   │   ├── download_bce_mro.py
│   │   ├── download_Monetary_aggregate_M3.py
│   │   ├── download_unemployment_rate.py
│   │   ├── scrape_crypttoast_article_financier.py
│   │   ├── scrape_twitter_api.py
│   │   └── scrape_twitter.py
│
│   ├── clean/                           ← Préparation et nettoyage des datasets
│   │   ├── cleaned_Bitcoin_historical_data.py
│   │   ├── cleaned_HICP_inflation_data.py
│   │   ├── cleaned_Monetary_aggregate_M3.py
│   │   ├── cleaned_MRO.py
│   │   └── cleaned_unemployment_rate_data.py
│
│   ├── injection_db_mongo/             ← Insertion dans MongoDB
│   │   ├── injection_articles_financiers.py
│   │   ├── injection_logs.py
│   │   └── __init__.py
│
│   ├── injection_db_postgres/          ← Insertion dans PostgreSQL
│   │   ├── injection_data_aggregate_M3.py
│   │   ├── injection_data_btcoin.py
│   │   ├── injection_data_Inflation.py
│   │   ├── injection_data_mro.py
│   │   ├── injection_data_unemployment.py
│   │   └── __init__.py
│
│   └── update/                         ← Scripts de mise à jour conditionnelle
│       ├── update_or_insert.py
│       └── __init__.py
│
├── setup/                               ← Configuration & automation
│   ├── logger_config.py                 ← Logger Python centralisé
│   ├── run_mongo.sh                     ← Script de lancement Docker MongoDB
│   ├── run_postgres.sh                  ← Script de lancement Docker PostgreSQL
│   └── __init__.py
│
├── .env                                 ← Variables d’environnement (pas versionner)
├── .gitignore                           ← Exclusions Git (env/, __pycache__/, .env, etc.)
├── alembic.ini                          ← Config Alembic
├── docker-compose.yaml                  ← Déploiement multi-conteneurs Docker
├── Dockerfile                           ← Image Docker de l'app FastAPI
├── requirements.txt                     ← Dépendances Python du projet
└── README.md                            ← Documentation principale du projet



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

## Configuration des bases de données POSTGRESQL et MONGODB
### Configuration de POSTGRESQL avec DOCKER
####  URL de connexion (avec SQLAlchemy)
```bash
    # Format de l' URL de connexion à la base de données POSTGRESQL
        URL = "postgresql+psycopg2://POSTGRES_USER:POSTGRES_PASSWORD@POSTGRES_HOST:POSTGRES_PORT/POSTGRES_DB"
```
#### Étapes pour lancer PostgreSQL avec Docker
```bash
    # Télécharger l'image officielle PostgreSQL
    docker pull postgres

    # Créer un volume persistant pour PostgreSQL
    docker volume create postgres_data

    # Inspecter le volume
    docker volume inspect postgres_data

    # Lancer PostgreSQL dans un conteneur Docker
    docker run --name VolatiChainXplorerAI_postgres \
    -e POSTGRES_USER=$POSTGRES_USER \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -e POSTGRES_DB=$POSTGRES_DB \
    -p 5433:5432 \
    -v postgres_data:/var/lib/postgresql/data \
    -d postgres

```
####  Gestion du conteneur PostgreSQL
```bash
    # Vérifier les conteneurs actifs
    docker ps

    # Voir tous les conteneurs (même stoppés)
    docker ps -a

    # Arrêter PostgreSQL
    docker stop VolatiChainXplorerAI_postgres

    # Redémarrer PostgreSQL
    docker start VolatiChainXplorerAI_postgres

    # Redémarrage complet (utile après un changement de config)
    docker restart VolatiChainXplorerAI_postgres

    # Voir les logs
    docker logs VolatiChainXplorerAI_postgres

    # Suivre les logs en temps réel
    docker logs -f VolatiChainXplorerAI_postgres
```
#### Utilisation avec Docker Compose (au cas où il est utilisé)
```bash
    # Lancer les services
    docker-compose up -d

    # Arrêter les services
    -compose down
```
#### Rendre un script exécutable
```bash
   # Rendre le script exécutable une fois 
        chmod +x setup/run_postgres.sh  #  Donne le droit de l’exécuter

   # Puis à chaque lancement
       ./database/run_postgres.sh       # Exécute le script s’il est exécutable
```

#### Installation des bibliothèques Python
##### PostgreSQL avec SQLAlchemy et Psycopg2
```bash
    # Installation de SQLAlchimy
        pip install SQLAlchemy psycopg2-binary
```
##### Alembic – Gestion des migrations de schéma
```bash
    # Installer Alembic
    pip install alembic

    # Initialiser un environnement Alembic (classique)
    alembic init alembic

    # Ou version moderne (recommandée pour pyproject.toml)
    alembic init --template pyproject alembic 
```
#### Utilisation de Alembic
```bash
    # Créer une révision automatique
    alembic revision --autogenerate -m "create all macro and btc tables"

    # Appliquer la migration
    alembic upgrade head

    # Ajouter une nouvelle révision (ex : ajout de colonne/table)
    alembic revision --autogenerate -m "Added account table"

    # Revenir en arrière (downgrade)
    alembic downgrade -1   # ou downgrade base
```

### Schémas des entrées/sorties avec pydantic
```bash
    # Installation de la librairie pydantic
        pip install pydantic
```
### Configuration de MongoDB avec Docker
```bash
    # Format de l'URL de connexion MongoDB
    # Remplacer les variables par les valeurs de ton fichier .env
    # Definir un delai d'expiration côté client à l'aide de l' option de connexion timeoutMS
    URI = "mongodb://MONGO_USER:MONGO_PASSWORD@localhost:MONGO_PORT/MONGO_DB?authSource=admin&serverSelectionTimeoutMS=5000"

    # Extraire la dernière image MongoDB
    docker pull mongo

    # Créer un volume nommé pour la persistance des données
    docker volume create mongo_data

    # Vérifier les détails du volume
    docker volume inspect mongo_data

    # Lancer MongoDB dans un conteneur Docker
     docker run --name mongo_VolatiChainXplorerAI \
    -e MONGO_INITDB_ROOT_USERNAME=$MONGO_USER \
    -e MONGO_INITDB_ROOT_PASSWORD=$MONGO_PASSWORD \
    -e MONGO_INITDB_DATABASE=$MONGO_DB \
    -p $MONGO_PORT:27017 \
    -v mongo_data:/data/db \
    -d mongo:latest

    # Rendre un script exécutable (une seule fois)
    chmod +x setup/run_mongo.sh

    # Exécuter le script à chaque lancement
    ./setup/run_mongo.sh
```
####  Vérification et gestion du conteneur MongoDB
```bash
    # Vérifier les conteneurs en cours
    docker ps

    # Voir tous les conteneurs (même stoppés)
    docker ps -a

    # Arrêter le conteneur
    docker stop mongo_VolatiChainXplorerAI

    # Démarrer le conteneur
    docker start mongo_VolatiChainXplorerAI

    # Redémarrer le conteneur
    docker restart mongo_VolatiChainXplorerAI

    # Voir les logs
    docker logs mongo_VolatiChainXplorerAI

    # Suivre les logs en temps réel
    docker logs -f mongo_VolatiChainXplorerAI
```
#### Docker Compose (au cas où c'est utilisé)
```bash
    # Lancer les services définis dans docker-compose.yml
    docker-compose up -d

    # Arrêter tous les services
    docker-compose down
```
#### Installation des bibliothèques Python
##### MONGODB avec pymongo
```bash
    # Installation de pymongo
    pip install pymongo
```