# Projet-VolatiChainXplorerAI
VolatiChainXplorer AI est un projet d'analyse de la volatilité du Bitcoin basé sur la collecte de données multi-sources (API, CSV, articles, réseaux sociaux). Les données sont stockées dans PostgreSQL (prix Bitcoin + indicateurs macro-économiques BCE) et MongoDB (articles financiers) et exposées via une API FastAPI pour des analyses sémantiques et prédictives.

**Statut actuel (Dernière mise à jour : 2026-06-05) :**
- ✅ Base PostgreSQL structurée avec tables Bitcoin et indicateurs macro (MRO, Inflation, Chômage, M3)
- ✅ Vue unifiée `v_macro_indicators_daily_v1` pour jointures temporelles (daily × monthly)
- ✅ Données Bitcoin enrichies (2010-2026) avec support multi-sources
- ✅ Scripts de collecte, nettoyage et injection opérationnels
- ✅ Migrations Alembic appliquées et documentées
- 🔄 API FastAPI en cours de développement

# Les sources de données
     https://www.coingecko.com/en/api
     https://coinmarketcap.com/currencies/bitcoin/historical-data/
     https://github.com/ranaroussi/yfinance
     https://www.reddit.com/dev/api/
     https://sdw.ecb.europa.eu/             # Pour les articles
     https://data-api.ecb.europa.eu/        # Pour les indicateurs macroéconomiques
     https://cryptoast.fr                   # Pour les articles

# Historique du projet

## Changelog

###  Juin 2026 - Phase 2 : Restructuration et enrichissement de la base de données

**05/06/2026**
- ✅ Migration `ccb59cb90494` : Correction du problème d'auto-incrémentation de la colonne id
- ✅ Création du script `concatenate_bitcoin_csvs.py` pour fusion des CSV Bitcoin
- ✅ Enrichissement de la table t_bitcoin_prices avec données 2010-2026 (5800+ lignes)
- ✅ Documentation complète du README avec structure BDD et workflow

**02/06/2026**
- ✅ Migration `c24e71c09ba3` : Refonte complète de t_bitcoin_prices
  - Support multi-sources (CoinMarketCap, CoinGecko, Kraken)
  - Types Numeric pour précision financière
  - Contrainte d'unicité composite : (date, source, currency, granularity)
- ✅ Migration `325ae849c379` : Standardisation des 4 tables macro-économiques BCE
  - Ajout colonne obs_status
  - Création vue v_macro_indicators_daily_v1 avec DATE_TRUNC
  - Alignement temporel daily/monthly pour ML
- ✅ Scripts de nettoyage modernisés (pandas 2.0, pathlib, context managers)

###  Juin 2025 - Phase 1 : Initialisation du projet

**26/06/2025**
- ✅ Migration `daa38defa7ad` : Renommage password_user → hashed_password (sécurité)
- ✅ Migration `c417baba77db` : Ajout du champ role_user dans t_users

**16/06/2025**
- ✅ Migration `a35097d1ed2f` : Création initiale des tables macro et Bitcoin
- ✅ Configuration Docker PostgreSQL + MongoDB
- ✅ Scripts de collecte BCE (MRO, Inflation, Chômage, M3)
- ✅ Scripts de scraping articles financiers (Cryptoast)
- ✅ Structure du projet établie


