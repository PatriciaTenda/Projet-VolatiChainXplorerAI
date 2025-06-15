# Projet-VolatiChainXplorerAI
VolatiChainXplorer AI est un projet d’analyse de la volatilité du Bitcoin basé sur la collecte de données multi-sources (API, CSV, articles, réseaux sociaux). Les données sont stockées dans PostgreSQL/MongoDB et exposées via une API FastAPI pour des analyses sémantiques et prédictives.

# Les sources de données
     https://www.coingecko.com/en/api
     https://coinmarketcap.com/currencies/bitcoin/historical-data/
     https://github.com/ranaroussi/yfinance
     https://www.reddit.com/dev/api/
     https://sdw.ecb.europa.eu/             # Pour les articles
     https://data-api.ecb.europa.eu/        # Pour les indicateurs macroéconomiques
     https://cryptoast.fr


# Structure du projet 
```bash
PROJET-VOLATICHAINXPLORERAI/
├── api/                    ← Application FastAPI (routes, schémas, auth)
├── data/                   ← Données du projet (brutes, nettoyées, exportées)
│   ├── cleaned/            ← Données nettoyées
│   ├── exports/            ← Données transformées / résultats
│   └── raw/                ← Données collectées à la source
├── database/               ← Connexion, modèles ORM, initialisation BDD
│   ├── conn_db/            ← Fichiers de connexion à PostgreSQL
│   ├── models/             ← Modèles SQLAlchemy
│   └── init_db.py          ← Script de création des tables
├── scripts/                ← Traitement et import de données
│   ├── clean/              ← Nettoyage des données
│   ├── collect/            ← Récupération (scraping/API)
│   └── import_db/          ← Insertion des données en BDD
├── notebooks/              ← Analyses exploratoires (Jupyter)
├── setup/                  ← Scripts de lancement (Docker Bash)
│   └── run_postgres.sh     ← Script de lancement PostgreSQL
├── docker-compose.yaml     ← Orchestration des services Docker
├── Dockerfile              ← Dockerisation de l’API
├── .env                    ← Variables d’environnement
├── .gitignore              ← Fichiers à ignorer par Git
├── README.md               ← Documentation du projet
└── requirements.txt        ← Dépendances Python du projet

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