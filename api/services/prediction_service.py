import sys
from pathlib import Path

import pandas as pd
from autogluon.tabular import TabularPredictor

from api.exceptions.model_exceptions import InferenceError, ModelUnavailableError
from setup.logger_config import setup_logger

#  retrouver le chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# initialiser le logger
name_module = Path(__file__).stem
logger = setup_logger(name_module)

# retrouver le chemin des modèles
model_path_7d = (
    project_root
    / "data"
    / "exports"
    / "autogluon_models"
    / "predictor_7d"
)

model_path_30d = (
    project_root
    / "data"
    / "exports"
    / "autogluon_models"
    / "predictor_30d"
)

def load_predictor(
    model_path: Path,
    horizon_days: int,
)-> TabularPredictor | None:
    """Charger les modeles à partir des chemins spécifiès"""
    if not model_path.exists():
        logger.error(
            "Le modèle %s non trouvé au chemin: %s.",
            horizon_days,
            model_path,
        )
        return None
    
    try:
        logger.info("Chargement de modèle depuis le chemin spécifié : %s.", model_path)

        predictor = TabularPredictor.load(str(model_path))

        logger.info(
            "Modele de l'horizon à %s jours chargé avec succès au demarrage de l'API",
            horizon_days
        )
        return predictor

    except Exception:
        logger.exception(
            "Echec du chargement du modèle %s jours",
            horizon_days
        )
        return None

# Charger les modèles au démarrage de l'API
predictor_7d = load_predictor(model_path_7d, 7)
predictor_30d = load_predictor(model_path_30d, 30)

def predict_volatility(
    features : dict, 
    horizon_days : int
) -> dict :
    
    """
        Prédire la volatilité du bitcoin à 7 et à 30 jours.

        Args:
            features (dict): Les variables explicatives d'entrée pour la prédiction.
            horizon_days (int): L'horizon de prédiction 7 ou 30 jours.

        Returns:
            dict: { 
                "horizon_days": int,
                "target": str,
                "predicted_volatility": float,
                "predicted_volatility_percent": float,
                "model_name": str,
            }
    """
    # Choisir le modèle correspondant à l'horizon demandé
    if horizon_days == 7:
        predictor = predictor_7d
    elif horizon_days == 30 :
        predictor = predictor_30d
    else:
        raise ValueError(
            "Horizon de prédiction non correspondant. Veuillez utiliser 7 ou 30."
        )
    
    if predictor is None:
        raise ModelUnavailableError(
            f"le modèle pour l' horizon {horizon_days} n' est pas disponible."
        )
    try:
        # Convertir les features en tableau de données pandas pour autogluon
        input_data = pd.DataFrame([features])
        # Faire la prédiction avec le modèle choisi
        prediction = predictor.predict(
            input_data,
            model="WeightedEnsemble_L2"
        )
        predicted_volatility = float(prediction.iloc[0])
    except Exception as error:
        raise InferenceError(
            f"la prédiction à {horizon_days} jours "
            "n’a pas pu être effectuée."
        ) from error
    return {
        "horizon_days" : horizon_days,
        "target" : predictor.label,
        "predicted_volatility" : predicted_volatility,
        "predicted_volatility_percent" : predicted_volatility * 100,
        "model_name" : "WeightedEnsemble_L2"
    }

