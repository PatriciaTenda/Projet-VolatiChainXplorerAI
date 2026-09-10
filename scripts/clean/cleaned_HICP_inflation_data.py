import sys
from pathlib import Path

import pandas as pd

# Chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Chemin du fichier CSV à nettoyer
csv_path = (
    project_root
    / "data"
    / "raw"
    / "csvFile"
    / "bce_HICP_Inflation_updated.csv"
)

# Chemin du fichier de sortie pour les données nettoyées
output_csv_path = (
    project_root
    / "data"
    / "cleaned"
    / "HICP_Inflation_cleaned_updated.csv"
)

#Créer le dossier de sortie et vérifier s'il n'existe pas
output_csv_path.parent.mkdir(parents=True, exist_ok=True)

if not csv_path.exists():
    raise FileNotFoundError(
        f"Le fichier CSV à nettoyer n'existe pas: {csv_path}"
    )
    
# Charger le fichier CSV
df = pd.read_csv(csv_path,
                 sep=",",
                 encoding="utf-8-sig",
                 engine= "python"
                )
print(f"Colonnes disponibles: {df.columns.tolist()}")
print(f"nombre total de ligne brute: {len(df)}")


# Colonnes nécessaires pour le dataset
columns_names = [
    "TIME_PERIOD",
    "OBS_VALUE", 
    "OBS_STATUS", 
    "TIME_FORMAT", 
    "TITLE"
]

# Vérivifier que les colonnes existes
missing_columns=[
    col for col in columns_names 
    if col not in df.columns
    
]
if missing_columns:
    raise ValueError(
        f"Les colonnes suivantes sont manquantes dans le fichiers CSV: {missing_columns}"
)
    
# Créer une copie indépendante du dataset reduit
df_HICP_Inflation = df[columns_names].copy()

# récupérer les métadonnées du dataset 
df_HICP_Inflation["SOURCE_LABEL"] = "ECB/Eurostat"

df_HICP_Inflation["TITLE"] = (
    "Euro area - HICP total - Annual inflation rate"
)

""" Nétoyage des données"""

# Nettoyage de la colonne "TIME_PERIOD" : suppression des espaces superflus
df_HICP_Inflation["TIME_PERIOD"] = (
    df_HICP_Inflation["TIME_PERIOD"]
    .astype(str)
    .str.strip()
)

# Conversion de la colonne "date" en format datetime
df_HICP_Inflation["date"] = pd.to_datetime(
    df_HICP_Inflation["TIME_PERIOD"],
    errors="coerce",
    ).dt.date

# Conversion de la colonne 'OBS_VALUE' en en nombre
df_HICP_Inflation["OBS_VALUE"] = pd.to_numeric(
    df_HICP_Inflation["OBS_VALUE"], 
    errors="coerce",
    )

# Tri + export des données propres
df_HICP_Inflation = (
    df_HICP_Inflation
    .dropna(subset = ["date", "OBS_VALUE"])
    .drop_duplicates(subset="date", keep="last")
    .sort_values("date")
    .reset_index(drop=True)
)

# controle avant export
print(f"nombre total de ligne après nettoyage: {len(df_HICP_Inflation)}")
print(f"Première date : {df_HICP_Inflation['date'].min()}")
print(f"Dernière date : {df_HICP_Inflation['date'].max()}")
print(f"Nombre de dates dupliquées :{df_HICP_Inflation.duplicated(subset='date').sum()}")

# Exporter le fichier nettoyé
df_HICP_Inflation.to_csv(
    output_csv_path,
    index=False,
    encoding="utf-8-sig",
)
print("Fichier BCE nettoyé et exporté.")