# Structure du projet 
```bash
PROJET-VOLATICHAINXPLORERAI/
│
├── alembic/                             ← Fichiers de migration PostgreSQL (générés par Alembic)
│   └── versions/                        ← Migrations appliquées :
│       ├── c24e71c09ba3_refactor_bitcoin_prices_table_structure.py
│       ├── 325ae849c379_update_macro_tables_standardize_columns_.py
│       └── ccb59cb90494_fix_bitcoin_prices_id_sequence.py
│
├── api/                                 ← Backend FastAPI
│   ├── auths/                           ← Gestion de l'authentification (routes sécurisées)
│   ├── routers/                         ← Routes de l’API
│   └── main.py                          ← Point d’entrée de l’application FastAPI
│
├── data/                                ← Données brutes ou transformées
│   ├── cleaned/                         ← Données nettoyées prêtes pour injection
│   │   ├── bitcoin_historical_cleaned_updated.csv  ← CSV Bitcoin consolidé (2010-2026)
│   │   ├── bce_mro_cleaned.csv
│   │   ├── HICP_Inflation_cleaned.csv
│   │   ├── Monetary_aggregate_M3_cleaned.csv
│   │   └── unemployment_rate_cleaned.csv
│   ├── raw/
│   │   ├── articles_financiers/         ← Articles scrappés (.json)
│   │   ├── logs/                        ← Fichiers logs (.log)
│   │   └── csvFile/                     ← Fichiers csv bruts (.csv)
│   └── exports/                         ← Exports et backups
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
├── env/                                 ← Environnement virtuel local (non versionner)
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
│   │   ├── cleaned_unemployment_rate_data.py
│   │   └── concatenate_bitcoin_csvs.py  ← Fusion des CSV Bitcoin historique + complément
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
##  Librairies Python utilisées

- **Python 3.12** : Version recommandée pour garantir la compatibilité avec les bibliothèques utilisées.

### Utilitaires
- `requests` : Requêtes HTTP pour récupérer des données depuis des APIs.
- `pandas` : Manipulation et analyse de données tabulaires.
- `dateparser` : Parsing intelligent des dates en différents formats.
- `python-slugify` : Génère des noms de fichiers "propres" (slugs) à partir de chaînes de caractères.

### Extraction de données financières
- `pycoingecko` : Accès facile à l’API publique CoinGecko.
- `yfinance` : Téléchargement des données boursières (Yahoo Finance).

### Scraping web et réseaux sociaux
- `lxml` : Parser HTML/XML performant (utilisé avec BeautifulSoup).
- `beautifulsoup4` : Librairie de web scraping pour extraire le contenu HTML.
- `html5lib` : Parser HTML alternatif compatible avec BeautifulSoup.
- `tweepy` : Client officiel de l’API Twitter/X.
- `snscrape` : Scraping de Twitter/X sans API (pratique sans authentification).

### PostgreSQL & ORM
- `SQLAlchemy` : ORM pour interagir avec une base PostgreSQL en Python.
- `psycopg2-binary` : Driver PostgreSQL utilisé par SQLAlchemy.
- `alembic` : Gestionnaire de migration de base de données (avec SQLAlchemy).

### MongoDB
- `pymongo` : Driver officiel pour se connecter et manipuler des bases MongoDB en Python.

### API REST avec FastAPI
- `fastapi` : Framework web moderne et rapide pour créer l’API du projet.
- `uvicorn` : Serveur ASGI ultra-performant pour exécuter l’API FastAPI.
- `pydantic` : Validation de données et création de schémas de requêtes/réponses pour FastAPI.

### Déploiement (via Docker)
- `docker`, `docker-compose` *(hors Python)* : Lancement des bases PostgreSQL et MongoDB dans des conteneurs.

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

    # Vérifier la version actuelle
    alembic current
```

## Structure de la base de données PostgreSQL

### Tables principales

#### Table `t_bitcoin_prices`
Stocke les prix historiques du Bitcoin avec support multi-sources.

**Colonnes :**
- `id` : Clé primaire auto-incrémentée
- `date` : Date du cours (format Date)
- `open` : Prix d'ouverture (Numeric 18,8)
- `high` : Prix le plus haut (Numeric 18,8)
- `low` : Prix le plus bas (Numeric 18,8)
- `close` : Prix de clôture (Numeric 18,8)
- `volume` : Volume des transactions (Numeric 24,8)
- `market_cap` : Capitalisation de marché (Numeric 28,8)
- `source` : Source des données (ex: "coinmarketcap_historical_data")
- `currency` : Devise (ex: "EUR")
- `granularity` : Granularité temporelle (ex: "1d")
- `collected_at` : Date de collecte (auto-générée)

**Contrainte d'unicité :** `(date, source, currency, granularity)`

**Période couverte :** 2010-07-14 à aujourd'hui

#### Tables macro-économiques BCE

**Table `t_macro_bce_mro_rates`** (Taux directeur BCE)
- `id_mro` : Clé primaire
- `date` : Date de l'observation
- `value` : Valeur du taux MRO
- `obs_status` : Statut de l'observation
- `time_period` : Période temporelle
- `indicator_name` : Nom de l'indicateur
- `source_label` : Label de la source

**Table `t_macro_hicp_inflation`** (Inflation HICP)
- `id_inflation` : Clé primaire
- `date` : Date de l'observation
- `value` : Valeur de l'inflation
- `obs_status` : Statut de l'observation
- `time_period` : Période temporelle
- `indicator_name` : Nom de l'indicateur
- `source_label` : Label de la source

**Table `t_macro_unemployment_rate`** (Taux de chômage)
- `id_unemployment` : Clé primaire
- `date` : Date de l'observation
- `value` : Valeur du taux de chômage
- `obs_status` : Statut de l'observation
- `time_period` : Période temporelle
- `indicator_name` : Nom de l'indicateur
- `source_label` : Label de la source

