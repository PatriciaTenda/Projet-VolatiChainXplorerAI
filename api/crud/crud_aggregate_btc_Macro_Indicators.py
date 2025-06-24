import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date
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
            SELECT *
            FROM v_bitcoin_macro_indicator_daily
            WHERE day BETWEEN :start_date AND :end_date
            ORDER BY day ASC
        """)
        result = db.execute(query, {"start_date": start_date, "end_date": end_date})
        data = result.fetchall()
        logger.info(f"{len(data)} lignes récupérées de v_btc_macro_daily entre {start_date} et {end_date}.")
        return data
    except Exception as e:
        logger.error(f"Erreur lors de la requête BTC + Macro : {e}", exc_info=True)
        raise RuntimeError("Erreur lors de la récupération des données agrégées.")
