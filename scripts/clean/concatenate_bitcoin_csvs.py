"""
Script : concatenate_bitcoin_csvs.py
Projet : VolatiChainXplorerAI
Date : 2026-06-04

Description :
    Ce script concatène deux fichiers CSV Bitcoin :
    1. bitcoin_historical_cleaned.csv (2010-07-14 à 2025-06-12)
    2. bitcoin_historical_cleaned_13-06-2025_03-06-2026.csv (2025-06-13 à 2026-06-03)
    
    Il produit un fichier complet couvrant toute la période.

Usage :
    python scripts/clean/concatenate_bitcoin_csvs.py
"""

import pandas as pd
import sys
from pathlib import Path

# Définir les chemins des fichiers
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Fichier 1 : données historiques 2010-2025
csv_historical = project_root / "data" / "cleaned" / "bitcoin_historical_cleaned_14-07-2010_12-06-2025.csv"

# Fichier 2 : complément 2025-2026
csv_complement = project_root / "data" / "cleaned" / "bitcoin_historical_cleaned_13-06-2025_03-06-2026.csv"

# Fichier de sortie : fusion complète
csv_output = project_root / "data" / "cleaned" / "bitcoin_historical_cleaned_updated.csv"

print(" Chargement des fichiers CSV...")

# Charger les fichiers CSV
df_historical = pd.read_csv(
    csv_historical,
    sep=",",
    parse_dates=["date_bitcoin"],
    encoding="utf-8-sig",
    engine="python"
)
print(f"  Historique : {len(df_historical)} lignes")

df_complement = pd.read_csv(
    csv_complement,
    sep=",",
    parse_dates=["date_bitcoin"],
    encoding="utf-8-sig",
    engine="python"
)
print(f"  Complément : {len(df_complement)} lignes")

# Concaténer les DataFrames
df_combined = pd.concat([df_historical, df_complement], ignore_index=True)
print(f" Total : {len(df_combined)} lignes\n")

# Préparer les colonnes finales
df_combined["date"] = df_combined["date_bitcoin"]
use_columns = ["date", "open", "high", "low", "close", "volume", "marketCap"]
df_final = df_combined[use_columns].copy()

# Trier par date
df_final = df_final.sort_values("date").reset_index(drop=True)

# Vérifier les doublons
nb_doublons = df_final.duplicated(subset=["date"]).sum()
if nb_doublons > 0:
    print(f" {nb_doublons} doublons détectés - suppression...")
    df_final = df_final.drop_duplicates(subset=["date"], keep="first")
    print(f"  Lignes restantes : {len(df_final)}\n")
else:
    print("✓ Aucun doublon détecté\n")

# Exporter le DataFrame final
df_final.to_csv(csv_output, index=False, encoding="utf-8-sig")
print(f" Fichier exporté : {csv_output}")
print(f"   - Lignes finales : {len(df_final)}")
print(f"   - Date min       : {df_final['date'].min()}")
print(f"   - Date max       : {df_final['date'].max()}")