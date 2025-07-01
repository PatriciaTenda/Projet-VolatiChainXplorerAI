"""
    Module : api/schemas/correlated_btc_rates_articlesFi.py
    Date : 2025-06-28
    Description :
        Ce module définit les schémas Pydantic utilisés pour la restitution des données croisées entre les cours du Bitcoin, les indicateurs macroéconomiques et les articles financiers.
        Il est utilisé dans l'API pour valider et structurer les données renvoyées par les endpoints.
"""

# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from api.schemas.aggregate_btc_Macro_Indicators import BitcoinMacroIndicatorsResponse

class BtcIndicatorsArticlesResponse(BaseModel):
    day: date  
    close_price_bitcoin: Optional[float]
    rate_mro: Optional[float]
    inflation_rate: Optional[float]
    unemployment_rate: Optional[float]
    monetary_m3_rate: Optional[float]
   
    class Config:
            from_attributes = True


class CorrelatedResponse(BaseModel):
    article_count: int
    results: List[BtcIndicatorsArticlesResponse]