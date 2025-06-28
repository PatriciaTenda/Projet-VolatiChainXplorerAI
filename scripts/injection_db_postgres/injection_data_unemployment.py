"""
    Script : python injection_data_unemployment.py
    Projet : VolatichainXplorerAI
    Date : 2025-06-19

    Description :
        Ce script insère automatiquement toutes les données de taux de chômage néttoyées
        depuis des fichiers .csv dans la table "t_macro_bce_unemployment".

    Usage : python injection_data_unemployment.py
"""
# Charger les librairies en nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))

#from database.conn_db.connect_postgresql import get_db
import pandas as pd
from database.postgres.models.macro_indicators import MacroBcetauxChomage
from database.conn_db.connect_postgresql import SessionLocal
from sqlalchemy.orm import Session
from setup.logger_config import setup_logger

# Récupération du nom du module
module_name = "scripts\\import_db\\injection_data_unemployment.py".split("\\", 3)
module_name = module_name[2].split(".",1)[0]

# set le logger du module en cours
logger = setup_logger(module_name)

# Charger le fichier CSV
df = pd.read_csv("data/cleaned/unemployment_rate_cleaned.csv", sep=",", encoding="utf-8")

# Connexion à la base de données
logger.info("Début de la connexion à la base de données postgresql")
db: Session = SessionLocal()

# Récupérer les données du dataframe
records = []

for _, row in df.iterrows():
    # Estancier la classe BitcoinPrices
    # mro : Main Refenancing operational
    macroBcetauxChomage = MacroBcetauxChomage(
        date_unemployment=row["TIME_PERIOD"],
        unemployment_rate=row["OBS_VALUE"],
        indicator_name_unemployment=row["TITLE"],
        source_label_unemployment=row.get("SOURCE_LABEL")

    )  
    records.append(macroBcetauxChomage)
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