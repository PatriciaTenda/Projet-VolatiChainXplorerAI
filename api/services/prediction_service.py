import sys
from pathlib import Path

import pandas as pd
from autogluon.tabular import TabularPredictor

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

# Vérifier et charger les modèles une seule fois au demarrage de l'API
if not model_path_7d.exists() or not model_path_30d.exists():
    logger.error("Les modèles n'ont pas été trouvés aux chemins spécifiés.")
    raise FileNotFoundError(
        "Les modèles n'ont pas été trouvés aux chemins spécifiés : - %s - %s",
        model_path_7d, model_path_30d,
    )
    
logger.info("Chargement des modèles depuis les chemins spécifiés.")

predictor_7d = TabularPredictor.load(str(model_path_7d))
predictor_30d = TabularPredictor.load(str(model_path_30d))

logger.info("Modeles chargés avec succès au demarrage de l'API")


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
        
    # Convertir les features en tableau de données pandas pour autogluon
    input_data = pd.DataFrame([features])
    
    # Faire la prédiction avec le modèle choisi
    prediction = predictor.predict(
        input_data,
        model = "WeightedEnsemble_L2"
    )
    
    predicted_volatility = float(prediction.iloc[0])
    
    return {
        "horizon_days" : horizon_days,
        "target" : predictor.label,
        "predicted_volatility" : predicted_volatility,
        "predicted_volatility_percent" : predicted_volatility * 100,
        "model_name" : "WeightedEnsemble_L2"
    }

