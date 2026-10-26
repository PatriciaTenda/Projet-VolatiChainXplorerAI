from datetime import date

import pandas as pd
import pytest

from api.services import feature_preparation_service


def test_prepare_features_for_prediction_success(
    monkeypatch
):
    """ Ce test vérifie que la fonction prepare_features_for_prediction fonctionne correctement. """
    
    expected_date = date(2026, 10, 9)
    
    # Simuler la derniere date recupérer de la base de données
    monkeypatch.setattr(
        feature_preparation_service,
        "get_latest_available_date",        
        lambda db: expected_date,        
    )
    
    # Simuler les lignes récuperées dans postgresql
    class FakeRow:
        def __init__(self):
            self._mapping = {                    
                "day": expected_date,
                "open": 66000.0,
                "high": 67000.0,
                "low": 65000.0,
                "close": 66500.0,
                "volume": 1000000.0,
                "market_cap": 1300000000.0,
                "rate_mro": 2.4,
                "inflation_rate": 3.3,
                "unemployment_rate": 6.4,
                "monetary_m3_rate": 3.38,
            }
    
    monkeypatch.setattr(
        feature_preparation_service,
        "get_bitcoin_macro_indicators_range",
        lambda db, start_date, end_date: [FakeRow()]
    )
    
    # Préparer les données
    monkeypatch.setattr(
        feature_preparation_service,
        "prepare_data",
        lambda data : data
    )
    
    expected_features = {
        col : float(index)
        for index, col in enumerate(
            feature_preparation_service.FEATURES_COLUMNS,
            start=1
        ) 
    }
    
    fake_ingineering_features = pd.DataFrame(
        [expected_features],
        index=pd.to_datetime([expected_date])
    )
    
    # Préparer les features pour la prédiction
    monkeypatch.setattr(
        feature_preparation_service,
        "create_features",
        lambda db: fake_ingineering_features
    )
    features, feature_date = feature_preparation_service.prepare_features_for_prediction(
        db = object()        
    )
    
    assert len(features)  == 15
    assert feature_date == expected_date
    assert features == expected_features
    assert set(features) == set(feature_preparation_service.FEATURES_COLUMNS)
    
    
    # =================================== teste d'historique insuffisant de données===========================
    
def test_prepare_features_with_insufficient_history(monkeypatch):
    """Vérifier qu’un historique insuffisant provoque une ValueError."""
    
    expected_date = date(2026, 10, 9)
        
    # Simuler la derniere date recupérer de la base de données
    monkeypatch.setattr(
        feature_preparation_service,
        "get_latest_available_date",        
        lambda db: expected_date,        
    )
    
    # Simuler les lignes récuperées dans postgresql
    class FakeRow:
        def __init__(self):
            self._mapping = {                    
                "day": expected_date,
                "open": 66000.0,
                "high": 67000.0,
                "low": 65000.0,
                "close": 66500.0,
                "volume": 1000000.0,
                "market_cap": 1300000000.0,
                "rate_mro": 2.4,
                "inflation_rate": 3.3,
                "unemployment_rate": 6.4,
                "monetary_m3_rate": 3.38,
            }
    
    monkeypatch.setattr(
        feature_preparation_service,
        "get_bitcoin_macro_indicators_range",
        lambda db, start_date, end_date: [FakeRow()]
    )
    with pytest.raises( 
        ValueError, 
        match="L’historique disponible ne permet pas de calculer les variables"
    ):
        feature_preparation_service.prepare_features_for_prediction(
            db=object()
        )
        
# ======================================== test d'absence de données ===========================
def test_prepare_features_no_data(monkeypatch):
    """Vérifier qu’une absence de données provoque une ValueError."""

    expected_date = date(2026, 10, 9)
        
    # Simuler la derniere date recupérer de la base de données
    monkeypatch.setattr(
        feature_preparation_service,
        "get_latest_available_date",        
        lambda db: expected_date,        
    )

    # Simuler l'absence de lignes récuperées dans postgresql
    monkeypatch.setattr(
        feature_preparation_service,
        "get_bitcoin_macro_indicators_range",
        lambda db, start_date, end_date: []
    )
    with pytest.raises( 
        ValueError, 
        match="Aucune donnée disponible pour la plage de dates spécifiée."
    ):
        feature_preparation_service.prepare_features_for_prediction(
            db=object()
        )