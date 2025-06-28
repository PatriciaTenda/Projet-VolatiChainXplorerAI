"""
    Script : python injection_data_bitcoin.py
    Projet : VolatichainXplorerAI
    Date : 2025-06-19

    Description :
        Ce script insère automatiquement toutes les données de cours historique du bitcoin néttoyées
        depuis des fichiers .csv dans la table "t_bitcoin_prices".

    Usage :
        python injection_data_bitcoin.py
"""
# Charger les librairies en nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))

#from database.conn_db.connect_postgresql import get_db
import pandas as pd
from database.postgres.models.bitcoin_prices import BitcoinPrices
from database.conn_db.connect_postgresql import SessionLocal
from sqlalchemy.orm import Session
from setup.logger_config import setup_logger

# Récupération du nom du module
module_name = "scripts\\import_db\\injection_data_btcoin.py".split("\\", 3)
module_name = module_name[2].split(".",1)[0]

# set le logger du module en cours
logger = setup_logger(module_name)

# Charger le fichier CSV
df = pd.read_csv("data/cleaned/bitcoin_historical_cleaned.csv", sep=",", encoding="utf-8")
logger.debug(f"Extrait du DF :\n{df.head()}")

# Vérification de l'état du dataframe
if df.empty:
    logger.warning("CSV vide — terminaison du script")
    exit(0)

# Connexion à la base de données
logger.info("Début de la connexion à la base de données postgresql")
db: Session = SessionLocal()

# Récupérer les données du dataframe
records = []

for _, row in df.iterrows():
    # Estancier la classe BitcoinPrices
    bitcoinprices = BitcoinPrices(
        date_bitcoin=row["date_bitcoin"],
        time_open_bitcoin=row["timeOpen"],
        time_close_bitcoin=row["timeClose"],
        time_high_bitcoin=row.get("timeHigh"),
        time_low_bitcoin=row.get("timeLow"),
        open_price_bitcoin=row["open"],
        close_price_bitcoin=row["close"],
        high_price_bitcoin=row.get("high"),
        low_price_bitcoin=row.get("low"),
        volume_bitcoin=row.get("volume"),
        market_Cap_bitcoin=row.get("marketCap")
    )
    records.append(bitcoinprices)
    logger.info(f"{len(records)} enregistrements à injecter")

# Connexion à la base de données
try:
    logger.info("Début d'injection des données à la base de données postgresql")
    db.bulk_save_objects(records)
    db.commit()
    logger.info("Injection terminée avec succès")
except Exception as e:
    logger.error(f"Erreur enregistrée pendant l'injection : {e}")
    db.rollback()
    raise 
finally:
    db.close()
    logger.info("Fin d'injection et fermeture de la session")