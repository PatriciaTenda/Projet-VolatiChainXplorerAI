import pandas as pd
import sys
from pathlib import Path

# Chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Chemin du CSV
csv_path = project_root /"data"/"raw"/"csvFile"/"bce_mro_updated.csv"

# Chemin du fichier CSV de sortie pour les données nettoyées
output_file = project_root / "data"/"cleaned"/"bce_mro_cleaned_updated.csv"

# Charger le fichier CSV
df = pd.read_csv(csv_path,
                 sep=",",
                 encoding="utf-8-sig",
                 engine="python")
print(df.head())

# Récupérer le TITLE et la source proprement du TITLE complete
full_TITLE = str(df.at[0, "TITLE_COMPL"])
parts = [part.strip() for part in full_TITLE.split(",")]
print(parts)

# Tronquer proprement le TITLE
part_0 = parts[0].split("-", -1)
zone = part_0[0].replace("(changing composition)", " ").strip()
indicator = part_0[1].strip() 
used_title = f"{zone} - {indicator} - MRO"
source_title = parts[1].replace("provided by", " ").strip()
print(used_title,"====", source_title)

# Colonnes pertinentes pour le dataset réduit
colomnes_names = ["TIME_PERIOD","OBS_VALUE", "OBS_STATUS", "TIME_FORMAT", "TITLE"]

# Dataset réduit
df_MRO = df[colomnes_names]
df_MRO = df_MRO.copy()
print(df_MRO.head())

# Le TITLE à utiliser dans le dataset réduit 
df_MRO["TITLE"] = used_title

# Récupérer la source proprement du TITLE complete
df_MRO["SOURCE_LABEL"] = source_title




""" Nétoyage des données"""
# Nettoyage de la colonne "TIME_PERIOD" et suppressions des espaces
df_MRO["TIME_PERIOD"] = df_MRO["TIME_PERIOD"].astype(str).str.strip()

# Conversion de la colonne "date" en format datetime
df_MRO["date"] = pd.to_datetime(df_MRO["TIME_PERIOD"],
                                errors="coerce"
                                ).dt.date
print(df_MRO.head())

# Conversion de la colonne 'OBS_VALUE' en format numeric
df_MRO['OBS_VALUE'] = pd.to_numeric(df_MRO['OBS_VALUE'], 
                                    errors='coerce'
                )
print(df_MRO.head())

# Tri + export des données propres
df_MRO = df_MRO.dropna(subset=["date", "OBS_VALUE"]).sort_values("date").reset_index(drop=True)
df_MRO.to_csv(output_file,
              index=False
            )

print("Fichier BCE nettoyé et exporté.")

