import pandas as pd

df = pd.read_csv("Data/raw/csvFile/bce_mro.csv")
print(df.head())

# Récupérer le TITLE
full_TITLE = df.at[0,"TITLE"]
print(full_TITLE)

# Tronquer proprement le TITLE
short_TITLE = full_TITLE.split("-")[0]
print(short_TITLE)

# Colonnes pertinantes pour le dataset
colomnes_names = ["TIME_PERIOD","OBS_VALUE", "OBS_STATUS", "TIME_FORMAT", "TITLE"]

# Dataset réduit
df_MRO = df[colomnes_names]
print(df_MRO.head())

# Le TITLE à utiliser dans le dataset réduit 
df_MRO["TITLE"] = short_TITLE

# Récupérer la source proprement du TITLE complete
TITLE_complet = df.at[0, "TITLE_COMPL"].split(",")[1]
df_MRO["SOURCE_LABEL"] = TITLE_complet

df_MRO = df_MRO.copy()


""" Nétoyage des données"""
# Conversion de la colonne 'TIME_PERIOD' en format datetime
df_MRO['TIME_PERIOD'] = pd.to_datetime(df_MRO['TIME_PERIOD'])
print(df_MRO.head())

# Conversion de la colonne 'OBS_VALUE' en format numeric
df_MRO['OBS_VALUE'] = pd.to_numeric(df_MRO['OBS_VALUE'], errors='coerce')
print(df_MRO.head())

# Tri + export des données propres
df_MRO = df_MRO.dropna().sort_values('TIME_PERIOD')
df_MRO.to_csv("data/cleaned/bce_mro_cleaned.csv", index=False)

print("Fichier BCE nettoyé et exporté.")

