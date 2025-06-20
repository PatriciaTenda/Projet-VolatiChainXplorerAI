import pandas as pd

df = pd.read_csv("data/raw/csvFile/bce_HICP_Inflation_download.csv")
print(df.head())

# Récupérer le TITLE
full_TITLE = df.at[0,"TITLE"]
print(full_TITLE)

# Récupérer la source proprement du TITLE complete
TITLE_complet = df.at[0, "TITLE_COMPL"].split(",")[2]
print(TITLE_complet)

# Colonnes pertinantes pour le dataset
colomnes_names = ["TIME_PERIOD","OBS_VALUE", "OBS_STATUS", "TIME_FORMAT", "TITLE"]

# Dataset réduit
df_HICP_Inflation = df[colomnes_names]
print(df_HICP_Inflation.head())

# Le label source à utiliser dans le dataset réduit 
df_HICP_Inflation["SOURCE_LABEL"] = TITLE_complet
df_HICP_Inflation = df_HICP_Inflation.copy()

""" Nétoyage des données"""
# Conversion de la colonne 'TIME_PERIOD' en format datetime
df_HICP_Inflation['TIME_PERIOD'] = pd.to_datetime(df_HICP_Inflation['TIME_PERIOD'])
print(df_HICP_Inflation.head())

# Conversion de la colonne 'OBS_VALUE' en format numeric
df_HICP_Inflation['OBS_VALUE'] = pd.to_numeric(df_HICP_Inflation['OBS_VALUE'], errors='coerce')
print(df_HICP_Inflation.head())

# Tri + export des données propres
df_HICP_Inflation = df_HICP_Inflation.dropna().sort_values('TIME_PERIOD')
df_HICP_Inflation.to_csv("data/cleaned/HICP_Inflation_cleaned.csv", index=False)
print("Fichier BCE nettoyé et exporté.")

