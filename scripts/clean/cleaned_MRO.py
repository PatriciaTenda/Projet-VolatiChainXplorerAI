"""
Nettoyage et préparation des données sur le taux des opérations principales de refinancement (MRO).
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
    / "bce_MRO_updated.csv"
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
    / "bce_mro_cleaned_updated.csv"
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
df_mro = df[columns_needed].copy()

# Récupérer les métadonnées du dataset réduit
df_mro["TITLE"] = (
    "Main Refinancing Operations (MRO) rate"
)

df_mro["SOURCE_LABEL"] = "BCE/Eurostat"

""" Nétoyage des données"""
# Conversion de la colonne "date" en format datetime et nettoyage des espaces
# le TIME_PERIOD est le format originale BCE
df_mro["TIME_PERIOD"] = df_mro["TIME_PERIOD"].astype(str).str.strip()

# le date est le format vraie date technique pour PostgreSQL
df_mro["date"] = pd.to_datetime(
    df_mro["TIME_PERIOD"],
    errors="coerce"
).dt.date

# Conversion de la colonne 'OBS_VALUE' en format numeric : Valeur numérique pour le taux de chômage, avec coercition des erreurs en NaN
df_mro["OBS_VALUE"] = pd.to_numeric(
    df_mro["OBS_VALUE"], 
    errors="coerce"
)

# Tri + export des données propres
df_mro= (
    df_mro
    .dropna(subset=["date", "OBS_VALUE"])
    .drop_duplicates(subset="date", keep="last")
    .sort_values("date")
    .reset_index(drop=True)
)

# controle avant export
print(f"nombre total de ligne après nettoyage: {len(df_mro)}")
print(f"Première date : {df_mro['date'].min()}")
print(f"Dernière date : {df_mro['date'].max()}")
print(f"Nombre de dates dupliquées :{df_mro.duplicated(subset='date').sum()}")

# Exporter le dataset nettoyé vers un fichier CSV
df_mro.to_csv(
    output_csv_path, 
    index=False,
    encoding="utf-8-sig"
)
logger.info(
    "Fichier MRO nettoyé et exporté."
    "Nombre de lignes nettoyées : %s", 
    len(df_mro)
)

