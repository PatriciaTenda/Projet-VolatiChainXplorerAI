"""
Script pour collecter les données historiques du Bitcoin en utilisant yfinance
et les sauvegarder dans un fichier CSV.

"""
# Charger les bibliothèques nécessaires
from pycoingecko import CoinGeckoAPI
import pandas as pd

# Charger l'API de CoinGecko
cg = CoinGeckoAPI()

# Extraction des données du Bitcoin en USD pour les 365 derniers jours
data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days='365', interval='daily')

# Convertir les données en DataFrame
df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
df = df[['date', 'price']].sort_values('date')

# Enregistrer dans un fichier CSV dans le dossier data/raw
df.to_csv("data/raw/btc_prices_coingecko.csv", index=False)
print("Données enregistrées avec pycoingecko")