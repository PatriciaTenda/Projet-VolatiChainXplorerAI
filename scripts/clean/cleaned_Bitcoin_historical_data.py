import pandas as pd


import pandas as pd

# Liste des colonnes de dates dans ton fichier
date_cols = ["timeOpen", "timeClose", "timeHigh", "timeLow", "timestamp"]

df = pd.read_csv(
    "data/raw/csvFile/Bitcoin_14_05_2010_12_06_2025_historical_data_coinmarketcap.csv", 
    sep=";", 
    parse_dates=date_cols,         # Convertit automatiquement en datetime
    date_parser=pd.to_datetime,    # Utilise le parser standard (optionnel ici)
    encoding="utf-8-sig",    # pour gérer les caractères BOM
    engine="python"          # pour bien parser les séparateurs personnalisés
    )
 
print(df.head())

# Liste des colonnes du dataset
all_possibles_colomns = df.columns.str.strip() 
print(all_possibles_colomns)

# Colonnes pertinantes pour le dataset
col_names = ["timeOpen","timeClose","timeHigh","timeLow","open","high","low","close","volume","marketCap"]

# Vérification des colonnes existantes
existing_cols = [col for col in col_names if col in df.columns]
print(f"Colonnes existantes : {existing_cols}")

# Extraction du Dataset réduit
df_bitcoin = df[existing_cols].copy()
print(df_bitcoin.columns.tolist())
print(df_bitcoin.head())

""" Nétoyage des données"""
# Conversion de la colonne 'OBS_VALUE' en format numeric
colomnes_numerics = ["open", "high","low","close", "volume", "marketCap"]
for col in colomnes_numerics:
    df_bitcoin[col] = pd.to_numeric(df_bitcoin[col], errors='coerce')
    
# Ajout de la date simplifiée (clé logique) 
df_bitcoin["date_bitcoin"] = df_bitcoin["timeOpen"].dt.date
print(df_bitcoin["date_bitcoin"].dtypes)
# Tri des données propres
df_bitcoin = df_bitcoin.dropna().sort_values("date_bitcoin")

# Export des données propres
df_bitcoin.to_csv("data/cleaned/bitcoin_historical_cleaned.csv", index=False)
print("Fichier Bitcoin nettoyé et exporté.")