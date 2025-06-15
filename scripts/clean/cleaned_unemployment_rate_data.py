import pandas as pd

df = pd.read_csv("data/raw/csvFile/bce_unemployment_rate_download.csv")
print(df.head())

# Récupérer le TITLE
full_TITLE = df.at[0,"TITLE"]
print(full_TITLE)

# Tronquer proprement le TITLE
short_TITLE = full_TITLE.split("-")[1]
print(short_TITLE)

# Colonnes pertinantes pour le dataset
colomnes_names = ["TIME_PERIOD","OBS_VALUE", "OBS_STATUS", "TIME_FORMAT", "TITLE"]

# Dataset réduit
df_unemployment_rate = df[colomnes_names]
print(df_unemployment_rate.head())

# Le TITLE à utiliser dans le dataset réduit 
df_unemployment_rate["TITLE"] = short_TITLE
df_unemployment_rate= df_unemployment_rate.copy()

""" Nétoyage des données"""
# Conversion de la colonne 'TIME_PERIOD' en format datetime
df_unemployment_rate['TIME_PERIOD'] = pd.to_datetime(df_unemployment_rate['TIME_PERIOD'])
print(df_unemployment_rate.head())

# Conversion de la colonne 'OBS_VALUE' en format numeric
df_unemployment_rate['OBS_VALUE'] = pd.to_numeric(df_unemployment_rate['OBS_VALUE'], errors='coerce')
print(df_unemployment_rate.head())

# Tri + export des données propres
df_unemployment_rate= df_unemployment_rate.dropna().sort_values('TIME_PERIOD')
df_unemployment_rate.to_csv("data/cleaned/unemployment_rate_cleaned.csv", index=False)
print("Fichier BCE nettoyé et exporté.")

