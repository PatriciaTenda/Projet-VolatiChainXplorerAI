"""
    Module : api/schemas/correlated_btc_rates_articlesFi.py
    Date : 2025-06-28
    Description :
        Ce module définit les schémas Pydantic utilisés pour la restitution des données croisées entre les cours du Bitcoin, les indicateurs macroéconomiques et les articles financiers.
        Il est utilisé dans l'API pour valider et structurer les données renvoyées par les endpoints.
"""  # noqa: N999

# Charger les librairies nécessaires
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from datetime import date

from pydantic import BaseModel, ConfigDict;


class BtcIndicatorsArticlesResponse(BaseModel):
    day: date  
    close_price: float | None
    rate_mro: float | None
    inflation_rate: float | None
    unemployment_rate: float | None
    monetary_m3_rate: float | None
   
    model_config = ConfigDict(from_attributes=True)


class CorrelatedResponse(BaseModel):
    article_count: int
    results: list[BtcIndicatorsArticlesResponse]

    model_config = ConfigDict(from_attributes=True)