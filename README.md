# VolatiChainXplorerAI

<p align="center">
  <img src="frontend/images/Logo_VolatiChainXplorerAI.png" alt="VolatiChainXplorerAI" width="220" />
</p>

<div align="center">
  <strong>Data engineering + market intelligence for Bitcoin volatility</strong>
</div>

VolatiChainXplorerAI est un projet de data engineering et d’analyse de marché appliqué au Bitcoin. Son objectif est de collecter, structurer et croiser des données issues de plusieurs sources — prix historiques, indicateurs macroéconomiques, articles financiers et signaux de marché — afin de fournir une base exploitable pour l’analyse, la recherche et la prédiction de la volatilité du Bitcoin.

## Vision du projet

Le projet combine trois dimensions clés :

1. Collecte et préparation de données financières et macroéconomiques
2. Stockage robuste et évolutif dans PostgreSQL et MongoDB
3. Exploitation via une API FastAPI et des services de prédiction de volatilité

L’objectif est de créer une plateforme technique lisible, modulaire et extensible, adaptée à la recherche, au benchmarking et à la démonstration de solutions IA appliquées à la finance.

## État du projet

Le projet est aujourd’hui à un stade fonctionnel avancé, avec les éléments suivants déjà opérationnels :

- ✅ Collecte de données multi-sources (Bitcoin, macroéconomie, articles financiers)
- ✅ Base PostgreSQL structurée pour les prix BTC et les indicateurs macroéconomiques
- ✅ Base MongoDB configurable pour le stockage des contenus financiers
- ✅ API FastAPI modulaire, documentée et exploitable
- ✅ Prédictions de volatilité du Bitcoin à 7 et 30 jours
- ✅ Monitoring avec Prometheus, Grafana et Alertmanager
- ✅ Scripts de nettoyage, injection et mise à jour des données
- ✅ Tests automatisés sur l’API, les routes de prédiction et le monitoring
- ✅ Documentation technique et benchmark AutoML dans le dossier `docs/`
- ⚠️ Front-end non finalisé : le dépôt contient des ressources visuelles et de branding, mais pas encore une interface web complète

## Stack technique

- Python 3.12+
- FastAPI pour l’API REST
- SQLAlchemy pour l’accès aux données PostgreSQL
- MongoDB pour les contenus financiers et textuels
- PostgreSQL pour les données structurées et historiques
- Alembic pour les migrations de schéma
- Docker / Docker Compose pour l’infrastructure locale
- Prometheus + Grafana + Alertmanager pour le monitoring
- Pytest pour les tests automatisés
- Pandas / NumPy pour la préparation des données

## Fonctionnalités clés

### 1) Collecte et ingestion de données

Le projet collecte des données depuis plusieurs sources, notamment :

- CoinGecko, CoinMarketCap et yFinance pour les prix historiques du Bitcoin
- Données macroéconomiques de la BCE : MRO, inflation, chômage et M3
- Articles financiers et contenus de presse spécialisés
- Scripts d’injection et de mise à jour vers PostgreSQL et MongoDB

### 2) Base de données

Le projet organise les données dans plusieurs modèles et schémas dédiés :

- `database/postgres/models/bitcoin_prices.py`
- `database/postgres/models/macro_indicators.py`
- `database/postgres/models/users.py`
- Tables et vues PostgreSQL pour l’analyse temporelle et les jointures

### 3) API REST

L’application FastAPI exposée dans `api/main.py` permet notamment de :

- consulter les prix historiques du Bitcoin
- accéder aux indicateurs macroéconomiques de la BCE
- lire les articles financiers stockés dans MongoDB
- combiner les données BTC + macro + articles
- authentifier les utilisateurs
- supprimer un compte utilisateur
- obtenir des prédictions de volatilité à 7 et 30 jours
- surveiller les métriques de prédiction via Prometheus

### 4) Prédiction de volatilité

Le backend intègre des services de préparation des features et de prédiction pour deux horizons :

- 7 jours
- 30 jours

Les routes de prédiction sont sécurisées et exposent des métriques de monitoring pour suivre les performances et les erreurs.

### 5) Monitoring et observabilité

Le projet embarque :

- Prometheus pour la collecte des métriques
- Grafana pour la visualisation
- Alertmanager pour la gestion des alertes
- Endpoint `/metrics` pour exposer les métriques de prédiction

## Architecture du dépôt

