""" /api/v1/correlated-data/ - Route de croisement PostgreSQL + MongoDB
    Script : python  correlated_btc_rates_articlesFi.py
    Projet : VolatichainXplorerAI
    Date : 2025-06-28

    Méthode : GET
    Authentification : Requise (JWT token)
    Paramètres :
            - start: date de début (format YYYY-MM-DD)
            - end: date de fin (format YYYY-MM-DD)
            

    Description :
        Cette route permet de récupérer, pour une période donnée, deux types de données complémentaires :

        Les données agrégées quotidiennes issues de la vue PostgreSQL v_bitcoin_macro_indicators, qui regroupe les prix du Bitcoin et les indicateurs macroéconomiques (inflation, chômage, M3, MRO).

        Le nombre d'articles traitant du Bitcoin présents dans MongoDB sur la même période, filtrés par date de publication et mots-clés pertinents.

        Objectif :
        Fournir un aperçu croisé de l'évolution des facteurs économiques et de l'intensité médiatique autour du Bitcoin, en vue de futures analyses de corrélation ou de prédiction.

        Exemple d'appel:
        GET /api/v1/correlated-data/?start=2021-01-01&end=2021-12-31
        Authorization: Bearer <JWT_token>  

             Usage :
                python correlated_btc_rates_articlesFi.py
"""
# Charger les librairies nécessaires
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo.database import Database
from sqlalchemy.orm import Session

from api.auths.dependencies import get_current_user
from api.crud.crud_correlated_btc_macro_articles import (
    get_articles_btc_macroRates_by_date_range,
)
from api.schemas.correlated_btc_rates_articlesFi import CorrelatedResponse
from database.conn_db.connect_mongodb import get_mongodb
from database.conn_db.connect_postgresql import get_db
from database.postgres.models.users import Users
from setup.logger_config import setup_logger

# Mise en place du logger qui va permettre de suivre les actions de ce module
name_module = os.path.basename(__file__).split(".")[0]  # Récupère le nom du fichier sans l'extension

# Set le logger du module en cours
logger = setup_logger(name_module)

# Créer le routeur pour les endpoints liées aux données croisées
router = APIRouter(
    prefix = "/api/v1/correlated-btc-rates-articlesFi",
    tags = ["Correlated Bitcoin - Macro Indicators - Financial Articles"]
)

@router.get("/", response_model=CorrelatedResponse,)
def get_correlated_data(
    start_date: Annotated[
        date, Query(..., description="Date de début (YYYY-MM-DD)")
    ],
    end_date: Annotated[
        date, Query(..., description="Date de fin (YYYY-MM-DD)")
    ],
    pg_db: Annotated[Session, Depends(get_db)],
    mongo_db: Annotated[Database, Depends(get_mongodb)],
    current_user: Annotated[Users, Depends(get_current_user)],
):
    """
    Obtenir les indicateurs macroéconomiques, prix du bitcoin et nombre d'articles contenant 'bitcoin' pour une période donnée.
    """
    try:
        data = get_articles_btc_macroRates_by_date_range(pg_db, mongo_db, start_date, end_date)
        return data
    except HTTPException as e:
        logger.exception(
            "Erreur lors de la récupération des données ")
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception as e:
        logger.exception(
            " Erreur inattendue"
        )
        raise HTTPException(status_code=500, detail=str(e)) from e