# Charger les librairies nécessaires
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))
from datetime import date

from pydantic import BaseModel

# Modèle Pydantic pour la réponse de l'API (ce qui sera renvoyé en JSON)
# C'est la représentation de votre TBitcoinPrice en JSON

class BitcoinPriceResponse(BaseModel):
    """
    Schéma de données utilisé pour restituer un enregistrement historique des prix du Bitcoin.

    Attributs :
        id_price (int) : Identifiant de l'enregistrement.
        date (date) : Date du prix enregistré.
        open_price (float) : Prix d'ouverture.
        close_price (float) : Prix de clôture.
        high_price (float | None) : Prix le plus haut.
        low_price (float | None) : Prix le plus bas.
        volume (float | None) : Volume échangé.
        market_cap (float | None) : Capitalisation boursière du Bitcoin.
    """
    id_price: int
    date: date # Type Python pour DATE    
    open_price: float
    close_price: float
    high_price: float | None
    low_price: float | None
    volume: float | None
    market_cap: float | None

    class Config:
        from_attributes = True # Permet à Pydantic de lire les données directement à partir d'un objet ORM 
                        # afin qu'on ait pas besoin de tout convertir à la main(dict ou autre)