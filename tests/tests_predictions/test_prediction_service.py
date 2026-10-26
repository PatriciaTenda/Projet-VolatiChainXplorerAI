import sys
from pathlib import Path

# Chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

import pandas as pd
import pytest

from api.services import prediction_service


# Simmuler les prédicteurs de volatilité autogluon
class FakePredictor:
    def __init__(self, target, predicted_volatility):
        self.label = target
        self.predicted_volatility = predicted_volatility
        
    def predict(self, input_data, model):
        """Simule la prédiction de la volatilité"""
        assert isinstance(input_data, pd.DataFrame)
        assert model == "WeightedEnsemble_L2"
        return pd.Series([self.predicted_volatility])
            
            
            
# ====================================== test horizon_days valid ======================================
@pytest.mark.parametrize(
    "horizon_days, predictor_name, target, predicted_volatility",
    [
      (
        7, 
       "predictor_7d", 
       "target_volatility_7d", 
       0.017
      ),
      
      (
        30, 
        "predictor_30d", 
        "target_volatility_30d", 
        0.020
      )
    ],
)
def test_prediction_valid_horizon_days(
    horizon_days,
    predictor_name,
    target,
    predicted_volatility,
    monkeypatch,
):    
    """ Ce script à pour but de tester les horizons de prédiction du service"""
    
    # Créer des instances de FakePredictor pour les horizons 7 et 30 jours
    fake_predictor = FakePredictor(
        target, 
        predicted_volatility
    )
    
    monkeypatch.setattr(
        prediction_service,
        predictor_name,
        fake_predictor       
    )
    
    # simmuler un dictictionnaire de features pour les tests
    fake_features = {
        "log_return": 0.01,
        "volatility_7d": 0.02,
        "volatility_30d": 0.03,
    }
    
    #  Appeler le véritable service avec le faux prédicteur    
    result = prediction_service.predict_volatility(
        fake_features, 
        horizon_days
    )
    
    assert result["horizon_days"] == horizon_days
    assert result["target"] == target
    assert result["predicted_volatility"] == pytest.approx(predicted_volatility)
    assert result["predicted_volatility_percent"] == pytest.approx(predicted_volatility * 100)
    assert result["model_name"] == "WeightedEnsemble_L2"
    
    
    
# ============================== test horizon_days invalid ==============================

def test_prediction_invalid_horizon_days():
    
    """ Ce script à pour but de vérifier qu’un horizon différent de 7 et 30 est refusé."""
    
    # simmuler un dictictionnaire de features pour les tests
    fake_features = {
        "log_return": 0.01,
        "volatility_7d": 0.02,
        "volatility_30d": 0.03,
    }

    # Simuler la fonction de prédiction de la volatilité aux horizons 7 et 30 jours   
    with pytest.raises(ValueError, match="7 ou 30."):
        prediction_service.predict_volatility(
            fake_features, 
            15
        )
    
    
    



