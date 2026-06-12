import pandas as pd
import sys
from pathlib import Path

# Chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Chemin du fichier CSV
csv_path = project_root/"data"/"raw"/"csvFile"/"bce_HICP_Inflation_updated.csv"

# Chemin du fichier de sortie pour les données nettoyées
output_csv_path = project_root/"data"/"cleaned"/"HICP_Inflation_cleaned_updated.csv"

# Charger le fichier CSV
df = pd.read_csv(csv_path,
                 sep=",",
                 encoding="utf-8-sig",
                 engine= "python"
                )
print(df.head())


# Récupérer le TITLE
title_compl = str(df.at[0,"TITLE_COMPL"])
short_TITLE = title_compl.split("-")
zone = short_TITLE[0].split(" ", 1)[0].strip()
indicator = short_TITLE[1].strip()
used_title = f"{zone} - {indicator} - Inflation rate"
print(used_title)

# Récupérer la source proprement du TITLE complete
title_source = title_compl.split(",")[2]
print(title_source)

# Colonnes pertinantes pour le dataset
colomnes_names = ["TIME_PERIOD","OBS_VALUE", "OBS_STATUS", "TIME_FORMAT", "TITLE"]

# Dataset réduit
df_HICP_Inflation = df[colomnes_names]
print(df_HICP_Inflation.head())

# Le label source à utiliser dans le dataset réduit 
df_HICP_Inflation["SOURCE_LABEL"] = title_source
df_HICP_Inflation["TITLE"] = used_title
df_HICP_Inflation = df_HICP_Inflation.copy()

""" Nétoyage des données"""
# Nettoyage de la colonne "TIME_PERIOD" : suppression des espaces superflus
df_HICP_Inflation["TIME_PERIOD"] = df_HICP_Inflation["TIME_PERIOD"].astype(str).str.strip()

# Conversion de la colonne "date" en format datetime
df_HICP_Inflation["date"] = pd.to_datetime(
    df_HICP_Inflation["TIME_PERIOD"],
    errors="coerce"
    ).dt.date
print(df_HICP_Inflation.head())

# Conversion de la colonne 'OBS_VALUE' en format numeric
df_HICP_Inflation["OBS_VALUE"] = pd.to_numeric(
    df_HICP_Inflation["OBS_VALUE"], 
    errors="coerce"
    )
print(df_HICP_Inflation.head())

# Tri + export des données propres
df_HICP_Inflation = df_HICP_Inflation.dropna(subset = ["date", "OBS_VALUE"]).sort_values("date").reset_index(drop=True)
df_HICP_Inflation.to_csv(output_csv_path,
                          index=False
                    )
print("Fichier BCE nettoyé et exporté.")

