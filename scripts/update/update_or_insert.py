""" Ce script générique à pour but de mettre à jour les données dans les tables en base de données postgresql en cas de besoin"""

# Charger les libraiiries nécessaires

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from database.conn_db.connect_postgresql import SessionLocal
from setup.logger_config import setup_logger


# Récupération du nom du module
module_name = os.path.basename(__file__).split(".",1)[0]
print(module_name)

# Créer un logger pour journaliser les exécutions du script
logger = setup_logger(module_name)

"""# Connexion à la base de données
logger.info("Début de connexion à la base de donnée")
db: Session = SessionLocal()
"""
# Fonction qui éxécute l'upsert afin de mettre à jours une table en base de données PostgreSQL
def upsert_table(df, model, db : Session, col_conflit : list, col_to_update: list) -> None:

    """
    Effectue un INSERT ou UPDATE sur conflit pour une table SQLAlchemy.
    :param df: DataFrame à insérer
    :param model: Modèle SQLAlchemy ciblé
    :param db: session SQLAlchemy
    :param col_conflit: liste des colonnes déclenchant un conflit
    :param col_to_update: colonnes à mettre à jour en cas de conflit
    """
    records = df.to_dict(orient="records")

    for row in records:
        upsert_query = insert(model).values(**row)
        upsert_query = upsert_query.on_conflict_do_update(
            index_elements= col_conflit,
            set_={col: getattr(upsert_query.excluded, col) for col in col_to_update}
        )
        try:
            logger.info("Début de la mise à jour et de l'insertion de la nouvelle valeur")
            db.execute(upsert_query)
        except Exception as e:
            logger.error(f"Erreur l'hors de l'upsert : {e}")
            db.rollback()
            raise

    db.commit()
    logger.info("Fin de l'insertion/ Mise à jour terminée")


# Fonction pour implémenter la fonction upsert_table() sur les tables 
def main():
    # Charger le modèle sollicité
    from database.postgres.models.macro_indicators import MacroBceMRO

    # Charger le fichier csv 
    df = pd.read_csv("data/cleaned/bce_mro_cleaned.csv", usecols=["TIME_PERIOD","OBS_VALUE", "TIME_FORMAT", "TITLE","SOURCE_LABEL"] , sep = ",", encoding="utf-8")

    # Renommer les colonnes pour facilieter le mappage avec les table du modele SQLAlchemy
    df = df.rename(columns={
        "TIME_PERIOD": "date_mro",
        "OBS_VALUE": "rate_mro",
        "TIME_FORMAT": "time_periode_mro",
        "TITLE": "indicator_name_mro",
        "SOURCE_LABEL": "source_label_mro"
        }
    )

    # Identifier les colonnes clées pour conflit et update
    col_conflit = ["date_mro"]
    col_to_update =["date_mro","rate_mro", "time_periode_mro", "indicator_name_mro", "source_label_mro"]

    # Connexion avec la base de données
    logger.info("Connexion à la base de données")
    db: Session= SessionLocal()
    logger.info("Connexion réussie!")

    try:
        # Appel de la fonction upsert_table 
        upsert_table(df, MacroBceMRO, db= db, col_conflit= col_conflit, col_to_update=col_to_update)
    
    finally:
        db.close()
        logger.info("Session terminée!")

if __name__ == "__main__":
    main()









