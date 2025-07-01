# Charger les librairies nécessaires
import os
import sys

# Ajoute le répertoire parent au chemin du système pour les imports relatifs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy.orm import Session
from database.postgres.models.bitcoin_prices import BitcoinPrices
from api.exceptions.bitcoin_prices_exceptions import BitcoinPricesNotFound, ValidationError
from database.conn_db.connect_postgresql import get_db  # Importe get_db si utilisé ailleurs
from setup.logger_config import setup_logger
from datetime import date # Importe date pour le typage des dates

# Mise en place d'un logger pour le module
name_file = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(name_file)

def get_all_bitcoin_prices(db: Session, skip: int = 0, limit: int = 10):
    """
    Récupère les enregistrements des prix du Bitcoin depuis la base PostgreSQL,
    triés par date décroissante, avec prise en charge de la pagination.

    Cette requête SQL est équivalente à la logique implémentée :

        SELECT date_bitcoin, open_price_bitcoin, close_price_bitcoin
        FROM t_bitcoin_prices
        ORDER BY date_bitcoin DESC
        LIMIT {limit} OFFSET {skip};

    Paramètres :
        db (Session) : Session SQLAlchemy active.
        skip (int) : Nombre de lignes à ignorer (début de pagination). Doit être >= 0.
        limit (int) : Nombre maximal de résultats à retourner. Doit être > 0.

    Retourne :
        list[BitcoinPrices] : Liste des objets BitcoinPrices correspondant aux critères spécifiés.

    Lève :
        ValidationError : Si 'skip' est négatif ou 'limit' est non positif.
        BitcoinPricesNotFound : Si aucun prix n'est trouvé pour les critères donnés.
    """
    # Validation des paramètres d'entrée
    if skip < 0:
        logger.error(f"Erreur de validation : 'skip' doit être un nombre positif ou nul, reçu {skip}.")
        raise ValidationError(detail=f"'skip' doit être un nombre positif ou nul, reçu {skip}.")
    if limit <= 0:
        logger.error(f"Erreur de validation : 'limit' doit être un nombre positif, reçu {limit}.")
        raise ValidationError(detail=f"'limit' doit être un nombre positif, reçu {limit}.")

    try:
        # Requête de récupération des cours du bitcoin
        prices = db.query(BitcoinPrices).order_by(BitcoinPrices.date_bitcoin.desc()).offset(skip).limit(limit).all()

        if not prices:
            logger.warning(f"Aucun prix Bitcoin trouvé pour skip={skip}, limit={limit}.")
            raise BitcoinPricesNotFound(skip=skip, limit=limit)
        
        logger.info(f"Récupération de {len(prices)} prix Bitcoin (skip={skip}, limit={limit}).")
        return prices
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des prix Bitcoin : {e}", exc_info=True)
        # Rélancer l'exception ou lever une exception plus générique si nécessaire
        raise

def get_bitcoin_prices_by_date_range(db: Session, start_date: date, end_date : date):
    """
    Récupère les prix du Bitcoin pour une plage de date.

    Cette requête SQL est équivalente à la logique implémentée :
        select * from t_bitcoin_prices 
        where date (date_bitcoin) 
        between start_date and end_date;

    Paramètres :
        db (Session) : Session SQLAlchemy active.
        start_date (date) : Date de début de la plage.
        end_date (date) : Date de fin de la plage.


    Retourne :
        BitcoinPrices | None : L'objet BitcoinPrices est une liste de prix du bitcoin correspondant à la plage dedate, ou None si non trouvé.

    Lève :
        ValidationError : Si les dates start_date et end_date  ne sont pas des objets dates valides.
    """
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        logger.error(f"Erreur de validation :'start_date et end_date ' doit être des objets date, reçu {type(start_date).__name__}, {type(end_date).__name__}.")
        raise ValidationError(detail=f"'start_date' ou 'end_date' est invalide.")

    try:
        prices = db.query(BitcoinPrices).filter(BitcoinPrices.date_bitcoin.between(start_date, end_date)).order_by(BitcoinPrices.date_bitcoin.asc()).all()
        if prices:
            logger.info(f"{len(prices)} prix Bitcoin trouvés du {start_date} au {end_date}.")
        else:
            logger.warning(f"Aucun prix Bitcoin trouvés sur la plage de date {start_date} à {end_date}.")
        return prices
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du prix Bitcoin sur la plage de date {start_date} à {end_date}. : {e}", exc_info=True)
        raise

