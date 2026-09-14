"""
    Script : python injection_data_unemployment.py
    Projet : VolatichainXplorerAI
    Date : 2025-06-19
    Date de mise à jour : 2026-09-11

    Description :
            Ce script met à jour la table "t_macro_bce_unemployment"
            à partir du fichier CSV nettoyé.
        
            Pour chaque date :
            - si elle n'existe pas, la ligne est insérée ;
            - si elle existe, ses valeurs sont mises à jour.
"""
# Charger les librairies en nécessaires
import sys
from pathlib import Path

#  Chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError

from database.conn_db.connect_postgresql import SessionLocal
from database.postgres.models.macro_indicators import MacroBcetauxChomage
from setup.logger_config import setup_logger

# Récupération du nom du module
module_name = Path(__file__).stem

# set le logger du module en cours
logger = setup_logger(module_name)

# Set du chemin du fichier CSV et verifier son existence
csv_path = (
    project_root 
    / "data" 
    / "cleaned" 
    / "unemployment_rate_cleaned_updated.csv"
)
if not csv_path.exists():
    raise FileNotFoundError(
        f"Le fichier CSV n'existe pas: {csv_path}"
    )   
# Charger le fichier CSV
df = pd.read_csv(csv_path, 
                 sep=",", 
                 encoding="utf-8",
                 engine= "python"
                )

logger.debug(f"Extrait du DF :\n{df.head()}")
logger.info(f"Fichier chargé : {csv_path}")

# Adapter les noms des colonnes du csv au format attendu par sqlalchemy
df_unemployment = df.rename(columns={
    "OBS_VALUE" : "value",
    "OBS_STATUS": "obs_status",
    "TIME_PERIOD" : "time_period",
    "TITLE" : "indicator_name",
    "SOURCE_LABEL": "source_label"
})

# Adapter les noms des colonnes  du csv à ceux de la base de données 
columns_db_unemployment = [
    "date",
    "value",
    "obs_status",
    "time_period",
    "indicator_name",
    "source_label"  
]

df_unemployment = df_unemployment[columns_db_unemployment]

# S'assurer que la colonne "date" est au format datetime
df_unemployment["date"]= pd.to_datetime(
    df_unemployment["date"],
    errors="raise"
).dt.date

# convertir les lignes du dataframe en dictionnaires
records = df_unemployment.to_dict(orient="records")

# Vérifier que les données existent
if not records:
    logger.warning("Aucune données de chômage disponible pour l'injection")
    sys.exit(0)
logger.info(f"Nombre de lignes à injecter : {len(records)}")
print(records[0])

# Mettre en place l'instruction INSERT pour l'injection des données de chômage dans PostgreSQL
insert_query = insert(MacroBcetauxChomage.__table__).values(records) 
upsert_query = insert_query.on_conflict_do_update(
    index_elements=["date"],
    set_={
          "value": insert_query.excluded.value,
          "obs_status": insert_query.excluded.obs_status,
          "time_period": insert_query.excluded.time_period,
          "indicator_name": insert_query.excluded.indicator_name,
          "source_label": insert_query.excluded.source_label    
    }
)

# Exécuter l'injection dans la base de données
with SessionLocal() as session:
    try:
        logger.info("Début de l'upsert des données de chômage")
        session.execute(upsert_query)
        session.commit()
        logger.info(
            "Upsert des données de chômage reussie : %s lignes traitées",
             len(records)
        )
    except SQLAlchemyError as error:
        session.rollback()
        logger.error(
            "Erreur lors de l'upsert des données de chômage : %s",
            error,
        )
        raise