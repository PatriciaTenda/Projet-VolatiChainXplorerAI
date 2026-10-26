# Charger les librairies nécessaires
import sys
from datetime import date
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from setup.logger_config import setup_logger

# Chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Initialisation du logger
name_module = Path(__file__).stem
logger = setup_logger(name_module)


class VolatilityPredictionRequest(BaseModel):
    """Variable nécessaire à la prédiction de la volatilité du bitcoin à 7 et 30 jours"""
    
    model_config = ConfigDict(
        extra="forbid",
        allowed_inf_nan=False
    )
    
    # Variables macroéconomiques et financières nécessaires à la prédiction
    log_return: float = Field(description="Rendement logarithmique journalier")
    volatility_3d: float= Field(description="Volatilité glissante à 3 jours")
    volatility_7d: float= Field(description="Volatilité glissante à 7 jours")
    volatility_14d: float= Field(description="Volatilité glissante à 14 jours")
    volatility_30d: float= Field(description="Volatilité glissante à 30 jours")
    daily_range: float= Field(description="Amplitude quotidienne")
    volume_change: float= Field(description="Variation du volume")
    market_cap_change: float= Field(description="Variation de la capitalisation boursière")
    rate_mro: float= Field(description="Taux directeur de la BCE MRO")
    inflation_rate: float= Field(description="Taux d'inflation")
    unemployment_rate: float= Field(description="Taux de chômage")
    monetary_m3_rate: float= Field(description="Variationde la masse monétaire M3")
    log_return_lag_1d: float= Field(description="Rendement logarithmique décalé d'un jour")
    log_return_lag_7d: float= Field(description="Rendement logarithmique décalé de 7 jours")
    log_return_lag_30d: float= Field(description="Rendement logarithmique décalé de 30 jours")
    
    
    
class VolatilityPredictionResponse(BaseModel):
    """Variables nécessaires des réponses de la prédiction de la volatilité du bitcoin à 7 et 30 jours"""

    model_config = ConfigDict(
        extra="forbid",
        allowed_inf_nan=False
    )

    horizon_days: int = Field(description="Horizon de prédiction en jours")
    target: str = Field(description="Variable cible de la prédiction")
    predicted_volatility: float = Field(description="Volatilité prédite à l'horizon spécifié")
    predicted_volatility_percent: float = Field(description="Volatilité prédite en pourcentage à l'horizon spécifié")
    model_name: str = Field(description="Nom du modèle utilisé pour la prédiction")
    data_date: date | None = Field(description="Date des données utilisées pour la prédiction")
    