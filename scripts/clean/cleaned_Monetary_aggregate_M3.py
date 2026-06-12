import pandas as pd
import sys
from pathlib import Path

# Chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))


# Chemin du CSV
csv_path = project_root/"data"/"raw"/"csvFile"/"bce_Monetary_aggregate_M3_updated.csv"

# Chemin du fichier CVSV de sortie pour les données nettoyées
output_file = project_root /"data"/"cleaned"/"Monetary_aggregate_M3_cleaned_updated.csv"

df = pd.read_csv(csv_path,
                 sep=",",
                 encoding="utf-8-sig",
                 engine="python"
                )
print(df.head())

# Récupérer le TITLE et la source proprement du TITLE complete
title_compl = str(df.at[0, "TITLE_COMPL"]).split(",")
parts = [part.strip() for part in title_compl]
print(parts)

# Récupérer le TITLE
zone = parts[0].replace("(changing composition)", " ").strip()
print(zone)

indicator = parts[3].split("-")[1].strip()
print(indicator)

used_title = f"{zone} - {indicator}"
print(used_title)

# Récupérer la source proprement du TITLE complete
title_source = "API SDMX BCE"
print(title_source)

# Colonnes pertinantes pour le dataset
colomnes_names = ["TIME_PERIOD","OBS_VALUE", "OBS_STATUS", "TIME_FORMAT", "TITLE"]

# Dataset réduit
df_Monetary_aggregate_M3 = df[colomnes_names]
df_Monetary_aggregate_M3 = df_Monetary_aggregate_M3.copy()
print(df_Monetary_aggregate_M3.head())

# Le TITLE à utiliser dans le dataset réduit 
df_Monetary_aggregate_M3["TITLE"] = used_title

# Le label source à utiliser dans le dataset réduit 
df_Monetary_aggregate_M3["SOURCE_LABEL"] = title_source


""" Nétoyage des données"""
# Nettoyage de la colonne "TIME_PERIOD" : suppression des espaces superflus
df_Monetary_aggregate_M3["TIME_PERIOD"] = df_Monetary_aggregate_M3["TIME_PERIOD"].astype(str).str.strip()

# Conversion de la colonne "date" en format datetime
df_Monetary_aggregate_M3["date"] = pd.to_datetime(df_Monetary_aggregate_M3["TIME_PERIOD"],
                                                  errors="coerce"
                                                  ).dt.date
print(df_Monetary_aggregate_M3.head())

# Conversion de la colonne 'OBS_VALUE' en format numeric
df_Monetary_aggregate_M3['OBS_VALUE'] = pd.to_numeric(df_Monetary_aggregate_M3["OBS_VALUE"], 
                                                      errors= "coerce"
                                                      )
print(df_Monetary_aggregate_M3.head())

# Tri + export des données propres
df_Monetary_aggregate_M3= df_Monetary_aggregate_M3.dropna(subset= ["date", "OBS_VALUE"]).sort_values("date").reset_index(drop=True)
df_Monetary_aggregate_M3.to_csv(output_file, 
                                index=False
                                )
print("Fichier BCE nettoyé et exporté.")

