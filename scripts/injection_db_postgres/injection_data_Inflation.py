"""
    :param Script : python  scripts/injection_db_postgres/injection_data_inflation.py
    :param Projet : VolatichainXplorerAI
    :param Date : 2025-06-19
    :param Date de mise à jour : 2026-09-09

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

import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from database.conn_db.connect_postgresql import SessionLocal
from database.postgres.models.macro_indicators import MacroBceInflation
from setup.logger_config import setup_logger

# Chemin du CSV
csv_path = project_root / "data" / "cleaned" / "HICP_Inflation_cleaned_updated.csv"

# Récupération du nom du module
name_module = Path(__file__).stem

# set le logger du module en cours
logger = setup_logger(name_module)

# Charger le fichier CSV
df = pd.read_csv(csv_path, 
                 sep=",", 
                 encoding="utf-8-sig",
                 engine="python")

# Adapter les noms des colonnes du CSV au format attendu par le modele SQLAlchemy
df_inflation= df.rename(columns={
        "OBS_VALUE":"value",                
        "OBS_STATUS":"obs_status",
        "TIME_PERIOD":"time_period",
        "TITLE":"indicator_name",
        "SOURCE_LABEL":"source_label"
})

# Adapter les noms des colonnes du CSV aux colonnes de la base de données postgres
columns_db=[
    "date",
    "value",
    "obs_status",
    "time_period",        
    "indicator_name",
    "source_label"
]
                         
df_inflation = df_inflation[columns_db]

# garantir que la colonne "date" est au format datetime
df_inflation["date"] = pd.to_datetime(df_inflation["date"]).dt.date

# Enlever les espaces autour du nom de la
df_inflation["source_label"] =df_inflation["source_label"].str.strip()

# transformer les ligne en dictionnaire
records = df_inflation.to_dict(orient="records")

# Vérifier si des enregistrements sont disponibles pour l'injection
if not records:
    logger.warning("Aucun données d'inflation disponibles pour l'injection")
    sys.exit(0)
print(records[0])
logger.info(f"{len(records)} enregistrements prêts pour l'injection")


# Construire l'instruction INSERT pour la table d'inflation
insert_query = insert(MacroBceInflation.__table__).values(records)
upsert_query = insert_query.on_conflict_do_update(
    index_elements=["date"],
    set_={
         "value":insert_query.excluded.value,
            "obs_status":insert_query.excluded.obs_status,
            "time_period":insert_query.excluded.time_period,        
            "indicator_name":insert_query.excluded.indicator_name,
            "source_label":insert_query.excluded.source_label
    }
)

# Exécuter l'intruction UPSERT dans la base de données
with SessionLocal() as session:
    logger.info("Début de l'injection des données d'inflation")
    try:
        session.execute(upsert_query)
        session.commit()
        logger.info(f"Injection des données d'inflation terminées avec succès : {len(records)} enregistrements injectés")
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Erreur lors de l'injection des données d'inflation : {e}")
        raise    
    