```text
Projet-VolatiChainXplorerAI/
├── api/                          # API FastAPI, routers, services, auth, schemas
│   ├── auths/
│   ├── crud/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── main.py
│   └── README_API.md
├── database/                    # Connexions aux bases et modèles SQLAlchemy
│   ├── conn_db/
│   ├── mongo/
│   └── postgres/
├── data/                        # Données brutes, nettoyées et exportées
│   ├── raw/
│   ├── cleaned/
│   └── exports/
├── docs/                        # Veille, benchmark, preuves sprint, documentation
│   ├── benchmark/
│   ├── veille/
│   ├── preuves_by_sprint/
│   └── readme_docs.md
├── frontend/                    # Assets visuels et branding du projet
│   └── images/
├── monitoring/                  # Config Prometheus / Grafana / Alertmanager
├── notebooks/                   # Notebooks d’analyse et prototypage
├── scripts/                     # Collecte, nettoyage, injection, mise à jour
│   ├── collect/
│   ├── clean/
│   ├── injection_db_mongo/
│   ├── injection_db_postgres/
│   └── update/
├── setup/                       # Configuration globale et logging
├── tests/                       # Tests Pytest (API, CRUD, monitoring, prédictions)
├── .env                         # Variables d’environnement locales
├── .gitignore
├── alembic.ini
├── docker-compose.yaml
├── Dockerfile
├── pytest.ini
├── requirements.txt
├── README.md
└── ...
```

## Démarrage rapide

### 1) Cloner le dépôt

```bash
git clone https://github.com/PatriciaTenda/Projet-VolatiChainXplorerAI.git
cd Projet-VolatiChainXplorerAI
```

### 2) Créer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# ou .venv\Scripts\activate   # Windows
```

### 3) Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4) Démarrer l’infrastructure locale

```bash
docker compose up -d
```

Cela lance :

- PostgreSQL sur `localhost:5433`
- MongoDB sur `localhost:27017`
- Prometheus sur `localhost:9090`
- Grafana sur `localhost:3000`
- Alertmanager sur `localhost:9093`

### 5) Lancer l’API

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Puis ouvrir :

- `http://localhost:8000/docs`
- `http://localhost:8000/health`

## API et endpoints

Endpoints principaux :

- `GET /` : page d’accueil de l’API
- `GET /health` : vérification de santé de l’API et des bases
- `GET /status` : statut de test
- `POST /api/v1/auth/login` : authentification
- `GET /api/v1/bitcoin-prices` : prix historiques du Bitcoin
- `GET /api/v1/macro-indicators` : indicateurs macroéconomiques
- `GET /api/v1/articles-financiers` : articles financiers
- `GET /api/v1/correlated-btc-rates-articlesFi` : données croisées
- `POST /api/v1/bitcoin/volatility/predictions/latest/7` : prédiction à 7 jours
- `POST /api/v1/bitcoin/volatility/predictions/latest/30` : prédiction à 30 jours
- `GET /metrics` : métriques Prometheus

## Tests

Le dépôt contient une suite de tests pour valider les composants critiques :

```bash
pytest
```

Les tests couvrent notamment :

- vérification de l’état des services
- routes et logique de prédiction
- préparation des features
- monitoring Prometheus
- CRUD et intégration de données

## Documentation complémentaire

Le projet inclut une documentation détaillée dans plusieurs dossiers :

- `docs/readme_docs.md` : vue d’ensemble de la documentation projet
- `docs/benchmark/` : benchmark des outils AutoML et comparatifs techniques
- `docs/veille/` : veille technologique et synthèses
- `api/README_API.md` : documentation dédiée à l’API
- `notebooks/` : notebooks d’analyse exploratoire

## Roadmap

Axes de progression identifiés :

- finalisation d’une interface web front-end dédiée
- enrichissement des modèles de prédiction avec de nouvelles features
- ajout de dashboards métier plus complets sur Grafana
- automatisation accrue du workflow de collecte et de mise à jour
- sécurisation avancée des flux d’authentification et de déploiement

## Licence et usage

Ce projet est conçu dans un cadre académique et de démonstration. Il peut servir de base pour des projets plus avancés de data engineering, de data science appliquée au marché crypto ou de recherche en finance quantitative.

## Références

- GitHub : `https://github.com/PatriciaTenda/Projet-VolatiChainXplorerAI`
- Documentation projet : `docs/readme_docs.md`
- Documentation API : `api/README_API.md`

---

<p align="center">
  <i>VolatiChainXplorerAI — turning market signals into actionable intelligence.</i>
</p>
