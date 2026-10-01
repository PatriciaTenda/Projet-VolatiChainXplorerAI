"""
Script : cleaned_bitcoin_historical_data.py
Projet : VolatiChainXplorerAI
Date de mise à jour : 2026-09-15

Description :
    Nettoyer les données historiques Bitcoin issues de CoinMarketCap
    et exporter un fichier prêt pour l'injection PostgreSQL.
"""
import sys
from pathlib import Path

import pandas as pd

# Définir le chemin du projet
path_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(path_root))

from setup.logger_config import setup_logger

name_module = Path(__file__).stem
logger = setup_logger(name_module)


# Définir le chemin vers le fichier csv à nettoyer
path_csv = (
    path_root 
    / "data" 
    / "raw" 
    / "csvFile" 
    / "Bitcoin_11_08_2025-12_09_2026_historical_data_coinmarketcap.csv"
)
if  not path_csv.exists():
    raise FileNotFoundError(
        "Le fichier csv est introuvable!"
    )

# Définir le chemin vers le fichier csv nettoyé
output_csv = (
    path_root
    / "data"
    / "cleaned"
    / "bitcoin_historical_cleaned_04-06-2026_12-09-2026.csv"
)
output_csv.parent.mkdir(parents=True, exist_ok=True)

# chargement du fichier csv brut et création du DataFrame pandas
df = pd.read_csv(
                path_csv, 
                sep=";", 
                encoding="utf-8-sig",          # pour gérer les caractères BOM
                engine="python"                # pour bien parser les séparateurs personnalisés
)

# supprimer les espaces des noms de colonnes du dataset
df.columns = df.columns.str.strip()
required_columns = [
    "timeOpen", 
    "open", 
    "high", 
    "low", 
    "close", 
    "volume", 
    "marketCap"
]

# Vérifier les colonnes manquantes
missing_col = [
    col for col in required_columns
    if col not in df.columns
]
if missing_col:
    logger.error(f"Les colonnes manquantes : {missing_col}")
    raise ValueError(f"Les colonnes manquantes : {missing_col}")

df_bitcoin = df[required_columns].copy()

""" Nétoyage des données"""

# garantir que les colonnes sont dans le format numeric
colomnes_numerics = [
    "open", 
    "high",
    "low",
    "close", 
    "volume", 
    "marketCap"
]
for col in colomnes_numerics:
    df_bitcoin[col] = pd.to_numeric(df_bitcoin[col], errors='coerce')
    
# Ajout de la date simplifiée (clé logique) 
df_bitcoin["date"] = pd.to_datetime(df_bitcoin["timeOpen"]).dt.date
logger.info("Colonne 'date' ajoutée avec succès.")

# colonnes uilis&es
columns_used = [
    "date", 
    "open", 
    "high", 
    "low", 
    "close", 
    "volume", 
    "marketCap"
]
# Vérifier les colonnes manquantes
missing_col = [
    col for col in columns_used
    if col not in df_bitcoin.columns
]
if missing_col:
    logger.error(f"Les colonnes manquantes : {missing_col}")
    raise ValueError(f"Les colonnes manquantes : {missing_col}")

df_updated_bitcoin = df_bitcoin[columns_used].copy()

# nettoyage des données propres
rows_before_cleaning = len(df_updated_bitcoin)
df_updated_bitcoin= (
        df_updated_bitcoin
        .dropna(subset=["date", *colomnes_numerics])
        .sort_values("date")
        .reset_index(drop=True)
)

logger.info(
    "Nettoyage terminé : %s de lignes supprimées.",
    rows_before_cleaning - len(df_updated_bitcoin)
)

# Filtrage des données à partir de la date spécifiée
start_date = pd.Timestamp("2026-06-04").date()
df_updated_bitcoin = df_updated_bitcoin[
    df_updated_bitcoin["date"] >= start_date
].copy()

logger.info(f"Colonnes du dataset réduit : {df_updated_bitcoin.columns.tolist()}")
logger.info(f"Aperçu du dataset réduit :\n{df_updated_bitcoin.head()}")

# Export des données propres
# df_updated_bitcoin.to_csv("data/cleaned/bitcoin_historical_cleaned.csv", index=False)
df_updated_bitcoin.to_csv(
    output_csv, 
    index=False,
    encoding="utf-8-sig"
)
logger.info("Fichier Bitcoin nettoyé et exporté.")