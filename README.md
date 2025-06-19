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
├── alembic/                      ← Dossier de migration Alembic
│   ├── versions/                 ← Scripts de migration auto-générés
│   ├── env.py                    ← Script de configuration Alembic
│   ├── script.py.mako           ← Template de génération Alembic
│   └── README                    ← Explication Alembic (optionnel)
│
├── api/                          ← Application FastAPI (routes, auth, endpoints)
│   └── ...                       ← À structurer (main.py, routes/, etc.)
│
├── data/                         ← Données du projet
│   └── ...                       ← (brutes, nettoyées, exports à créer)
│
├── database/                     ← Couche d’abstraction des bases de données
│   ├── conn_db/                  ← Fichiers de connexion
│   │   ├── connect_postgresql.py
│   │   ├── connect_mongodb.py
│   │   └── __init__.py
│   │
│   ├── models/                   ← Modèles SQLAlchemy
│   │   ├── bitcoin_prices.py
│   │   ├── macro_indicators.py
│   │   ├── users.py
│   │   └── __init__.py
│   │
│   └── schemas/                  ← Schémas Pydantic
│       └── __init__.py
│
├── env/                          ← Fichier `.env` contenant les variables d’environnement
│
├── notebooks/                    ← Analyses exploratoires et visualisations
│   └── ...                       ← Fichiers `.ipynb`
│
├── scripts/                      ← Scripts de traitement, collecte, injection
│   ├── collect/                  ← Pour les scripts de scraping/API
│   ├── clean/                    ← Nettoyage des fichiers
│   ├── import_db/                ← Insertion PostgreSQL
│   └── build_views.py            ← Script pour exécuter les vues SQL
│
├── setup/                        ← Configuration et automation
│   └── run_postgres.sh           ← Lancement Docker PostgreSQL / MongoDB
│
├── .env                          ← Variables d’environnement (.gitignored)
├── .gitignore                    ← Ignore les caches, .env, __pycache__, etc.
├── README.md                     ← Documentation de ton projet
└── requirements.txt              ← Liste des dépendances Python


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
### Configration de POSTGRESQL dans DOCKER
```bash
    # Format de l' URL de connexion à la base de données POSTGRESQL
        URL = "postgresql+psycopg2://POSTGRES_USER:POSTGRES_PASSWORD@POSTGRES_HOST:POSTGRES_PORT/POSTGRES_DB"
    
    # Extraction de l'image Docker PostgreSQL
    # Extraire la dernière image PostgreSQL, ouvrir le terminal ou l'invite de commande et exécutez :
        docker pull postgres

    # Pour le configurer, commencez par créer un volume nommé :
        docker volume create postgres-data # donner un nom au volume crée

    # Inspecter les détails du volume en exécutant la commande suivante :
        docker volume inspect postgres-data

    # Exécution de PostgreSQL dans un conteneur Docker
    # Une fois l'image PostgreSQL obtenue, créer et démarrer un conteneur avec une seule commande :
        docker run --name VolatiChainXplorerAI_postgres \
                    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
                    -e POSTGRES_USER=$POSTGRES_USER \
                    -e POSTGRES_DB=$POSTGRES_DB \
                    -p 5433:5432 \
                    -v postgres-data:/var/lib/postgresql/data \
                    -d postgres 

    # Rendre le script exécutable une fois 
        chmod +x setup/run_postgres.sh  #  Donne le droit de l’exécuter

    # Puis à chaque lancement
       ./database/run_postgres.sh       # Exécute le script s’il est exécutable
 

    # Vérifier que le conteneur fonctionne avec :
        docker ps
        docker ps -a   # pour vérifier les conteneurs, même céux supprimé

    # Pour arrêter un conteneur PostgreSQL en cours d’exécution, exécutez la commande suivante :
        docker stop postgres-db

    # Pour exécutez la commande suivante lorsque vous devez le redémarrer :
        docker start postgres-db
    
    # Pour redémarrer un conteneur en cours d'exécution, ce qui peut être utile après avoir modifié certaines configurations, exécutez la commande suivante :
        docker restart postgres-db

    # Exécutez cette commande pour afficher les journaux du conteneur PostgreSQL :
        docker logs postgres-db
        docker logs -f postgres-db # suivre les logs en temps réel

    # Exécuter docker_compose.yaml
        docker-compose up -d

    # Pour stopper l'exécution de docker_compose.yaml
        docker-compose down -d
```
## Installations des librairies néccessaires pour les bases de données
### POSTGRESQL - SQLAlchimy
```bash
    # Installation de SQLAlchimy
        pip install SQLAlchemy psycopg2-binary
```
#### Installation de la librairie alembic pour la gestion des versions avec SQLAlchemy
```bash
    # Installation du dossier d'alembic
        pip install alembic
    
    # Initialisation de l'environnement d'alembic (Option choisi pour le projet)
        alembic init 
        
    # ou exécuter cette commande pour une intégration moderne avec les projets qui suivent la norme PEP 518 (nouveau et plus moderne)
        alembic init --template pyproject alembic

    # Pour creer une nouvelle révision, utiliser le script de création d'une migration de la manière suivante :
       alembic revision --autogenerate -m "create all macro and btc tables"

        
    # Pour exécuter une première migration
        alembic upgrade head

    # Pour exécuter une seconde migration ( Par exemple,  on peut ajouter dans une table déjà créée une nouvelle colonne)
        alembic revision --autogenerate -m "Added account table" # Au cas où

    # A l'inverse pour downgrade la migration c'est - à - dire retourner au debut de la migration
        alembic downgrade 
```
### Schémas des entrées/sorties avec pydantic
```bash
    # Installation de la librairie pydantic
        pip install pydantic
```