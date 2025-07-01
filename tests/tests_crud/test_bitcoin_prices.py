# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from sqlalchemy.orm import Session
from database.conn_db.connect_postgresql import SessionLocal
from api.crud.crud_bitcoin_prices import get_all_bitcoin_prices, get_bitcoin_prices_by_date_range
from datetime import date
from setup.logger_config import setup_logger
import time 

# Mise en place d'un logger pour le module de création des collections
name_file =os.path.splitext(os.path.basename(__file__))[0]
# set le logger du module en cours
logger = setup_logger(name_file)

# Fonction de test de la fonction get_all_bitcoin_prices
def test_get_all_bitcoin_prices(skip: int=0, limit: int=5):
    # Connexion à l base de données
    db: Session = SessionLocal()

    # Bornes de la paginations
    try:
        # Délimitation du temps de début et de fin de chrono pour avoie le temps de récupération
        start = time.time()  # Début chrono

        prices = get_all_bitcoin_prices(db, skip= skip, limit=limit)
        logger.info(f"Page affichée : skip = {skip}, limit = {limit} → {len(prices)} résultats")

        end = time.time()  # Fin chrono
        logger.info(f"Temps de récupération : {end - start:.3f} secondes — Prix du Bitcoin récupérés : {len(prices)}")


        if prices:
            first = prices[0]
            logger.info(f"Dernier prix : {first.close_price_bitcoin} € le {first.date_bitcoin}")

            # Calcul du numéro de page
            page_number = (skip // limit) + 1
            logger.info(f"=== Page {page_number} ===")

            # Afficher les premiers pour vérif visuelle
            for i, p in enumerate(prices, start=skip+1):
                logger.info(f"{i}. {p.date_bitcoin} | Open = {p.open_price_bitcoin:.2f} €, Close = {p.close_price_bitcoin:.2f} €")
        else:
            logger.warning("Aucun prix trouvé.")
    except Exception as e:
        logger.error(f"Une erreur est survenue : {str(e)}")
        raise
    finally:
        db.close()

def test_get_prices_by_date_range(start_date: date, end_date: date):
    db: Session = SessionLocal()
    try:
        prices = get_bitcoin_prices_by_date_range(db, start_date, end_date)
        if prices:
            logger.info(f"Récupération des prix du {start_date} au {end_date} :")
            for p in prices:
                logger.info(f"- {p.date_bitcoin} | Open: {p.open_price_bitcoin} € | Close: {p.close_price_bitcoin} €")

        else:
            logger.info(f"Aucun prix trouvé pour la plage de date {start_date} au {end_date}")
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des prix du {start_date} au {end_date} : {str(e)}", exc_info=True)
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_get_all_bitcoin_prices(skip=0, limit=5)
    test_get_all_bitcoin_prices(skip=5, limit=5)
    test_get_all_bitcoin_prices(skip=10, limit=5)
    print("-------------SEPARATION----------------------")
    test_get_prices_by_date_range(date(2010,7,14), date(2011, 7, 14))
