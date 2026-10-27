# Charger les bibliothèques nécessaires
import sys
from datetime import date
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.auths.dependencies import require_user_or_admin
from api.monitoring.metrics import (
    INPUT_DATA_AGE_DAYS,
    PREDICTED_VOLATILITY,
    PREDICTION_DURATION,
    PREDICTION_REQUESTS_TOTAL,
)
from api.schemas.prediction import (
    VolatilityPredictionRequest,
    VolatilityPredictionResponse,
)
from api.services.feature_preparation_service import (
    prepare_features_for_prediction,
)
from api.services.prediction_service import predict_volatility
from database.conn_db.connect_postgresql import get_db
from database.postgres.models.users import Users
from setup.logger_config import setup_logger

# Récuperer le chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Definir le logger
name_module = path = Path(__file__).stem
logger = setup_logger(name_module)

PREDICTION_RESPONSES = {
    400: {
        "description": "Horizon invalide ou données insuffisantes"
    },
    401: {
        "description": "Authentification requise"
    },
    403: {
        "description": "Utilisateur non autorisé"
    },
    500: {
        "description": "Erreur interne pendant la prédiction"
    },
}


# Création du routeur pour les prédictions
router = APIRouter(
    prefix="/api/v1/bitcoin/volatility/predictions", # Préfixe commun pour toutes les routes 
    tags=["Bitcoin Volatility predictions"]
)

@router.post(
    "/manual/{horizon_days}", 
    response_model=VolatilityPredictionResponse,
    responses=PREDICTION_RESPONSES
)
def get_volatility_prediction(
    
    request : VolatilityPredictionRequest,
    horizon_days: int,
    current_user : Annotated[
        Users, 
        Depends(require_user_or_admin)
    ],
):
    """Obtenir la prédiction de la volatilité du Bitcoin pour un horizon donné (7 ou 30 jours)"""
 
# Vérifier les paramètres d'entrée
    if horizon_days not in [7, 30]:
        logger.error(
            "Horizon invalide : %s",
            horizon_days
        )
        
        raise HTTPException(
            status_code= 400,
            detail="Horizon invalide. Les valeurs acceptées sont 7 ou 30 jours."
        )
        
# Transformer les données validées en dictionnaire   
    features = request.model_dump()
    
# Appeler le service de prédiction et retourner la réponse
    try:
        
        return  predict_volatility(features, horizon_days)
    
    except ValueError as error:
        logger.warning(
            "Erreur lors de la prédiction de la volatilité : %s", 
            error
        )
        raise HTTPException(
            status_code=400,
            detail="Erreur sur les données d'entrée pour la prédiction de la volatilité."
        ) from error
    except Exception as error:
        logger.exception("Erreur lors de la prédiction de la volatilité")
        raise HTTPException(
            status_code=500,
            detail="Erreur interne lors de la prédiction de la volatilité."
        ) from error   
        
        
        
@router.post(
    "/latest/{horizon_days}",
    response_model=VolatilityPredictionResponse,
    responses=PREDICTION_RESPONSES
)
def get_latest_volatility_prediction(
    horizon_days: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[
        Users,
        Depends(require_user_or_admin),
    ],
):
    """
        Prédire la volatilité à partir des dernières données disponibles.
    """
    # Définir les variables qui servent à préparer les valeurs qui seront associées au label de Prometheus
    route_name = "latest"
    horizon_label = str(horizon_days)
        
    # Vérifier que l’horizon demandé est autorisé
    if horizon_days not in [7, 30]:
        logger.error(
            "Horizon invalide : %s",
            horizon_days,
        )
        
        # Incrémenter le compteur de requêtes de prédiction avec le statut "invalid_horizon"
        PREDICTION_REQUESTS_TOTAL.labels(
            route=route_name,
            horizon=horizon_label,
            status="invalid_horizon"
        ).inc()

        raise HTTPException(
            status_code=400,
            detail=(
                "Horizon invalide. Les valeurs acceptées "
                "sont 7 ou 30 jours."
            ),
        )

    try:
        # Mesurer la préparation et la prédiction de la volatilité
        with PREDICTION_DURATION.labels(
            route=route_name,
            horizon=horizon_label
        ).time():
            # Préparer automatiquement les 15 variables
            features, features_date = prepare_features_for_prediction(db)

            # Effectuer la prédiction
            result = predict_volatility(
                features,
                horizon_days,
            )
        # Enregistrer la valeur prédite
        PREDICTED_VOLATILITY.labels(
            horizon=horizon_label            
        ).observe(
            result["predicted_volatility"]
        )
        
        # Calculer l'ancienneté des données utilisées
        data_age_days = (
            date.today() - features_date
        ).days
        
        
        INPUT_DATA_AGE_DAYS.labels(
            horizon=horizon_label
        ).set(data_age_days)
        
        # compter les prédiction reussies
        PREDICTION_REQUESTS_TOTAL.labels(
            route=route_name,
            horizon=horizon_label,
            status="success"
        ).inc()
        
        # Ajouter la date des données utilisées
        result["data_date"] = features_date       
        
        logger.info(
            "Prédiction à %s jours réalisée avec les données du %s.",
            horizon_days,
            features_date,
        )

        return result

    except ValueError as error:
        logger.warning(
            "Données insuffisantes pour la prédiction : %s",
            error,
        )
        
        # Compter les requêtes de prédiction échouées en raison d'une indisponibilité de données
        PREDICTION_REQUESTS_TOTAL.labels(
            route=route_name,
            horizon=horizon_label,
            status="data_error"
        ).inc()
        
        raise HTTPException(
            status_code=400,
            detail="Aucune donnée disponible pour la prédiction.",
        ) from error

    except Exception as error:
        logger.exception(
            "Erreur pendant la prédiction automatique."
        )
        
        # Compter les requêtes de prédiction échouées en raison d'une erreur interne
        PREDICTION_REQUESTS_TOTAL.labels(
            route=route_name,
            horizon=horizon_label,
            status="error"
        ).inc()
        
        raise HTTPException(
            status_code=500,
            detail=(
                "Une erreur interne est survenue "
                "pendant la prédiction."
            ),
        ) from error