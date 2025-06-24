# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from pydantic import BaseModel
from datetime import date
from typing import Optional

class BitcoinMacroIndicatorsResponse(BaseModel):
    """
    Schéma de réponse combinant les données Bitcoin et les indicateurs macroéconomiques.

    Attributs :
        day (date) : Date d'observation.
        close_price_bitcoin (float | None) : Prix de clôture du Bitcoin.
        rate_mro (float | None) : Taux directeur MRO.
        inflation_rate (float | None) : Taux d'inflation.
        unemployment_rate (float | None) : Taux de chômage.
        monetary_m3_rate (float | None) : Taux de variation de la masse monétaire M3.
    """
    day: date
    close_price_bitcoin: Optional[float]
    rate_mro: Optional[float]
    inflation_rate: Optional[float]
    unemployment_rate: Optional[float]
    monetary_m3_rate: Optional[float]

    class Config:
        from_attribute = True   # Permet à Pydantic de lire les données directement à partir d'un objet ORM 
                                # afin qu'on ait pas besoin de tout convertir à la main(dict ou autre)
