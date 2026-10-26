# Charger les librairies nécessaires
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from datetime import date

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.exceptions.macro_indicators_exceptions import (
    DatabaseError,
    MacroIndicatorsNotFound,
    ValidationError,
)
from database.postgres.models.macro_indicators import (
    MacroBceInflation,
    MacroBceMonetaryM3,
    MacroBcetauxChomage,
)
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

            status_code=400,
            detail="Les dates ne sont pas valides."
        )
    from fastapi import HTTPException
    Raises:
        ValidationError: Si les dates ne sont pas valides.
        HTTPException: Si les dates ne sont pas valides.
    """
    if start_date > end_date:
        raise ValidationError(
            message="'start_date' ne peut pas être postérieur à 'end_date'."
        )

    query = text("""
        SELECT
            date AS date_mro,
            rate_mro
        FROM public.v_macro_indicators_daily_v1
        WHERE date BETWEEN :start_date AND :end_date
        ORDER BY date ASC
    """)

    try:
        result = db.execute(
            query,
            {
                "start_date": start_date,
                "end_date": end_date,
            },
        )
        return result.mappings().all()

    except SQLAlchemyError as e:
        logger.exception("Erreur lors de la récupération du MRO quotidien")
        raise DatabaseError(
            operation="get_mro_rates_by_date_range"
        ) from e


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
    # 1. Vérifier les paramètres skip et limit
    if skip < 0 or limit <= 0:
        raise ValidationError(message=f"'skip' ou 'limit' invalide (skip={skip}, limit={limit})")
    
    # 2. Récupérer les taux d'inflation avec pagination
    try:
        inflation_rate = (
            db
            .query(MacroBceInflation)
            .order_by(
                MacroBceInflation
                .date_inflation
                .desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
       
    except SQLAlchemyError:
        logger.exception(
            "Erreur lors de la récupération des taux d'inflation"
        )
        raise DatabaseError(operation="get_all_inflation_rates")
    
       
    # 3. Logger le résultat et retourner les données
    if not inflation_rate:
        logger.warning(
            "Aucun taux d'inflation trouvé (skip=%s, limit=%s)",
            skip, limit
        )
        raise MacroIndicatorsNotFound(skip=skip, limit=limit)
    else:
        logger.info(
            "%d taux d'inflation récupérés.",
            len(inflation_rate)
        )
    return inflation_rate

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
    # 1. Valider les paramètres de pagination
    if skip < 0 or limit <= 0:
        raise ValidationError(message=f"'skip' ou 'limit' invalide (skip={skip}, limit={limit})")

    # 2. Récupérer les taux de chômage avec pagination
    try:
        unemployment_rate = (
            db
            .query(MacroBcetauxChomage)
            .order_by(MacroBcetauxChomage.date_unemployment.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    except SQLAlchemyError:
        logger.exception(
            "Erreur lors de la récupération des taux de chômage"
        )
        raise DatabaseError(operation="get_all_unemployment_rates")

    # 3. Logger le résultat et retourner les données
    if not unemployment_rate:
        logger.warning(
            "Aucun taux de chômage trouvé (skip=%s, limit=%s)",
            skip, limit
        )
        raise MacroIndicatorsNotFound(skip=skip, limit=limit)
    else:
        logger.info(
            "%d taux de chômage récupérés.",
            len(unemployment_rate)
        )
    return unemployment_rate


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
    # 1. Valider les paramètres de pagination
    if skip < 0 or limit <= 0:
        raise ValidationError(message=f"'skip' ou 'limit' invalide (skip={skip}, limit={limit})")

    # 2. Récupérer les taux M3 avec pagination
    try:
        m3_rate = (
            db
            .query(MacroBceMonetaryM3)
            .order_by(MacroBceMonetaryM3.date_monetary_m3.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    except SQLAlchemyError:
        logger.exception(
            "Erreur lors de la récupération des taux M3"
        )
        raise DatabaseError(operation="get_all_monetary_m3_rates")

    # 3. Logger le résultat et retourner les données
    if not m3_rate:
        logger.warning(
            "Aucun taux M3 trouvé (skip=%s, limit=%s)",
            skip, limit
        )
        raise MacroIndicatorsNotFound(skip=skip, limit=limit)
    else:
        logger.info(
            "%d taux M3 récupérés.",
            len(m3_rate)
        )
    return m3_rate


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
        RuntimeError: En cas d'erreur de requête.
    """
    try:
        query = text("""
            SELECT
                date AS day,
                rate_mro,
                inflation_rate,
                unemployment_rate,
                monetary_m3_rate
            FROM v_macro_indicators_daily_v1
            WHERE date BETWEEN :start_date AND :end_date
            ORDER BY date ASC
        """)
        result = db.execute(query, {"start_date": start_date, "end_date": end_date})
        logger.info(f"Indicateurs macro récupérés de {start_date} à {end_date}.")
        return result.fetchall()
    except SQLAlchemyError:
        logger.exception("Erreur lors de la récupération des indicateurs journaliers")
        raise RuntimeError("Erreur lors de la récupération des indicateurs macroéconomiques")
