# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from sqlalchemy.orm import Session
from database.conn_db.connect_postgresql import SessionLocal
from api.crud.crud_macro_indicators import get_macro_indicators_daily, get_mro_rates_by_date_range, get_all_inflation_rates, get_all_unemployment_rates, get_all_monetary_m3_rates
import time
from setup.logger_config import setup_logger
from datetime import date

# Mise en place d'un logger pour le module de création des collections
name_file =os.path.splitext(os.path.basename(__file__))[0]
# set le logger du module en cours
logger = setup_logger(name_file)

#---------------TEST TAUX DIRECTEUR MRO--------------------------
def test_get_mro(start_date : date, end_date: date):
    db: Session = SessionLocal()
    try:
        mro_rates = get_mro_rates_by_date_range(db, start_date, end_date)
        logger.info(f"Taux MRO récupérés : {len(mro_rates)} sur la plage du {start_date} au {end_date}")
        if mro_rates:
            for i, mro in enumerate(mro_rates, start=1):
                logger.info(f"{i}. {mro.date_mro} → Taux MRO : {mro.rate_mro}%")
    except Exception as e:
        logger.error(f"Une erreur est survenue : {str(e)}")
        raise
    finally:
        db.close()
        logger.info("Fin de l'exécution")

#---------------TEST TAUX D'INFLATION--------------------------

def test_get_inflation(skip,limit):
    db: Session = SessionLocal()
    try:
        # Délimitation du temps de début et de fin de chrono pour avoie le temps de récupération
        start = time.time()  # Début chrono
        inflation_rates = get_all_inflation_rates(db, skip= skip, limit=limit)
        logger.info(f"Page affichée : skip = {skip}, limit = {limit} → {len(inflation_rates)} résultats")

        end = time.time()  # Fin chrono
        logger.info(f"Temps de récupération : {end - start:.3f} secondes — Taux d'inflation récupérés : {len(inflation_rates)}")

        if inflation_rates:
            first = inflation_rates[0]
            logger.info(f"Dernier taux : {first.inflation_rate} € le {first.date_inflation}")

            # Calcul du numéro de page
            page_number = (skip // limit) + 1
            logger.info(f"=== Page {page_number} ===")

            # Afficher les premiers pour vérif visuelle
            for i, p in enumerate(inflation_rates, start=skip+1):
                logger.info(f"{i}. {p.date_inflation} | taux d'inflation = {p.inflation_rate}")
        else:
            logger.warning("Aucun taux trouvé.")
    except Exception as e:
        logger.error(f"Une erreur est survenue : {str(e)}")
        raise
    finally:
        db.close()

#---------------TEST TAUX DE VARIATION MASSE MONETAIRE --------------------------

def test_get_m3(skip:int=0, limit: int=5):
    db: Session = SessionLocal()
    try:
        # Délimitation du temps de début et de fin de chrono pour avoie le temps de récupération
        start = time.time()  # Début chrono
        m3_rates = get_all_monetary_m3_rates(db, skip= skip, limit=limit)
        logger.info(f"Page affichée : skip = {skip}, limit = {limit} → {len(m3_rates)} résultats")

        end = time.time()  # Fin chrono
        logger.info(f"Temps de récupération : {end - start:.3f} secondes — Taux de variation de la masse monétaire récupérés : {len(m3_rates)}")

        if m3_rates:
            first = m3_rates[0]
            logger.info(f"Dernier taux : {first.monetary_m3_rate} € le {first.date_monetary_m3}")

            # Calcul du numéro de page
            page_number = (skip // limit) + 1
            logger.info(f"=== Page {page_number} ===")

            # Afficher les premiers pour vérif visuelle
            for i, p in enumerate(m3_rates, start=skip+1):
                logger.info(f"{i}. {p.date_monetary_m3} | taux de m3 = {p.monetary_m3_rate}")
        else:
            logger.warning("Aucun taux trouvé.")
    except Exception as e:
        logger.error(f"Une erreur est survenue : {str(e)}")
        raise
    finally:
        db.close()

#---------------TEST TAUX DE CHOMAGE--------------------------

def test_get_unemployment(skip:int=0, limit : int=5):
    db: Session = SessionLocal()
    try:
        # Délimitation du temps de début et de fin de chrono pour avoie le temps de récupération
        start = time.time()  # Début chrono
        unemployment_rates = get_all_unemployment_rates(db, skip= skip, limit=limit)
        logger.info(f"Page affichée : skip = {skip}, limit = {limit} → {len(unemployment_rates)} résultats")

        end = time.time()  # Fin chrono
        logger.info(f"Temps de récupération : {end - start:.3f} secondes — Taux de chômage récupérés : {len(unemployment_rates)}")

        if unemployment_rates:
            first = unemployment_rates[0]
            logger.info(f"Dernier taux : {first.unemployment_rate} € le {first.date_unemployment}")

            # Calcul du numéro de page
            page_number = (skip // limit) + 1
            logger.info(f"=== Page {page_number} ===")

            # Afficher les premiers pour vérif visuelle
            for i, p in enumerate(unemployment_rates, start=skip+1):
                logger.info(f"{i}. {p.date_unemployment} | taux de chômage = {p.unemployment_rate}")
        else:
            logger.warning("Aucun taux trouvé.")
    except Exception as e:
        logger.error(f"Une erreur est survenue : {str(e)}")
        raise
    finally:
        db.close()

#---------------TEST AGGREGAT DES INDICATEURS MACROeCONOMIQUES --------------------------

def test_get_macro_indicators(start_date: date, end_date: date):
    db: Session = SessionLocal()
    try:
        start = time.time()
        indicators = get_macro_indicators_daily(db, start_date, end_date)
        end = time.time()

        logger.info(f"Récupération de {len(indicators)} jours d’indicateurs macro entre {start_date} et {end_date}")
        logger.info(f"Temps d'exécution : {end - start:.3f} secondes")
        for i, row in enumerate(indicators, start=1):
            logger.info(f"{i}. {row.day} | MRO={row.rate_mro} | Inflation={row.inflation_rate} | Chômage={row.unemployment_rate} | M3={row.monetary_m3_rate}")
    except Exception as e:
        logger.error(f"Erreur lors du test de la vue macro_indicators_daily : {e}", exc_info=True)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    test_get_mro(start_date=date(2020, 1, 1), end_date=date(2021, 1, 1))
    test_get_mro(date(2022, 6, 1), date(2023, 6, 1))

    """test_get_inflation(skip=0, limit=5)
    test_get_unemployment(skip=0, limit=5)
    test_get_m3(skip=0, limit=5)
    test_get_macro_indicators(start_date=date(2020, 1, 1), end_date=date(2021, 1, 1))
"""
