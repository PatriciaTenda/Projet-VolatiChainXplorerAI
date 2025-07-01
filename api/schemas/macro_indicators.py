# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# --- MRO ---
class MroResponse(BaseModel):
    """
    Schéma de données utilisé pour restituer les taux des opérations principales de refinancement (MRO).

    Attributs :
        id_mro (int) : Identifiant de l'enregistrement.
        date_mro (date) : Date de publication du taux MRO.
        rate_mro (float | None) : Taux d'intérêt MRO.
        time_periode_mro (str | None) : Période de référence (ex : 'Mensuel', 'Trimestriel').
        indicator_name_mro (str | None) : Nom de l'indicateur (ex : 'Main Refinancing Operations').
        source_label_mro (str | None) : Source de la donnée (ex : 'BCE').
    """
    id_mro: int
    date_mro: date
    rate_mro: Optional[float]
    time_periode_mro: Optional[str]
    indicator_name_mro: Optional[str]
    source_label_mro: Optional[str]

    class Config:
        from_attribute = True

# --- INFLATION ---
class InflationResponse(BaseModel):
    """
    Schéma de données utilisé pour restituer les taux d'inflation publiés par la BCE.

    Attributs :
        id_inflation (int) : Identifiant de l'enregistrement.
        date_inflation (date) : Date de publication du taux d'inflation.
        inflation_rate (float | None) : Taux d'inflation (en pourcentage).
        time_periode_inflation (str | None) : Période de référence (ex : 'Mensuel').
        indicator_name_inflation (str | None) : Nom de l'indicateur.
        source_label_inflation (str | None) : Source de la donnée (ex : 'BCE').
    """
    id_inflation: int
    date_inflation: date
    inflation_rate: Optional[float]
    time_periode_inflation: Optional[str]
    indicator_name_inflation: Optional[str]
    source_label_inflation: Optional[str]

    class Config:
        from_attributes = True # Permet à Pydantic de lire les données directement à partir d'un objet ORM 
                               # afin qu'on ait pas besoin de tout convertir à la main(dict ou autre)

# --- TAUX DE CHÔMAGE ---
class UnemploymentResponse(BaseModel):
    """
    Schéma de données utilisé pour restituer les taux de chômage.

    Attributs :
        id_unemployment (int) : Identifiant de l'enregistrement.
        date_unemployment (date) : Date de publication du taux de chômage.
        unemployment_rate (float | None) : Taux de chômage (en pourcentage).
        indicator_name_unemployment (str | None) : Nom de l'indicateur.
        source_label_unemployment (str | None) : Source de la donnée (ex : 'BCE').
    """
    id_unemployment: int
    date_unemployment: date
    unemployment_rate: Optional[float]
    indicator_name_unemployment: Optional[str]
    source_label_unemployment: Optional[str]

    class Config:
        from_attributes = True # Permet à Pydantic de lire les données directement à partir d'un objet ORM 
                        # afin qu'on ait pas besoin de tout convertir à la main(dict ou autre)

# --- MASSE MONÉTAIRE M3 ---
class MonetaryM3Response(BaseModel):
    """
    Schéma de données utilisé pour restituer les taux de variation de la masse monétaire M3.

    Attributs :
        id_monetary_m3 (int) : Identifiant de l'enregistrement.
        date_monetary_m3 (date) : Date de publication de l'indicateur.
        monetary_m3_rate (float | None) : Taux de variation annuel de M3.
        indicator_name_m3 (str | None) : Nom de l'indicateur.
        source_label_m3 (str | None) : Source de la donnée (ex : 'BCE').
    """
    id_monetary_m3: int
    date_monetary_m3: date
    monetary_m3_rate: Optional[float]
    indicator_name_m3: Optional[str]
    source_label_m3: Optional[str]

    class Config:
        from_attributes = True # Permet à Pydantic de lire les données directement à partir d'un objet ORM 
                        # afin qu'on ait pas besoin de tout convertir à la main(dict ou autre)
                        
# --- INDICATEUR MACROECONOMIQUE ---
class MacroIndicatorsResponse(BaseModel):
    """
    Schéma de réponse regroupant les principaux indicateurs macroéconomiques agrégés par jour.

    Attributs :
        day (date) : Date d'observation.
        rate_mro (float | None) : Taux des opérations principales de refinancement (MRO).
        inflation_rate (float | None) : Taux d'inflation.
        unemployment_rate (float | None) : Taux de chômage.
        monetary_m3_rate (float | None) : Taux de variation de la masse monétaire M3.
    """

    day: date
    rate_mro: Optional[float]
    inflation_rate: Optional[float]
    unemployment_rate: Optional[float]
    monetary_m3_rate: Optional[float]

    class Config:
        from_attributes = True  # Permet à Pydantic de lire les données directement à partir d'un objet ORM 
                         # afin qu'on ait pas besoin de tout convertir à la main(dict ou autre)