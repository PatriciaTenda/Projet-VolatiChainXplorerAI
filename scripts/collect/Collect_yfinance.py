"""
Script pour collecter les données historiques du Bitcoin en utilisant yfinance
et les sauvegarder dans un fichier CSV.

"""
# Importation des bibliothèques nécessaires
import yfinance as yf


# Télécharger les données du Bitcoin en USD depuis 2013
btcData = yf.download("BTC-EUR", start="2018-01-01", end="2024-12-31", interval="1d")

# Afficher les premières lignes
print(btcData.head())

# Sauvegarder dans un fichier CSV pour traitement manuel
btcData.to_csv("data/raw/btc_historical_data.csv", index=True)

# Afficher un message de confirmation
print("Données sauvegardées dans btc_historical_data.csv")