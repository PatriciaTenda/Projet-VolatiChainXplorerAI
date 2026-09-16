"""
    Script : python injection_data_bitcoin.py
    Projet : VolatichainXplorerAI
    Date : 2026-06-02 (mis à jour)

    Description :
        Ce script insère automatiquement toutes les données de cours historique du bitcoin nettoyées
        depuis bitcoin_historical_cleaned.csv dans la table "t_bitcoin_prices".
        
        Structure de la nouvelle table :
        - date, open, high, low, close, volume, market_cap
        - source = 'coinmarketcap_manual_csv'
        - currency = 'EUR'
        - granularity = '1d'
        - collected_at (auto-généré)

    Usage :
        python injection_data_bitcoin.py
"""
# Charger les librairies nécessaires
import sys
from pathlib import Path

# Ajouter le dossier racine du projet au PYTHONPATH pour permettre les imports absolus
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from database.conn_db.connect_postgresql import SessionLocal
from database.postgres.models.bitcoin_prices import BitcoinPrices
from setup.logger_config import setup_logger

# Récupération du nom du module
module_name = Path(__file__).stem

# set le logger du module en cours
logger = setup_logger(module_name)

# Définir le chemin du fichier CSV de manière dynamique
csv_path = (
    project_root 
    / "data" 
    / "cleaned" 
    / "bitcoin_historical_cleaned_04-06-2026_12-09-2026.csv"
)
if not csv_path.exists():
    raise FileNotFoundError(
       f"Fichier csv introuvable :{csv_path}"
    )
    
# Charger le fichier CSV
df = pd.read_csv(
    csv_path, sep=",", 
    encoding="utf-8"
)

logger.debug(f"Extrait du DF :\n{df.head()}")
logger.info(f"Fichier chargé : {csv_path}")

# Adapter le nom de la colonne "marketCap" correspondant à celui de la table PostgreSQL
df_bitcoin = df.rename(columns={
    "marketCap":"market_cap"
})

# Definir les colonnes "source", "currency" et "granularity" avec des valeurs par defaut
df_bitcoin["source"] = "coinmarketcap_historical_data"
df_bitcoin["currency"] = "EUR"
df_bitcoin["granularity"] = "1d"

# Vérification des colonnes attendues
required_columns = [
    "date", 
    "open", 
    "high", 
    "low",
    "close", 
    "volume", 
    "market_cap",
    "source",
    "currency",
    "granularity"
]

missing_columns = [
    col for col in required_columns 
    if col not in df_bitcoin.columns
]

if missing_columns:
    raise ValueError(f"Colonnes manquantes dans le CSV : {missing_columns}")

if df_bitcoin.empty:
    raise ValueError("CSV vide - aucune donnée à injecter")
logger.info(f"Nombre de lignes à injecter : {len(df_bitcoin)}")

# Garantir la "date" au faormat datetime
df_bitcoin["date"] = pd.to_datetime(
    df_bitcoin["date"],
    errors="raise",
).dt.date 

# Convertir les lignes du dataset en dictionnaire
records = df_bitcoin[required_columns].to_dict(orient="records")
if not records:
    raise ValueError("Aucune données de bitcoin disponibles pour l'injection")
   

# Mettre en place l'intruction INSERT avec SQLAlchemy pour PostgreSQL
logger.info("Début de l'injection des données depuis le CSV")
insert_query = insert(BitcoinPrices.__table__).values(records)
upsert_query = insert_query.on_conflict_do_update(
    constraint="uq_t_bitcoin_prices_date_source_currency_granularity",
    set_={
        "open":insert_query.excluded.open, 
        "high":insert_query.excluded.high, 
        "low":insert_query.excluded.low,
        "close":insert_query.excluded.close, 
        "volume":insert_query.excluded.volume, 
        "market_cap":insert_query.excluded.market_cap,
        "collected_at": func.now()
    }
)
logger.info(f"{len(records)} enregistrements préparés pour injection")

# Injection des données avec context manager
with SessionLocal() as db:
    logger.info("Début d'injection des données à la base de données postgresql")
    try:
        db.execute(upsert_query)
        db.commit()
        logger.info(
            "Upsert Bitcoin réussi : %s lignes traitées",
            len(records)
        )
    except SQLAlchemyError as error:
        db.rollback()
        logger.error(
            "Erreur pendant l'upsert Bitcoin : %s",
            error
        )
        raise
 