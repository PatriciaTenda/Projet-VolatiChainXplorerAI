"""
    Ce script générique a pour but de fusionner les données dans les tables de bitcoin 
    et de la vue qui fusionne les données macroéconomiques en base de données postgresql,
    pour construire un dataset utilisable pour l'entrainement d'un modele de prédiction.
"""

# Charger les librairies nécessaires
import sys
from pathlib import Path

import pandas as pd

# Chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from database.conn_db.connect_postgresql import engine  #noqaE402
from setup.logger_config import setup_logger  #noqaE402

# Chemin vers le repertoire d'exports 
output_path = (
    project_root 
    / "data" 
    / "exports"
    / "datasets" 
    / "unprocessed"
    / "btc_macro_dataset.csv"
)
output_path.parent.mkdir(parents=True, exist_ok=True)

# Récuperation du nom du module
name_module = Path(__file__).stem

# créer un logger pour journaliser les exécutions du script
logger = setup_logger(name_module)
logger.info(f"Le nom du module est : {name_module}") 

# requête SQL pour joindre la table bitcoin et la vue macroéconomiques afin de construire un dataset
join_query = """
        SELECT
            b.date,
            b.open,
            b.high,
            b.low,
            b.close,
            b.volume,
            b.market_cap,
            m.rate_mro,
            m.inflation_rate,
            m.unemployment_rate,
            m.monetary_m3_rate
        FROM t_bitcoin_prices b
        LEFT JOIN v_macro_indicators_daily_v1 m
            ON b.date = m.date
        WHERE b.date >= '2010-07-14'
            AND b.source = 'coinmarketcap_historical_data'
            AND b.granularity = '1d'
            AND b.currency = 'EUR'
        ORDER BY b.date ASC    
"""

# Charger le dataset en utilisant la requete SQL
def load_dataset_from_db(query:str) -> pd.DataFrame:
    """
       Cette fonction charge le resultat de la requete SQL dans un dataframe pandas 
    """
    
    logger.info("Début du chargement du dataframe à partir des données de la jointure.")
    try:
        df = pd.read_sql_query(query, con=engine)
        if df.empty:
            raise ValueError("La jointure n'a retourné aucune donnée")

        duplicated_dates = df["date"].duplicated().sum()

        if duplicated_dates:
            raise ValueError(
                f"{duplicated_dates} date(s) dupliquée(s) dans le dataset"
            )
        # Vérification des valeurs manquantes dans les colonnes macroéconomiques
        macro_columns = [
            "rate_mro",
            "inflation_rate",
            "unemployment_rate",
            "monetary_m3_rate"
        ]

        logger.info(
            "Valeurs macroéconomiques manquantes :\n%s",
            df[macro_columns].isna().sum()
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
                
        df.to_csv(output_path,
                  sep=",",
                  encoding="utf-8",                   
                  index=False
        )
        logger.info(
            "Dataset exporté : %s lignes, %s colonnes, du %s au %s",
            len(df),
            len(df.columns),
            df["date"].min(),
            df["date"].max()
        )
        return df
    except Exception:
        logger.exception(
            "Échec de la construction du dataset Bitcoin/macro"
        )
        raise
        
        

if __name__ == "__main__":
    # Charger le datatset à partir de la base de données
    df = load_dataset_from_db(join_query)
    logger.info(f"Aperçu du dataset :\n{df.head()}")