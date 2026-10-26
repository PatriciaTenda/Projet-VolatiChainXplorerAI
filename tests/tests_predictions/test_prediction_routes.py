import sys
from datetime import date
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api.auths.dependencies import require_user_or_admin
from api.main import app
from api.routers import prediction_router
from database.conn_db.connect_postgresql import get_db

# Chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Initialisation du client de test pour l'application FastAPI
client = TestClient(app)


# ============================================ test invalid authentication ================================================================

def test_latest_prediction_required_authentication():
     """Ce script de test vérifie l'authentification de l'utilisateur pour les routes de prédiction"""
     response = client.post("/api/v1/bitcoin/volatility/predictions/latest/7")
     assert response.status_code == 401
     assert response.json() == {"detail": "Authentification requise"}
     assert response.headers["www-authenticate"] == "Bearer" 


# ============================================ test invalid horizon ================================================================
def fake_authenticate_user():
     """Ce script simmule le comportement d'un utilisateur authentifié"""
     return object()

def fake_database():
     """
          Ce script simmule l'utilisation d'une connexion à la base de données.
          Evite l'utilisation de la base de données réelle
     """
     yield object()
     

def test_latest_prediction_reject_invalid_horizon():
     """Ce script de test vérifie le rejet d'un horizon invalide pour les routes de prédiction"""
     
     app.dependency_overrides[require_user_or_admin] = (
          fake_authenticate_user
     )
     
     app.dependency_overrides[get_db] = (
          fake_database
     )
     
     try:    
         response = client.post("/api/v1/bitcoin/volatility/predictions/latest/15")
         
         assert response.status_code == 400
         assert response.json() == {
              "detail":(
                   "Horizon invalide. Les valeurs acceptées sont 7 ou 30 jours."
              )
          }
         
         
     finally:
          app.dependency_overrides.clear()
     

# ============================================ test valid horizon ================================================================
@pytest.mark.parametrize(
     "horizon_days, target, predicted_volatility",
     [
          (7, "target_volatility_7d", 0.017),
          (30, "target_volatility_30d", 0.020)
     ], 
)
def test_latest_prediction_valid_horizon(
     horizon_days,
     target,
     predicted_volatility,
     monkeypatch,
     
):
    """Ce scrupt teste le bon fonctionnement de la route de prédiction pour un horizon 7 ou 30 jours"""
    
    app.dependency_overrides[require_user_or_admin] = (
         fake_authenticate_user
    )
    
    app.dependency_overrides[get_db] = (
         fake_database
    )
    
    # Simulation de la préparation des features pour la base de données
    def fake_prepare_features(db):
     """Simule la préparation des features pour la base de données"""
     return {}, date(2026, 10, 9)

    # Simmulation de la prédiction de la volatilité
    def fake_prediction_volatility(features, horizon_days):
         """Simule la prediction de la volatilité"""
         return {
              "horizon_days": horizon_days,
              "target": target,
              "predicted_volatility": predicted_volatility,
              "predicted_volatility_percent": (
                   predicted_volatility *100
               ),
              "model_name": "WeightedEnsemble_L2",
         }
         
    monkeypatch.setattr(
         prediction_router,
         "prepare_features_for_prediction",
         fake_prepare_features,
    )
    
    monkeypatch.setattr(
         prediction_router,
         "predict_volatility",
         fake_prediction_volatility
    )
    
    try:
         response = client.post(
              f"/api/v1/bitcoin/volatility/predictions/latest/{horizon_days}"
          )
         
         data_result = response.json()
         
         assert response.status_code == 200
         assert data_result["horizon_days"] == horizon_days
         assert data_result["target"] == target
         assert data_result["predicted_volatility"] == pytest.approx(
              predicted_volatility
          )
         assert data_result["predicted_volatility_percent"] == pytest.approx(
              predicted_volatility * 100
          )
         assert data_result["model_name"] == "WeightedEnsemble_L2"
         assert data_result["data_date"] == "2026-10-09"

    finally:
         app.dependency_overrides.clear()
         
         
# ==================================== test données invalides pendant la prédiction =============================================
def test_latest_prediction_invalid_data(
     monkeypatch,
):
     """ Ce script teste le comportement de la route de prédiction lorsque des données sont invalides"""         
     app.dependency_overrides[require_user_or_admin] = (
          fake_authenticate_user
     )
     
     app.dependency_overrides[get_db] = (
          fake_database
     )
     
     def fake_prepare_features(db):
         """Simule la préparation des features pour la base de données"""
         raise ValueError(
              "Aucune donnée disponible pour la prédiction."
          )   
    
     monkeypatch.setattr(
          prediction_router,
          "prepare_features_for_prediction",
          fake_prepare_features,
     )
     
     try:
          response = client.post(
               "/api/v1/bitcoin/volatility/predictions/latest/7"
          )
          
          assert response.status_code == 400
          assert response.json() == {"detail": "Aucune donnée disponible pour la prédiction."}
     finally:
          app.dependency_overrides.clear()

# ==================================== test echec de la prédiction =============================================
@pytest.mark.parametrize(
     "horizon_days,target,predicted_volatility",
     [
         (7, "target_volatility_7d", 0.05),
     ]
)
def test_latest_prediction_invalid(
     monkeypatch, 
     horizon_days, 
     target, 
     predicted_volatility
):
     """ Ce script teste le comportement de la route de prédiction lorsque des données sont invalides"""         
     app.dependency_overrides[require_user_or_admin] = (
          fake_authenticate_user
     )
     
     app.dependency_overrides[get_db] = (
          fake_database
     )
     
     def fake_prepare_features(db):
         """Simule la préparation des features pour la base de données"""
         return None, None
    
     def fake_prediction_volatility(features, horizon_days):
         """Simule la prediction de la volatilité"""
         return object()
    
     monkeypatch.setattr(
          prediction_router,
          "prepare_features_for_prediction",
          fake_prepare_features,
     )

     monkeypatch.setattr(
          prediction_router,
          "predict_volatility",
          fake_prediction_volatility
     )
     
     try:
          response = client.post(
               f"/api/v1/bitcoin/volatility/predictions/latest/{horizon_days}"
          )
          
          assert response.status_code == 500
          assert response.json() == {"detail": "Une erreur interne est survenue pendant la prédiction."}
     finally:
          app.dependency_overrides.clear()
