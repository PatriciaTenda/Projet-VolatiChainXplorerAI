import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from database.conn_db.connect_postgresql import get_db
from database.postgres.models.macro_indicators import MacroBceInflation,MacroBceMonetaryM3,MacroBceMRO,MacroBcetauxChomage
from api.schemas.macro_indicators import MacroIndicatorsResponse, UnemploymentResponse,MonetaryM3Response,MroResponse,InflationResponse
from api.crud.crud_macro_indicators import get_all_inflation_rates, get_all_monetary_m3_rates, get_all_unemployment_rates, get_macro_indicators_daily,get_mro_rates_by_date_range
from api.schemas.macro_indicators import MacroIndicatorsResponse
from setup.logger_config import setup_logger

# Mise en place d'un logger pour le module de création des collections
name_file =os.path.splitext(os.path.basename(__file__))[0]
# set le logger du module en cours
logger = setup_logger(name_file)


# Création d’un routeur dédié aux routes relatives aux indicateurs macroéconomiques
router = APIRouter(
    prefix="/api/v1/macro-indicator",
    tags=["Macroeconomic indicator"]
)



# Route - Taux MRO
@router.get("/mro", response_model=List[MroResponse])
def read_mro_rates(
    start_date: date = Query(..., description="Date de début au format YYYY-MM-DD"),
    end_date: date = Query(..., description="Date de fin au format YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    return get_mro_rates_by_date_range(db, start_date, end_date)


# Route - Taux d'inflation (pagination)
@router.get("/inflation", response_model=List[InflationResponse])
def read_inflation_rates(
    skip: int = Query(0, ge=0, description="Nombre d'enregistrements à ignorer pour la pagination (par défaut 0)"),
    limit: int = Query(10, gt=0, le=100, description="Nombre maximum d'enregistrements à retourner (entre 1 et 100, par défaut 10)"),
    db: Session = Depends(get_db)
):
    return get_all_inflation_rates(db, skip=skip, limit=limit)


# Route - Taux de chômage (pagination)
@router.get("/unemployment", response_model=List[UnemploymentResponse])
def read_unemployment_rates(
    skip: int = Query(0, ge=0, description="Nombre d'enregistrements à ignorer pour la pagination (par défaut 0)"),
    limit: int = Query(10, gt=0, le=100, description="Nombre maximum d'enregistrements à retourner (entre 1 et 100, par défaut 10)"),
    db: Session = Depends(get_db)
):
    return get_all_unemployment_rates(db, skip=skip, limit=limit)


# Route - Taux de variation M3 (pagination)
@router.get("/m3", response_model=List[MonetaryM3Response])
def read_m3_rates(
    skip: int = Query(0, ge=0, description="Nombre d'enregistrements à ignorer pour la pagination (par défaut 0)"),
    limit: int = Query(10, gt=0, le=100, description="Nombre maximum d'enregistrements à retourner (entre 1 et 100, par défaut 10)"),
    db: Session = Depends(get_db)
):
    return get_all_monetary_m3_rates(db, skip=skip, limit=limit)


#  Route - Vue agrégée journalière
@router.get("/daily", response_model=List[MacroIndicatorsResponse])
def read_daily_macro_indicators(
    start_date: date = Query(..., description="Date de début"),
    end_date: date = Query(..., description="Date de fin"),
    db: Session = Depends(get_db)
):
    try:
        return get_macro_indicators_daily(db, start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
