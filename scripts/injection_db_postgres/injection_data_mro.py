"""
    Script : python injection_data_mro.py
    Projet : VolatichainXplorerAI
    Date : 2025-06-19
    Date de mise à jour : 2026-06-11

    Description :
        Ce script insère automatiquement toutes les données de taux directeur MRO néttoyées
        depuis des fichiers .csv dans la table "t_macro_bce_mro".

    Usage : python injection_data_mro.py
"""
# Charger les librairies en nécessaires
import sys
from pathlib import Path

#  Chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

#from database.conn_db.connect_postgresql import get_db
import pandas as pd # noqa: E402
from database.postgres.models.macro_indicators import MacroBceMRO # noqa: E402
from database.conn_db.connect_postgresql import SessionLocal # noqa: E402
from setup.logger_config import setup_logger # noqa: E402

# Récupération du nom du module
module_path= "scripts / import_db / injection_data_mro.py".split("/", 3)
module_name = module_path[2].replace(".py", " ").strip()

# set le logger du module en cours
logger = setup_logger(module_name)


# Chemin du CSV
csv_path = project_root / "data" / "cleaned" / "bce_mro_cleaned_updated.csv"

# Charger le fichier CSV
df = pd.read_csv(csv_path, 
                 sep=",", 
                 encoding="utf-8",
                 engine= "python"
                )

logger.debug(f"Extrait du DF :\n{df.head()}")
logger.info(f"Fichier chargé : {csv_path}")

# Récupérer les données du dataframe
records = []

for _, row in df.iterrows():
    # Estancier la classe MacroBceMRO avec les données du dataframe
    # mro : Main Refenancing operational
    mro = MacroBceMRO(
        date_mro=row["date"],
        time_period_mro=row["TIME_PERIOD"],
        rate_mro=row["OBS_VALUE"],
        obs_status_mro = row["OBS_STATUS"],
        indicator_name_mro=row.get("TITLE"),
        source_label_mro=row.get("SOURCE_LABEL"),
        
    )  
    records.append(mro)
    logger.info(f"{len(records)} enregistrements à injecter")

# Connexion à la base de données
try:
    logger.info("Début d'injection des données du MRO à la base de données postgresql")
    with SessionLocal() as db:
        db.add_all(records)
        db.commit()
        logger.info("Injection des données du MRO terminée avec succès")
except Exception as e:
    logger.error(f"Erreur enregistrée pendant l'injection : {e}")
    raise 
finally:
    logger.info("Fin d'injection des données du MRO")