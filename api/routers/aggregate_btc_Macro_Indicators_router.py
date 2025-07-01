# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database.conn_db.connect_postgresql import get_db
from api.schemas.aggregate_btc_Macro_Indicators import BitcoinMacroIndicatorsResponse
from api.crud.crud_aggregate_btc_Macro_Indicators import get_bitcoin_macro_indicators_range
from datetime import date
from setup.logger_config import setup_logger

# Mise en place d'un logger pour le module de création des collections
name_file =os.path.splitext(os.path.basename(__file__))[0]
# set le logger du module en cours
logger = setup_logger(name_file)

# Création d’un routeur dédié aux routes relatives à l'aggrégation Bitcoin + Indicateurs macroéconomique
router = APIRouter(
    prefix="/api/v1/bitcoin-macro-indicators", # Préfixe commun pour toutes les routes 
    tags=["Aggregate Bitcoin + macroeconomic indicators"]    # Étiquette utilisée dans la documentation Swagger

)

@router.get("/", response_model=List[BitcoinMacroIndicatorsResponse])
def get_bitcoin_macro_indicators_view(
    start_date: date = Query(..., description="Date de début de la plage (YYYY-MM-DD)"),
    end_date: date = Query(..., description="Date de fin de la plage (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
        Endpoint pour récupérer les données Bitcoin croisées avec les indicateurs macroéconomiques.

        - start_date : date de début
        - end_date : date de fin

        Retourne : liste de données quotidiennes avec prix BTC + indicateurs macro.
    """
    return get_bitcoin_macro_indicators_range(db, start_date, end_date)
