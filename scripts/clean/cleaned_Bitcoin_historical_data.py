import pandas as pd

df = pd.read_csv(
    "data/raw/csvFile/Bitcoin_14_05_2010_12_06_2025_historical_data_coinmarketcap.csv", 
    sep=";", 
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
# Conversion des colonnes  qui on les valeur temps en format datetime
df_bitcoin["timeOpen"] = pd.to_datetime(df_bitcoin["timeOpen"])
df_bitcoin["timeClose"] = pd.to_datetime(df_bitcoin["timeClose"])
df_bitcoin["timeHigh"] = pd.to_datetime(df_bitcoin["timeHigh"])
df_bitcoin["timeLow"] = pd.to_datetime(df_bitcoin["timeLow"])

# Conversion de la colonne 'OBS_VALUE' en format numeric
colomnes_numerics = ["timeLow", "open", "high","low","close", "volume", "marketCap"]
for col in colomnes_numerics:
    df_bitcoin[col] = pd.to_numeric(df_bitcoin[col], errors='coerce')
    
# Ajout de la date simplifiée (clé logique) 
df_bitcoin["date_bitcoin"] = df_bitcoin["timeOpen"].dt.date

# Tri des données propres
df_bitcoin = df_bitcoin.dropna().sort_values("date_bitcoin")

# Export des données propres
df_bitcoin.to_csv("data/cleaned/bitcoin_historical_cleaned.csv", index=False)
print("Fichier Bitcoin nettoyé et exporté.")