**Table `t_macro_monetary_m3`** (Agrégat monétaire M3)
- `id_m3` : Clé primaire
- `date` : Date de l'observation
- `value` : Valeur du M3
- `obs_status` : Statut de l'observation
- `time_period` : Période temporelle
- `indicator_name` : Nom de l'indicateur
- `source_label` : Label de la source

### Vue `v_macro_indicators_daily_v1`
Vue unifiée des indicateurs macro-économiques avec granularité journalière.

**Fonctionnement :**
- Utilise `DATE_TRUNC('month', date)` pour propager les valeurs mensuelles sur tous les jours du mois
- Joint les 4 tables macro avec `FULL OUTER JOIN`
- Filtre les données à partir du 2010-07-14 (aligné sur la date de début du Bitcoin)

**Colonnes :**
- `date` : Date journalière
- `rate_mro` : Taux directeur BCE
- `inflation_rate` : Taux d'inflation HICP
- `unemployment_rate` : Taux de chômage
- `monetary_m3_rate` : Agrégat monétaire M3

**Objectif :** Faciliter les jointures avec les données Bitcoin journalières pour les analyses prédictives et le machine learning.

### Bonnes pratiques appliquées
- **Types Numeric au lieu de Float** : Garantit la précision financière (pas d'erreurs d'arrondi)
- **Contraintes d'unicité composites** : Évite les doublons tout en supportant plusieurs sources
- **Server defaults** : collected_at auto-généré avec `func.now()`
- **Convention de nommage** : Python attributes ≠ SQL column names via `Column("sql_name", Type)`
- **DATE_TRUNC pour jointures temporelles** : Propage les valeurs mensuelles sur les jours
- **Vues pour agrégation** : Évite la duplication de données tout en facilitant les requêtes

## Workflow d'enrichissement de la base de données

### 1. Collecte des données brutes
```bash
# Télécharger les données Bitcoin (CoinMarketCap)
# Fichier CSV manuel à placer dans data/raw/csvFile/

# Télécharger les indicateurs macro (BCE)
python scripts/collect/download_bce_mro.py
python scripts/collect/download_bce_HICP_Inflation.py
python scripts/collect/download_unemployment_rate.py
python scripts/collect/download_Monetary_aggregate_M3.py
```

### 2. Nettoyage des données
```bash
# Nettoyer les données Bitcoin
python scripts/clean/cleaned_Bitcoin_historical_data.py

# Nettoyer les indicateurs macro
python scripts/clean/cleaned_MRO.py
python scripts/clean/cleaned_HICP_inflation_data.py
python scripts/clean/cleaned_unemployment_rate_data.py
python scripts/clean/cleaned_Monetary_aggregate_M3.py
```

### 3. Concatenation des CSV Bitcoin (si nécessaire)
Si vous avez plusieurs CSV Bitcoin à fusionner :
```bash
python scripts/clean/concatenate_bitcoin_csvs.py
```
Ce script :
- Fusionne les CSV historiques et compléments
- Supprime les doublons
- Trie par date
- Produit `bitcoin_historical_cleaned_updated.csv`

### 4. Injection dans PostgreSQL
```bash
# Injecter les données Bitcoin (utilise bitcoin_historical_cleaned_updated.csv)
python scripts/injection_db_postgres/injection_data_btcoin.py

# Injecter les indicateurs macro
python scripts/injection_db_postgres/injection_data_mro.py
python scripts/injection_db_postgres/injection_data_Inflation.py
python scripts/injection_db_postgres/injection_data_unemployment.py
python scripts/injection_db_postgres/injection_data_aggregate_M3.py
```

**Note :** Le script `injection_data_btcoin.py` utilise automatiquement le fichier `bitcoin_historical_cleaned_updated.csv` produit par l'étape 3.

### 5. Migrations appliquées
Les migrations Alembic suivantes ont été appliquées :

**Migration 1 : `c24e71c09ba3`** - Restructuration de t_bitcoin_prices *(02/06/2026)*
- Ajout des colonnes : source, currency, granularity, collected_at
- Remplacement des types Float par Numeric pour la précision financière
- Contrainte d'unicité composite : (date, source, currency, granularity)

**Migration 2 : `325ae849c379`** - Standardisation des tables macro *(02/06/2026)*
- Ajout de la colonne `obs_status` dans toutes les tables macro
- Création de la vue `v_macro_indicators_daily_v1` avec DATE_TRUNC
- Jointures mensuelles propagées sur les jours pour alignement avec Bitcoin

