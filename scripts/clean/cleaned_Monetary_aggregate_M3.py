import pandas as pd

df = pd.read_csv("data/raw/csvFile/bce_Monetary_aggregate_M3_download.csv")
print(df.head())

# Récupérer le TITLE
full_TITLE = df.at[0,"TITLE"]
print(full_TITLE)

# Tronquer proprement le TITLE
short_TITLE = full_TITLE.split(",")[0]
short_TITLE_strip = short_TITLE.replace("reported by MFIs", "").strip()
print(short_TITLE_strip)

# Colonnes pertinantes pour le dataset
colomnes_names = ["TIME_PERIOD","OBS_VALUE", "OBS_STATUS", "TIME_FORMAT", "TITLE"]

# Dataset réduit
df_Monetary_aggregate_M3 = df[colomnes_names]
print(df_Monetary_aggregate_M3.head())

# Le TITLE à utiliser dans le dataset réduit 
df_Monetary_aggregate_M3["TITLE"] = short_TITLE_strip
df_Monetary_aggregate_M3= df_Monetary_aggregate_M3.copy()

""" Nétoyage des données"""
# Conversion de la colonne 'TIME_PERIOD' en format datetime
df_Monetary_aggregate_M3['TIME_PERIOD'] = pd.to_datetime(df_Monetary_aggregate_M3['TIME_PERIOD'])
print(df_Monetary_aggregate_M3.head())

# Conversion de la colonne 'OBS_VALUE' en format numeric
df_Monetary_aggregate_M3['OBS_VALUE'] = pd.to_numeric(df_Monetary_aggregate_M3['OBS_VALUE'], errors='coerce')
print(df_Monetary_aggregate_M3.head())

# Tri + export des données propres
df_Monetary_aggregate_M3= df_Monetary_aggregate_M3.dropna().sort_values('TIME_PERIOD')
df_Monetary_aggregate_M3.to_csv("data/cleaned/Monetary_aggregate_M3_cleaned.csv", index=False)
print("Fichier BCE nettoyé et exporté.")

