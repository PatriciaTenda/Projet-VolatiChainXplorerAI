import sys
from pathlib import Path

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
)

#  retrouver le chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))


"""
Métriques permettant de surveiller le fonctionnement des prédictions.

Ces quatre métriques répondent chacune à une question :

- PREDICTION_REQUESTS_TOTAL :
  combien de prédictions réussissent ou échouent ?

- PREDICTION_DURATION :
  combien de temps prend une prédiction ?

- PREDICTED_VOLATILITY :
  quelles valeurs le modèle produit-il ?

- INPUT_DATA_AGE_DAYS :
  les données utilisées sont-elles récentes ?
"""

# Compter le nombre de demandes(requêtes) de prédiction
PREDICTION_REQUESTS_TOTAL = Counter(
    "volatichainxplorerai_prediction_counter_request",
    "Nombre total de requêtes de prédiction effectuées.",
    ["route","horizon", "status"]
)

# Mesurer la durée des requêtes de prédiction
PREDICTION_DURATION = Histogram(
    "volatichainxplorerai_prediction_duration_seconds",
    "Durée des predictions en secondes.",
    ["route", "horizon"]
)

# Répartir les valeurs prédites dans des intervalles
PREDICTED_VOLATILITY = Histogram(
    "volatichainxplorerai_predicted_volatility",
    "Distribution des valeurs de volatilité prédites.",
    ["horizon"],
    buckets=(
        0.1,
        0.25,
        0.5,
        1.0,
        2.5,
        5.0,
        10.0,
        20.0,
        30.0,
        60.0,
    )    
)

# Mesurer l’ancienneté des données utilisées
INPUT_DATA_AGE_DAYS = Gauge(
    "volatichainxplorerai_input_data_age_days",
    "Ancienneté des données utilisées pour la prédiction en jours.",
    ["horizon"]
)

