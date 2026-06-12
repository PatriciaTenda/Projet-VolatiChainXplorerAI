"""
    Script : python injection_data_Inflation.py
    Projet : VolatichainXplorerAI
    Date : 2025-06-19
    Date de mise à jour : 2026-06-12

    Description :
        Ce script insère automatiquement toutes les données de taux d'inflation néttoyées
        depuis des fichiers .csv dans la table "t_macro_bce_inflation".

    Usage : python injection_data_Inflation.py
"""
# Charger les librairies en nécessaires
import sys
from pathlib import Path

# Chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

import pandas as pd # noqa E402
from database.postgres.models.macro_indicators import MacroBceInflation # noqa E402
from database.conn_db.connect_postgresql import SessionLocal # noqa E402
from setup.logger_config import setup_logger # noqa E402

# Chemin du CSV
csv_path = project_root / "data" / "cleaned" / "HICP_Inflation_cleaned_updated.csv"

# Récupération du nom du module
path_module = "scripts / import_db / injection_data_Inflation.py".split("/", 3)
name_module = path_module[2].replace(".py", " ").strip()

# set le logger du module en cours
logger = setup_logger(name_module)

# Charger le fichier CSV
df = pd.read_csv(csv_path, 
                 sep=",", 
                 encoding="utf-8-sig",
                 engine="python")

# Récupérer les données du dataframe
records = []

for _, row in df.iterrows():
    # Estancier la classe macroBceInflation avec les données du dataframe
    macroBceInflation = MacroBceInflation(
        date_inflation=row["date"],
        time_period_inflation=row["TIME_PERIOD"],
        inflation_rate=row["OBS_VALUE"],
        obs_status_inflation=row["OBS_STATUS"],
        indicator_name_inflation=row["TITLE"],
        source_label_inflation=row.get("SOURCE_LABEL")

    )  
    records.append(macroBceInflation)
    logger.info(f"{len(records)} enregistrements à injecter")

# Connexion à la base de données
try:
    logger.info("Début d'injection des données à la base de données postgresql")
    with SessionLocal() as db:
        db.add_all(records)
        db.commit()
        logger.info("Injection des données du taux d'inflation terminée avec succès")
except Exception as e:
    logger.error(f"Erreur enregistrée pendant l'injection : {e}")
    raise 
finally:
    logger.info("Fin d'injection des données du taux d'inflation")