""""
    API principale pour VolatiChainXplorerAI.
    Cette API expose des données relatives à la collecte des données qui sont les cours historiques du bitcoin sur la période de 2010 à 2025, des indicateurs macroéconomiques, ainsi que des informations financières complémentaires.
    Elle fournit des points d'accès pour :
    - Accéder à l'historique des cours du Bitcoin
    - Obtenir les différents taux de la Banque Centrale Européenne
    - Authentifier et gérer l'accès à l'API via un endpoint dédié
    L'objectif est de faciliter l'exploration, l'analyse et l'intégration de ces données pour les développeurs et utilisateurs finaux.
"""
# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from fastapi import FastAPI, Depends
from sqlalchemy import text
from database.conn_db.connect_postgresql import get_db
from database.conn_db.connect_mongodb import get_mongodb
from api.routers.bitcoin_prices_router import router as bitcoin_router
from api.routers.macro_indicators_router import router as macro_indicators_router
from api.routers.aggregate_btc_Macro_Indicators_router import router as bitcoin_macro_indicators_router
from api.routers.articles_financiers_router import router as articles_financiers_router
from api.routers.auth_router import router 
from api.routers.correlated_btc_rates_articlesFi_router import router as correlated_btc_rates_articlesFi_router
from api.routers.delete_user_account_router import router as deleted_user_router

# Charger l'API
app = FastAPI(
    title="API VolatiChainXplorer AI - Architecture en couches",
    description=(
        "Bienvenue sur l'API **VolatiChainXplorer AI**.\n\n"
        "Cette interface vous permet d'explorer, d'analyser et de croiser intelligemment :\n"
        "- des données macroéconomiques (taux directeurs, inflation, chômage, masse monétaire M3),\n"
        "- des données de marché liées à la volatilité du **Bitcoin**,\n"
        "- des articles financiers issus de sources spécialisées.\n\n"
        "**Fonctionnalités principales :**\n"
        "-  Architecture modulaire (CRUD, routes, schémas Pydantic, gestion d'exceptions)\n"
        "-  Validation rigoureuse des données avec **Pydantic**\n"
        "-  Gestion centralisée des erreurs personnalisées\n"
        "-  Restitution des données **PostgreSQL** et **MongoDB**\n"
        "-  Prêt pour intégration dans des dashboards ou outils d'analyse IA\n\n"
        "**Aperçu rapide des routes principales :**\n"
        "-  `/api/v1/bitcoin-prices` : Prix journaliers du Bitcoin (PostgreSQL)\n"
        "-  `/api/v1/macro-indicators` : Les indicateurs macroéconomiques de la BCE\n"
        "-  `/api/v1/articles-financiers` : Articles économiques (MongoDB)\n"
        "-  `/api/v1/correlated-btc-rates-articlesFi` : Données croisées entre les cours du Bitcoin, les indicateurs macroéconomiques et les articles financiers\n"
        "-  `/api/v1/auth` : Authentification et gestion des utilisateurs\n"
        "-  `/api/v1/delete-user-account` : Suppression du compte utilisateur\n"
    ),
    version="1.0.0"
)

# Inclure les routes
app.include_router(router)      # Routes d'authentification
# Page d'accueil de l'API
@app.get("/", tags=["Home Page"])
def welcome():
    return{
        # project → Présente le Nom et le version du projet
        "project": "VolatiChainXplorer AI - API v1.0 ",
        # description → Présente la finalité réelle de l'API
        "description": (
            "Bienvenue sur l'API VolatiChainXplorer AI. "
            "Cette interface vous permet d'explorer, d'analyser et de croiser des données économiques macroéconomiques "
            "et des données sur la volatilité du Bitcoin."
        ),
        # features → Présente ce que l' API propose d'intéressant ou de structurant
        "features": [
            " Architecture modulaire (CRUD, routes, schémas Pydantic, gestion d'exceptions)",
            " Validation rigoureuse des données avec Pydantic",
            " Gestion centralisée des erreurs personnalisées",
            " Restitution des données PostgreSQL et MongoDB",
            " Prêt pour intégration dans des dashboards ou outils d'analyse IA"
        ],
        # routes de l'API → Pour guider rapidement un utilisateur qui teste depuis Swagger
        "routes_API_VolatiChainXplorerAI": {
            "/api/v1/correlated-btc-rates-articlesFi": "Données croisées entre les cours du Bitcoin, les indicateurs macroéconomiques et les articles financiers",
            "/api/v1/auth": "Authentification et gestion des utilisateurs",
            "/api/v1/delete-user-account": "Suppression du compte utilisateur",
            "/api/v1//bitcoin-prices": "Prix journaliers du Bitcoin (PostgreSQL)",
            "/api/v1/macro-indicator": "Indicateurs macroéconomiques de la BCE",
            "/api/v1/articles-financiers": "Articles économiques et financiers relatifs au bitcoinet sa volatilité (MongoDB)",
        }
    }
# Inclure les routeurs
# Les cours du bitcoin 
app.include_router(bitcoin_router)

# Les indicateurs macroéconomiques
app.include_router(macro_indicators_router)


# Aggrégation du bitcoin et des indicateurs macroéconomiques
app.include_router(bitcoin_macro_indicators_router)

# Les articles financiers
app.include_router(articles_financiers_router)

# Les données croisées entre les cours du Bitcoin, les indicateurs macroéconomiques et les articles financiers
app.include_router(correlated_btc_rates_articlesFi_router)

# Supprimer le compte d'un utilisateur
app.include_router(deleted_user_router)

# Endpoint du controle de l'état de l'API
@app.get("/health",tags=["API health"])
def health_check():
    """
    Vérification de l'état de santé de l'API et des bases de données.

    Retourne :
    - status: "ok" si tout va bien, sinon "degraded"
    - database: "ok" si les connexions à PostgreSQL et à MongoDB fonctionnent
    - version: numéro de version de l'API

    par exemple:
    - "status": "ok" ou "degraded",
    - "postgresql": "ok" ou "error",
    - "mongodb": "ok" ou "error",
    - "version": "1.0.0"
    """
    # check de PostgreSQL
    try:
        with get_db() as pg_db:
            pg_db.execute(text("SELECT 1"))
            pg_status = "ok"
    except Exception as e:
        print(f"[POSTGRES ERROR] {e}")
        pg_status = "error"

    # Check de  MongoDB
    try:
        with get_mongodb() as mongo_db:
            mongo_db.command("ping")
            mongo_status = "ok"
    except Exception as e:
        print(f"[MONGO ERROR] {e}")
        mongo_status = "error"

    # Check global de l'API
    status = "ok" if pg_status == "ok" and mongo_status == "ok" else "degraded"

    return {
        "status": status,
        "database_postgres": pg_status,
        "database_mongo": mongo_status,
        "version": "1.0.0"
    }

# Endpoint de test de l'API
@app.get("/status", tags=["Test API"])
def get_status():
    return {"API": "running"}


