# charger les librairies nécessaires
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.crud.crud_aggregate_btc_Macro_Indicators import (
    get_bitcoin_macro_indicators_range,
)
from scripts.build_dataset.build_features_engineering import (
    FEATURES_COLUMNS,
    create_features,
    prepare_data,
)
from setup.logger_config import setup_logger

# Chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Definir le logger
module_name = Path(__file__).stem
logger = setup_logger(module_name)

# ======================= feature pour récupérer la dernière date disponible ========================
def get_latest_available_date(db: Session):
    """
    Purpose:
        Récupère la dernière date disponible dans la vue.

    Args:
        db (Session): La session de base de données.

    Returns:
        date: La dernière date disponible.
    """
    query = text(
        """
            SELECT MAX(day)  
            FROM public.v_bitcoin_macro_indicator_daily
        """
    )
    
    try:
        latest_date = db.execute(query).scalar()
    except SQLAlchemyError:
        logger.exception("Erreur lors de la récupération de la dernière date disponible.")
        raise ValueError("Erreur lors de la récupération de la dernière date disponible.")
    
    if latest_date is None:
        logger.warning("Aucune date disponible dans la vue.")
        raise ValueError("Aucune données bitcoin et macroéconomiques disponibles dans la vue.")    
    return latest_date
    
# ======================= feature pour préparer les données pour la prédiction ========================

def prepare_features_for_prediction(
    db : Session
) -> tuple[dict[str, float], date]:
    """
    Prépare les features pour la prédiction.

    Args:
        db (Session): La session de base de données.

    Returns:
        tuple[dict[str, float], date]: Un tuple contenant les features préparées pour la prédiction et la date correspondante.
    """
    # Récupérer la dernière date disponible
    latest_date = get_latest_available_date(db)
    
    # Récupérer les données sur une plage de dates large de 90 jours
    
    start_date=latest_date - timedelta(days=90)
    
    rows = get_bitcoin_macro_indicators_range(
        db=db,
        start_date=start_date,
        end_date=latest_date,  
    )
    
    if not rows :
        logger.warning(
            "Aucune donnée disponible pour la plage de dates spécifiée."
        )
        raise ValueError(
            "Aucune donnée disponible pour la plage de dates spécifiée."
        )
        
    # Transformer la ligne sql récupérée en DataFrame
    data = pd.DataFrame(
        [
            dict(row._mapping) for row in rows
        ]
    )
    
    # Renommer la colonne 'day' en 'date' pour correspondre aux features attendues
    data = data.rename(columns={"day": "date"})
    
    # Colonnes qui doivent contenir des nombres
    numeric_columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "market_cap",
        "rate_mro",
        "inflation_rate",
        "unemployment_rate",
        "monetary_m3_rate",
    ]
    
    # Convertir les colonnes récupérées en type numérique
    data[numeric_columns] = data[numeric_columns].apply(
        pd.to_numeric, 
        errors="coerce"
    )
    
    # Préparer les données pour la création des features
    data = prepare_data(data)
    
    # Créer les features à partir des données préparées
    data = create_features(data)
    
    # Récupérer uniquement les features nécessaires pour la prédiction
    data_for_prediction = data.dropna(subset=FEATURES_COLUMNS)
    
    if data_for_prediction.empty:
        logger.warning(
             "L’historique disponible ne permet pas de calculer les variables."   
        )
        raise ValueError(
            "L’historique disponible ne permet pas de calculer les variables."
        )
        
    # Récupérer les dernières lignes de données les plus récentes pour la prédiction
    latest_row = data_for_prediction.iloc[-1]
    
    features = {
        col: float(latest_row[col]) for col in FEATURES_COLUMNS
    }
    
    features_date = pd.to_datetime(
        data_for_prediction.index[-1]
    ).date()
    
    return features, features_date
    
    
    
    