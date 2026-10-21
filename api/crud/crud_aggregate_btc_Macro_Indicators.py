import os  # noqa: N999
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from datetime import date

from sqlalchemy import text
from sqlalchemy.orm import Session

from setup.logger_config import setup_logger

# Mise en place d'un logger pour le module
name_file = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(name_file)


def get_bitcoin_macro_indicators_range(db: Session, start_date: date, end_date: date):
    """
    Récupère les données agrégées Bitcoin + indicateurs macro pour une plage de dates.

    Paramètres :
        db (Session) : Session SQLAlchemy.
        start_date (date) : Date de début de la plage.
        end_date (date) : Date de fin de la plage.

    Retourne :
        list[Row] : Liste des lignes récupérées depuis la vue.
    """
    try:
        query = text("""
                SELECT
                    day,
                    open,
                    high,
                    low,
                    close AS close_price,
                    volume,
                    market_cap,
                    rate_mro,
                    inflation_rate,
                    unemployment_rate,
                    monetary_m3_rate
                FROM public.v_bitcoin_macro_indicator_daily
                WHERE day BETWEEN :start_date AND :end_date
                ORDER BY day ASC
        """)
        
        result = db.execute(query, {"start_date": start_date, "end_date": end_date})
        data = result.fetchall()
        logger.info(f"{len(data)} lignes récupérées de v_btc_macro_daily entre {start_date} et {end_date}.")
        return data
    except Exception as e:
        logger.exception("Erreur lors de la requête BTC + Macro")
        raise RuntimeError(str(e)) from e
