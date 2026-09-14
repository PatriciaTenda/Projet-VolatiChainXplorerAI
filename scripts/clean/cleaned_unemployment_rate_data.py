"""
Nettoyage et préparation des données sur le taux de chômage.
Ce script charge les données brutes, effectue le nettoyage nécessaire,
et exporte les données nettoyées vers un fichier CSV.
"""
import sys
from pathlib import Path

import pandas as pd

# Ajouter le dossier racine du projet au PYTHONPATH pour permettre les imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from setup.logger_config import setup_logger

# Récupérer le nom du module
module_name = Path(__file__).stem
logger = setup_logger(module_name)

# Chemin du fichier dynamique vers le csv 
csv_path = (
    project_root
    / "data"
    / "raw"
    / "csvFile"
    / "bce_unemployment_rate_updated.csv"
)

if not csv_path.exists():
    raise FileNotFoundError(
        f" Le fichier csv à nettoyer est introuvable: {csv_path}"
    )
    
# Chemin du fichier de sortie pour les données nettoyées
output_csv_path = (
    project_root
    / "data"
    / "cleaned"
    / "unemployment_rate_cleaned_updated.csv"
)

# Créer le fichier de sortie et vérifier qu'il existe
output_csv_path.parent.mkdir(parents=True, exist_ok=True)


# Charger le fichier csv
df = pd.read_csv(
    csv_path,
    sep=",",
    encoding="utf-8-sig",
    engine="python"
)

print(f" liste de colonnes disponibles: {df.columns.to_list()}")
print(f" Nombre de lignes brutes: {len(df)}")

# Lister les colonnes necessaires pour le dataset
columns_needed=[
   "TIME_PERIOD",
    "OBS_VALUE", 
    "OBS_STATUS", 
    "TIME_FORMAT", 
    "TITLE"
]
# Identifier les colonnes manquantes
missing_columns = [
    col for col in columns_needed
    if col not in df.columns
]

# Afficher les colonnes manquantes
if missing_columns:
    raise ValueError(f"Les colonnes suivantes sont manquantesv: {missing_columns}")

# Créer uune copie independante du dataset réduit
df_unemployment = df[columns_needed].copy()

# Récupérer les métadonnées du dataset réduit
df_unemployment["TITLE"] = (
    "Unemployment rate, age 15 to 74, total"
)

df_unemployment["SOURCE_LABEL"] = "BCE"

""" Nétoyage des données"""
logger.info("Début du nettoyage des données sur le taux de chômage.")

# Conversion de la colonne "date" en format datetime et nettoyage des espaces
# le TIME_PERIOD est le format originale BCE
df_unemployment["TIME_PERIOD"] = df_unemployment["TIME_PERIOD"].astype(str).str.strip()

# le date est le format vraie date technique pour PostgreSQL
df_unemployment["date"] = pd.to_datetime(
    df_unemployment["TIME_PERIOD"],
    errors="coerce"
).dt.date

# Conversion de la colonne 'OBS_VALUE' en format numeric : Valeur numérique pour le taux de chômage, avec coercition des erreurs en NaN
df_unemployment["OBS_VALUE"] = pd.to_numeric(
    df_unemployment["OBS_VALUE"], 
    errors="coerce"
)

# Tri + export des données propres
df_unemployment= (
    df_unemployment
    .dropna(subset=["date", "OBS_VALUE"])
    .drop_duplicates(subset="date", keep="last")
    .sort_values("date")
    .reset_index(drop=True)
)

# controle avant export
print(f"nombre total de ligne après nettoyage: {len(df_unemployment)}")
print(f"Première date : {df_unemployment['date'].min()}")
print(f"Dernière date : {df_unemployment['date'].max()}")
print(f"Nombre de dates dupliquées :{df_unemployment.duplicated(subset='date').sum()}")

# Exporter le dataset nettoyé vers un fichier CSV
df_unemployment.to_csv(
    output_csv_path, 
    index=False,
    encoding="utf-8-sig"
)
logger.info(
    "Fichier BCE nettoyé et exporté."
    "Nonmbre de lignes nettoyées : %s", 
    len(df_unemployment)
)

