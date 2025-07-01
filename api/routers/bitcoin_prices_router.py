# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.conn_db.connect_postgresql import get_db  # fonction qui donne une session DB PostgreSQL
from api.crud.crud_bitcoin_prices import get_all_bitcoin_prices, get_bitcoin_prices_by_date_range # fonction de récupération des prix depuis le CRUD
from api.schemas.bitcoin_prices import BitcoinPriceResponse # schéma de sortie Pydantic
from typing import List
from setup.logger_config import setup_logger
from api.exceptions.bitcoin_prices_exceptions import BitcoinPricesNotFound, ValidationError
from datetime import date

# Mise en place d'un logger pour le module de création des collections
name_file =os.path.splitext(os.path.basename(__file__))[0]
# set le logger du module en cours
logger = setup_logger(name_file)

# Création d’un routeur dédié aux routes relatives au Bitcoin
router = APIRouter(
    prefix="/api/v1/bitcoin-prices", # Préfixe commun pour toutes les routes 
    tags=["Bitcoin Prices"]    # Étiquette utilisée dans la documentation Swagger
)

# ----------- Liste des prix du bitcoins avec pagination -------------------------

@router.get("/", response_model=List[BitcoinPriceResponse])
def read_bitcoin_prices(skip: int = Query(0, ge=0, description="Nombre d'enregistrements à ignorer pour la pagination (par défaut 0)"),     # Nombre de lignes à ignorer (offset) c'est à dire que skip doit être ≥ 0
                        limit: int = Query(10, gt=0, le=100, description="Nombre maximum d'enregistrements à retourner (entre 1 et 100, par défaut 10)"), # Nombre maximum de résultats à retourner c'est à dire que limit doit être ≤ 100
                        db: Session = Depends(get_db)   # Injection de la session de base de données
):

    """
    Récupère les prix du Bitcoin avec pagination (offset + limit).

    - **skip**: nombre de lignes ignorées depuis le début (début à 0)
    - **limit**: nombre maximum de lignes à afficher (par page)

    Requête SQL équivalente :
    ```sql
    SELECT date_bitcoin, open_price_bitcoin, close_price_bitcoin
    FROM t_bitcoin_prices
    ORDER BY date_bitcoin DESC
    OFFSET {skip}
    LIMIT {limit};
    ```

    Retourne une liste de résultats sous forme de schéma `BitcoinPriceResponse`.
    """
    print(type(db)) 
    try:
        # Appel à la fonction CRUD pour récupérer les données
        prices = get_all_bitcoin_prices(db, skip=skip, limit=limit)

        # Log du nombre de résultats récupérés
        logger.info(f"{len(prices)} résultats récupérés (skip={skip}, limit={limit})")
        return prices
    except BitcoinPricesNotFound as e:
            logger.warning(str(e))
            raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur inattendue dans read_bitcoin_prices : {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur serveur inattendue")


#---------------------Liste des prix du bitcoin sur une plage de date-----------------------------------

@router.get("/by-date-range", response_model=List[BitcoinPriceResponse])
def get_bitcoin_prices_range(
    start_date: date = Query(..., description="Date de début au format YYYY-MM-DD"),
    end_date: date = Query(..., description="Date de fin au format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """
    Récupère les prix du Bitcoin pour une plage de dates (inclusives).
    
    Exemple :
    - /by-date-range?start_date=2021-01-01&end_date=2021-01-31
    """
    try:
        if start_date > end_date:
            raise HTTPException(
                status_code=400,
                detail=f"La date de début {start_date} ne peut pas être postérieure à la date de fin {end_date}."
            )

        prices = get_bitcoin_prices_by_date_range(db, start_date=start_date, end_date=end_date)

        if not prices:
            logger.warning(f"Aucun prix Bitcoin trouvé entre {start_date} et {end_date}.")
            raise HTTPException(status_code=404, detail="Aucun prix Bitcoin trouvé pour la plage de dates spécifiée.")

        return prices

    except ValidationError as e:
        logger.error(f"Erreur de validation dans la route /by-date-range : {e}", exc_info=True)
        raise HTTPException(status_code=422, detail=str(e.detail))

    except Exception as e:
        logger.error(f"Erreur inattendue dans la route /by-date-range : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur serveur inattendue")