**Migration 3 : `ccb59cb90494`** - Fix SEQUENCE pour t_bitcoin_prices.id *(05/06/2026)*
- Création de la SEQUENCE `t_bitcoin_prices_id_seq`
- Association de la SEQUENCE à la colonne id pour auto-incrémentation

### 6. Vérification de l'injection
Après l'injection, vérifiez que les données sont bien présentes :
```python
from database.conn_db.connect_postgresql import SessionLocal
from database.postgres.models.bitcoin_prices import BitcoinPrices
from sqlalchemy import text

db = SessionLocal()

# Vérifier le nombre de lignes Bitcoin
count = db.query(BitcoinPrices).count()
print(f"Nombre de lignes Bitcoin : {count}")

# Vérifier la plage de dates
first = db.query(BitcoinPrices).order_by(BitcoinPrices.date).first()
last = db.query(BitcoinPrices).order_by(BitcoinPrices.date.desc()).first()
print(f"Période couverte : {first.date} à {last.date}")

# Tester la vue macro
result = db.execute(text("SELECT * FROM v_macro_indicators_daily_v1 LIMIT 5;"))
for row in result:
    print(row)

db.close()
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
#### Installation des bibliothèques Python interagir avec MONGODB 
```bash
    # Installation de pymongo
    pip install pymongo
```
## Sauvegarde (Backup) des données stockées dans les bases PostgreSQL et MongoDB 
###  PostgreSQL 
```bash
    # Utilise pg_dump pour exporter la base et on exécute cette ligne de commande dans le terminal 
    #  Cela crée un fichier SQL qui pourra être restaurer plus tard avec psql
    pg_dump -U ton_user -d nom_de_la_db > sauvegarde_postgres.sql

    # Pour restaurer la base de donnée :
        # Si la base est déja existante
        #Cette commande exécute tous les ordres SQL contenus dans la sauvegarde
        psql -U ton_user -d nom_de_la_db -f sauvegarde_postgres.sql

        # Si elle n'est pas existante
        # Créér d'abord une base vide
        createdb -U ton_user nouvelle_base

        # Puis, restaurer les données
        psql -U ton_user -d nouvelle_base -f sauvegarde_postgres.sql
```
### MongoDB 
```bash
    # Utilise pg_dump pour exporter la base et on exécute cette ligne de commande dans le terminal bash
    mongodump --db nom_de_la_db --out ./backup_mongo/

    # Pour restaurer
    mongorestore --db nom_de_la_db ./backup_mongo/nom_de_la_db

```


# Configuration de l'API
## Schémas des entrées/sorties avec pydantic
```bash
    # Installation de la librairie pydantic
        pip install pydantic
```
## Installation des bibliothèques Python pour l'API
```bash
    # Installation de la librairie fastAPI
        pip install "fastapi[standard]"
        pip install "uvicorn[standard]"

    # Pour lancer FastAPI
        python -m api.main  
        uvicorn api.main:app --reload
```
## Installation des bibliothèques Python pour le cryptage des passwords
```bash
    # Installation de la librairie pour le cryptage des password en vue de la sécurisation de l'authentification sur l'API
        pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

---

## 📝 Maintenance de la documentation

### Mise à jour du changelog
Pour maintenir ce README à jour lors de futures modifications :

1. **Après chaque migration Alembic** : Ajouter l'entrée dans la section "Migrations appliquées" avec la date
   ```bash
   # La date de création se trouve dans le fichier de migration
   # Ligne : Create Date: YYYY-MM-DD HH:MM:SS
   ```

2. **Après des modifications majeures** : Mettre à jour la section "Historique du projet"
   - Date de la modification
   - Description concise des changements
   - pour les tâches complétées
   - pour les tâches en cours

3. **Après injection de données** : Mettre à jour les statistiques dans "Statut actuel"
   - Nombre de lignes
   - Période couverte
   - Sources disponibles

4. **Mise à jour de la date "Dernière mise à jour"** : Modifier la date dans le statut en haut du document

### Template pour nouvelles migrations
```markdown
**Migration X : `revision_id`** - Description courte *(JJ/MM/YYYY)*
- Modification 1
- Modification 2
- Modification 3
```

### Template pour changelog
```markdown
**JJ/MM/YYYY**
- ✅/🔄/❌ Description de l'action effectuée ou en cours
- Détails techniques si nécessaire
- Impact sur le projet
```

---

**Dernière actualisation complète du README : 2026-06-05**

