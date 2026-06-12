"""
    Script : python injection_data_unemployment.py
    Projet : VolatichainXplorerAI
    Date : 2025-06-19
    Date de mise à jour : 2026-06-09

    Description :
        Ce script insère automatiquement toutes les données de taux de chômage néttoyées
        depuis des fichiers .csv dans la table "t_macro_bce_unemployment".

    Usage : python injection_data_unemployment.py
"""
# Charger les librairies en nécessaires
import sys
from pathlib import Path

# Définir le chemin du projet et ajouter au PYTHONPATH pour les imports absolus
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

#from database.conn_db.connect_postgresql import get_db
import pandas as pd # noqa: E402
from database.postgres.models.macro_indicators import MacroBcetauxChomage # noqa: E402
from database.conn_db.connect_postgresql import SessionLocal # noqa: E402
from sqlalchemy.orm import Session # noqa: E402
from setup.logger_config import setup_logger # noqa: E402


# Chemin du fichier CSV de manière dynamique
csv_path = project_root / "data" / "cleaned"/ "unemployment_rate_cleaned_updated.csv"

# Récupération du nom du module
list_name : list[str] = "scripts/import_db/injection_data_unemployment.py".split("/", 3)
module_name = str(list_name[2].split(".",1)[0])

# set le logger du module en cours
logger = setup_logger(module_name)

# Charger le fichier CSV
df = pd.read_csv(csv_path,
                 sep=",", 
                 encoding="utf-8",
                 engine= "python")

# Connexion à la base de données
logger.info("Début de la connexion à la base de données postgresql")
db: Session = SessionLocal()

# Récupérer les données du dataframe
records = []

for _, row in df.iterrows():
    # Estancier la classe macroBcetauxChomage avec les données du dataframe
    macroBcetauxChomage = MacroBcetauxChomage(
        date_unemployment = row["date"],
        time_period_unemployment = row["TIME_PERIOD"],
        obs_status_unemployment = row["OBS_STATUS"],
        unemployment_rate = row["OBS_VALUE"],
        indicator_name_unemployment = row["TITLE"],
        source_label_unemployment=row.get("SOURCE_LABEL")

    )  

    records.append(macroBcetauxChomage)
    logger.info(f"{len(records)} enregistrements à injecter")

# Connexion à la base de données
try:
    logger.info("Début d'injection des données à la base de données postgresql")
    with SessionLocal() as db:
        db.add_all(records)
        db.commit()
        logger.info("Injection des données concernant le taux de chômage terminée avec succès")
except Exception as e:
    logger.error(f"Erreur enregistrée pendant l'injection : {e}")
    raise 
finally:
    logger.info("Fin d'injection des données concernant le taux de chômage")