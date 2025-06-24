# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date

from database.postgres.models.macro_indicators import MacroBceMRO, MacroBceInflation, MacroBcetauxChomage, MacroBceMonetaryM3
from api.exceptions.macro_indicators_exceptions import MacroIndicatorsNotFound, ValidationError, DatabaseError
from setup.logger_config import setup_logger

# Initialisation du logger
name_file = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(name_file)


# ----------- MRO -----------

def get_mro_rates_by_date_range(db: Session, start_date: date, end_date: date):
    """
    Récupère les taux MRO entre deux dates données.

    Args:
        db (Session): Session SQLAlchemy active.
        start_date (date): Date de début.
        end_date (date): Date de fin.

    Returns:
        list[MacroBceMRO]: Liste des taux MRO dans la plage de dates.

    Raises:
        ValidationError: Si les dates ne sont pas valides.
    """
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        logger.error(f"start_date et end_date doivent être de type date.")
        raise ValidationError(message="'start_date' ou 'end_date' est invalide.")

    try:
        mro_rate = db.query(MacroBceMRO).filter(MacroBceMRO.date_mro.between(start_date, end_date)).order_by(MacroBceMRO.date_mro.asc()).all()
        if mro_rate:
            logger.info(f"{len(mro_rate)} taux MRO trouvés du {start_date} au {end_date}.")
        else:
            logger.warning(f"Aucun taux MRO trouvé entre {start_date} et {end_date}.")
        return mro_rate
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des taux MRO : {e}", exc_info=True)
        raise DatabaseError(operation="get_mro_rates_by_date_range")


# ----------- INFLATION -----------

def get_all_inflation_rates(db: Session, skip: int, limit: int):
    """
    Récupère les taux d'inflation avec pagination.

    Args:
        db (Session): Session SQLAlchemy.
        skip (int): Nombre de lignes à ignorer.
        limit (int): Nombre maximum de lignes à retourner.

    Returns:
        list[MacroBceInflation]

    Raises:
        ValidationError: Si skip ou limit sont invalides.
        MacroIndicatorsNotFound: Si aucun enregistrement trouvé.
    """
    if skip < 0 or limit <= 0:
        raise ValidationError(message=f"'skip' ou 'limit' invalide (skip={skip}, limit={limit})")

    try:
        inflation_rate = db.query(MacroBceInflation).order_by(MacroBceInflation.date_inflation.desc()).offset(skip).limit(limit).all()

        if not inflation_rate:
            logger.warning(f"Aucun taux d'inflation trouvé (skip={skip}, limit={limit})")
            raise MacroIndicatorsNotFound(skip=skip, limit=limit)

        logger.info(f"{len(inflation_rate)} taux d'inflation récupérés.")
        return inflation_rate

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des taux d'inflation : {e}", exc_info=True)
        raise DatabaseError(operation="get_all_inflation_rates")


# ----------- CHÔMAGE -----------

def get_all_unemployment_rates(db: Session, skip: int, limit: int):
    """
    Récupère les taux de chômage avec pagination.

    Args:
        db (Session): Session SQLAlchemy.
        skip (int): Nombre de lignes à ignorer.
        limit (int): Nombre de lignes à récupérer.

    Returns:
        list[MacroBcetauxChomage]

    Raises:
        ValidationError: Paramètres invalides.
        MacroIndicatorsNotFound: Si aucun résultat trouvé.
    """
    if skip < 0 or limit <= 0:
        raise ValidationError(message=f"'skip' ou 'limit' invalide (skip={skip}, limit={limit})")

    try:
        unemployment_rate = db.query(MacroBcetauxChomage).order_by(MacroBcetauxChomage.date_unemployment.desc()).offset(skip).limit(limit).all()

        if not unemployment_rate:
            logger.warning(f"Aucun taux de chômage trouvé (skip={skip}, limit={limit})")
            raise MacroIndicatorsNotFound(skip=skip, limit=limit)

        return unemployment_rate

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des taux de chômage : {e}", exc_info=True)
        raise DatabaseError(operation="get_all_unemployment_rates")


# ----------- MASSE MONÉTAIRE M3 -----------

def get_all_monetary_m3_rates(db: Session, skip: int, limit: int):
    """
    Récupère les taux de variation de la masse monétaire M3 avec pagination.

    Args:
        db (Session): Session SQLAlchemy.
        skip (int): Nombre de lignes à ignorer.
        limit (int): Nombre de lignes à récupérer.

    Returns:
        list[MacroBceMonetaryM3]

    Raises:
        ValidationError: Paramètres invalides.
        MacroIndicatorsNotFound: Si aucun résultat trouvé.
    """
    if skip < 0 or limit <= 0:
        raise ValidationError(message=f"'skip' ou 'limit' invalide (skip={skip}, limit={limit})")

    try:
        m3_rate = db.query(MacroBceMonetaryM3).order_by(MacroBceMonetaryM3.date_monetary_m3.desc()).offset(skip).limit(limit).all()

        if not m3_rate:
            logger.warning(f"Aucun taux M3 trouvé (skip={skip}, limit={limit})")
            raise MacroIndicatorsNotFound(skip=skip, limit=limit)

        return m3_rate

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des taux M3 : {e}", exc_info=True)
        raise DatabaseError(operation="get_all_monetary_m3_rates")


# ----------- AGRÉGÉ GLOBAL (depuis la vue) -----------

def get_macro_indicators_daily(db: Session, start_date: date, end_date: date):
    """
    Récupère les indicateurs macroéconomiques journaliers
    depuis la vue v_macro_indicators_daily_v1.

    Args:
        db (Session): Session SQLAlchemy.
        start_date (date): Date de début.
        end_date (date): Date de fin.

    Returns:
        list[Row]: Résultats agrégés par jour.

    Raises:
        RuntimeError: En cas d’erreur de requête.
    """
    try:
        query = text("""
            SELECT *
            FROM v_macro_indicators_daily_v1
            WHERE day BETWEEN :start_date AND :end_date
            ORDER BY day ASC
        """)
        result = db.execute(query, {"start_date": start_date, "end_date": end_date})
        logger.info(f"Indicateurs macro récupérés de {start_date} à {end_date}.")
        return result.fetchall()
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des indicateurs journaliers : {e}", exc_info=True)
        raise RuntimeError(f"Erreur lors de la récupération des indicateurs macroéconomiques : {e}")
