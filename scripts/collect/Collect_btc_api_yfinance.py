"""
Script pour collecter les données historiques du Bitcoin en utilisant yfinance
et les sauvegarder dans un fichier CSV.

"""
# Importation des bibliothèques nécessaires
import yfinance as yf


# Télécharger les données du Bitcoin en USD depuis 2013
btcData = yf.download("BTC-EUR", start="2009-01-01", end="2025-05-31", interval="1d")

# Afficher les premières lignes
print(btcData.head())

# Sauvegarder dans un fichier CSV pour traitement manuel
btcData.to_csv("data/raw/bitcoin_2014-09-17_2025-05-30-EURO.csv", index=True)

# Afficher un message de confirmation
print("Données sauvegardées dans bitcoin_2014-09-17_2025-05-30-EURO.csv")