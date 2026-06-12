import pandas as pd
import sys
from pathlib import Path

path_root = Path(__file__).resolve().parents[2]
print(path_root)
sys.path.insert(0, str(path_root))
path_csv = path_root / "data" / "raw" / "csvFile" / "Bitcoin_13_06_2025-03_06_2026_historical_data_coinmarketcap.csv"

# Liste des colonnes de dates dans ton fichier
date_cols = ["timeOpen", "timeClose", "timeHigh", "timeLow", "timestamp"]

df = pd.read_csv(
                path_csv, 
                sep=";", 
                parse_dates=date_cols,         # Convertit automatiquement en datetime
                encoding="utf-8-sig",          # pour gérer les caractères BOM
                engine="python"                # pour bien parser les séparateurs personnalisés
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

# 
df_bitcoin = df_bitcoin[df_bitcoin["date_bitcoin"] >= pd.to_datetime("2025-06-13").date()]
# Export des données propres
# df_bitcoin.to_csv("data/cleaned/bitcoin_historical_cleaned.csv", index=False)
df_bitcoin.to_csv("data/cleaned/bitcoin_historical_cleaned_13-06-2025_03-06-2026.csv", index=False)
print("Fichier Bitcoin nettoyé et exporté.")