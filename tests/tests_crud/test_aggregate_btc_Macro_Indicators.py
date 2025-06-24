# --- Imports nécessaires ---
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy.orm import Session
from database.conn_db.connect_postgresql import SessionLocal
from database.postgres.models.bitcoin_prices import BitcoinPrices
from database.postgres.models.macro_indicators import MacroIndicatorsDaily
from api.crud.crud_aggregate_btc_Macro_Indicators import get_bitcoin_macro_indicators_range
from setup.logger_config import setup_logger
from datetime import date

# Logger spécifique au module de test 
name_file = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(name_file)


# Fonction de test 
def test_get_bitcoin_macro_indicators(start_date: date, end_date: date):
    """
    Test de récupération des données combinées Bitcoin + indicateurs macroéconomiques
    depuis la vue v_bitcoin_macro_indicator_daily pour une plage de dates donnée.
    """
    db: Session = SessionLocal()
    try:
        logger.info(f"Test de récupération des données BITCOIN + Indicateurs macro entre {start_date} et {end_date}")
        records = get_bitcoin_macro_indicators_range(db, start_date, end_date)

        if not records:
            logger.warning(f"Aucune donnée trouvée entre {start_date} et {end_date}")
        else:
            logger.info(f"{len(records)} enregistrements récupérés.")

            # Affichage des premiers résultats pour vérification
            for i, r in enumerate(records[:5], start=1):
                logger.info(
                    f"{i}. Date: {r.day}, BITCOIN: close={r.close_price_bitcoin} | "
                    f"MRO={r.rate_mro}, Inflation={r.inflation_rate}, Chômage={r.unemployment_rate}, M3={r.monetary_m3_rate}"
                )
    except Exception as e:
        logger.error(f"Erreur lors du test : {e}", exc_info=True)
        raise
    finally:
        db.close()
        logger.info("Fin du test de récupération BTC + macro.")

#  Exécution 
if __name__ == "__main__":
    test_get_bitcoin_macro_indicators(start_date=date(2022, 1, 1), end_date=date(2022, 12, 31))
