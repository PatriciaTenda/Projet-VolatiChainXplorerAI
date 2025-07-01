# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))
 
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


# Modèle Pydantic pour la réponse de l'API (ce qui sera renvoyé en JSON)
# C'est la représentation de votre TBitcoinPrice en JSON

class BitcoinPriceResponse(BaseModel):
    """
    Schéma de données utilisé pour restituer un enregistrement historique des prix du Bitcoin.

    Attributs :
        id_price_bitcoin (int) : Identifiant de l'enregistrement.
        date_bitcoin (date) : Date du prix enregistré.
        time_open_bitcoin (datetime | None) : Heure d'ouverture du marché.
        time_close_bitcoin (datetime | None) : Heure de fermeture du marché.
        time_high_bitcoin (datetime | None) : Heure du prix le plus haut.
        time_low_bitcoin (datetime | None) : Heure du prix le plus bas.
        open_price_bitcoin (float) : Prix d'ouverture.
        close_price_bitcoin (float) : Prix de clôture.
        high_price_bitcoin (float | None) : Prix le plus haut.
        low_price_bitcoin (float | None) : Prix le plus bas.
        volume_bitcoin (float | None) : Volume échangé.
        market_Cap_bitcoin (float | None) : Capitalisation boursière du Bitcoin.
    """
    id_price_bitcoin: int
    date_bitcoin: date # Type Python pour DATE
    time_open_bitcoin: Optional[datetime]# Type Python pour TIMESTAMP WITHOUT TIME ZONE
    time_close_bitcoin: Optional[datetime]
    time_high_bitcoin: Optional[datetime]
    time_low_bitcoin: Optional[datetime]
    open_price_bitcoin: float
    close_price_bitcoin: float
    high_price_bitcoin: Optional[float]
    low_price_bitcoin: Optional[float]
    volume_bitcoin: Optional[float]
    market_Cap_bitcoin: Optional[float]

    class Config:
        from_attributes = True # Permet à Pydantic de lire les données directement à partir d'un objet ORM 
                        # afin qu'on ait pas besoin de tout convertir à la main(dict ou autre)