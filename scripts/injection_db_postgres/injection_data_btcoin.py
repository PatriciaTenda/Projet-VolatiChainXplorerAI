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
import os 
import sys
from pathlib import Path

# Ajouter le dossier racine du projet au PYTHONPATH pour permettre les imports absolus
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd  # noqa: E402
from database.postgres.models.bitcoin_prices import BitcoinPrices  # noqa: E402
from database.conn_db.connect_postgresql import SessionLocal  # noqa: E402
from setup.logger_config import setup_logger  # noqa: E402


# Récupération du nom du module
module_name = os.path.basename(__file__).replace(".py", "")


# set le logger du module en cours
logger = setup_logger(module_name)

# Définir le chemin du fichier CSV de manière dynamique
csv_path = project_root / "data" / "cleaned" / "bitcoin_historical_cleaned.csv"

# Charger le fichier CSV
df = pd.read_csv(csv_path, sep=",", encoding="utf-8")
logger.debug(f"Extrait du DF :\n{df.head()}")
logger.info(f"Fichier chargé : {csv_path}")

# Vérification des colonnes attendues
required_columns = ["date_bitcoin", "open", "high", "low", "close", "volume", "marketCap"]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    logger.error(f"Colonnes manquantes dans le CSV : {missing_columns}")
    sys.exit(1)

if df.empty:
    logger.warning("CSV vide — aucune donnée à injecter")
    exit(0)

logger.info(f"Nombre de lignes à injecter : {len(df)}")

# Récupérer les données du dataframe
records = []

for _, row in df.iterrows():
    # Instancier la classe BitcoinPrices avec la nouvelle structure
    bitcoinprices = BitcoinPrices(
        date = pd.to_datetime(row["date_bitcoin"]).date(),
        open_price = row["open"],
        high_price = row.get("high"),
        low_price = row.get("low"),
        close_price = row["close"],
        volume = row.get("volume"),
        market_cap = row.get("marketCap"),
        source = "coinmarketcap_manual_csv",
        currency = "EUR",
        granularity = "1d"
        # collected_at sera auto-généré par server_default
    )
    records.append(bitcoinprices)

logger.info(f"{len(records)} enregistrements préparés pour injection")

# Injection des données avec context manager
logger.info("Début d'injection des données à la base de données postgresql")
try:
    with SessionLocal() as db:
        db.add_all(records)
        db.commit()
        logger.info(f"Injection réussie : {len(records)} enregistrements insérés dans t_bitcoin_prices")
except Exception as e:
    logger.error(f"Erreur pendant l'injection : {e}")
    raise
finally:
    logger.info("Fin du processus d'injection")