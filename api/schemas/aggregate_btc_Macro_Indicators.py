# Charger les librairies nécessaires  # noqa: N999
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from datetime import date

from pydantic import BaseModel


class BitcoinMacroIndicatorsResponse(BaseModel):
    """
    Schéma de réponse combinant les données Bitcoin et les indicateurs macroéconomiques.

    Attributs :
        day (date) : Date d'observation.
        close_price (float | None) : Prix de clôture du Bitcoin.
        rate_mro (float | None) : Taux directeur MRO.
        inflation_rate (float | None) : Taux d'inflation.
        unemployment_rate (float | None) : Taux de chômage.
        monetary_m3_rate (float | None) : Taux de variation de la masse monétaire M3.
    """
    day: date
    close_price: float | None
    rate_mro: float | None
    inflation_rate: float | None
    unemployment_rate: float | None
    monetary_m3_rate: float | None

    class Config:
        from_attributes = True   # Permet à Pydantic de lire les données directement à partir d'un objet ORM 
                                # afin qu'on n'ait pas besoin de tout convertir à la main(dict ou autre)
