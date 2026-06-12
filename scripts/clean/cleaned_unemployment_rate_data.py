import sys
import pandas as pd
from pathlib import Path

# Ajouter le dossier racine du projet au PYTHONPATH pour permettre les imports
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Chemin du fichier dynamique vers le csv 
csv_path = project_root/"data"/"raw"/"csvFile"/"bce_unemployment_rate_updated.csv"

# Chemin du fichier de sortie pour les données nettoyées
output_csv_path = project_root/"data"/"cleaned"/"unemployment_rate_cleaned_updated.csv"

# Charger le fichier csv
df = pd.read_csv(csv_path,
                 sep=",",
                 encoding="utf-8-sig",
                 engine="python")
print(df.head())

# Récupérer les métadonnées depuis TITLE_COMPL et les préparer pour le dataset réduit
full_TITLE = str(df.at[0,"TITLE_COMPL"])
title_parts = [part.strip() for part in full_TITLE.split(";")]
print(title_parts)

# Récupérer le short TITLE  proprement du TITLE_COMPL
short_TITLE = title_parts[2]
print(short_TITLE)

# Récupérer la source proprement du TITLE_COMPL
TITLE_complet = title_parts[1]
print(TITLE_complet)

# Colonnes pertinantes pour le dataset
colomnes_names = ["TIME_PERIOD","OBS_VALUE", "OBS_STATUS", "TIME_FORMAT", "TITLE"]

# Dataset réduit
df_unemployment_rate = df[colomnes_names]
df_unemployment_rate= df_unemployment_rate.copy()
print(df_unemployment_rate.head())

# Méthadonnées propres pour le dataset reduit : title et source proprement extraites du TITLE_COMPL 
df_unemployment_rate["TITLE"] = short_TITLE
df_unemployment_rate["SOURCE_LABEL"] = TITLE_complet


""" Nétoyage des données"""
# Conversion de la colonne "date" en format datetime et nettoyage des espaces
# le TIME_PERIOD est le format originale BCE
df_unemployment_rate["TIME_PERIOD"] = df_unemployment_rate["TIME_PERIOD"].astype(str).str.strip()

# le date est le format vraie date technique pour PostgreSQL
df_unemployment_rate["date"] = pd.to_datetime(
    df_unemployment_rate["TIME_PERIOD"],
    errors="coerce"
).dt.date

print(df_unemployment_rate.head())

# Conversion de la colonne 'OBS_VALUE' en format numeric : Valeur numérique pour le taux de chômage, avec coercition des erreurs en NaN
df_unemployment_rate["OBS_VALUE"] = pd.to_numeric(
    df_unemployment_rate["OBS_VALUE"], 
    errors="coerce"
)
print(df_unemployment_rate.head())

# Tri + export des données propres
df_unemployment_rate= df_unemployment_rate.dropna(subset=["date", "OBS_VALUE"]).sort_values("date").reset_index(drop=True)
df_unemployment_rate.to_csv(output_csv_path, index=False)
print("Fichier BCE nettoyé et exporté.")

