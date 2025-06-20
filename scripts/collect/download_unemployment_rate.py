# scripts/collect/download_bce_mro.py
""" Script pour télécharger les taux de chômage depuis le site de la Banque Centrale Européenne (BCE).
    Ce script automatise la récupération des données au format CSV pour une utilisation ultérieure dans des analyses financières ou économiques.
"""
# Charger les bibliothèques nécessaires
import requests
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Récuperer les variables
dataset_code = os.getenv("dataset_code_Unemployment")
print(dataset_code)
serie_key = os.getenv("key_Unemployment")
# Vérification des variables
if not serie_key or not dataset_code:
    raise ValueError("Les variables d'environnement DATA_SERIE_KEY et DATA_DATASET_CODE sont requises.")

# Paramètres de l'URL
base = "https://data-api.ecb.europa.eu"
data_dataset_code = dataset_code
key = serie_key.split(".",1)[1]

# Construction de l'URL
default_url = f"{base}/service/data/{data_dataset_code}/{key}?format=csvdata" # URL direct de la page où on va télécharger le fichier csv
print(default_url)
# Nom du fichier csv
default_filename = "Data/raw/csvFile/bce_unemployment_rate_download.csv"

os.makedirs(os.path.dirname(default_filename), exist_ok = True)

def download_bce_HICP_Inflation(url, filename):
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"fichier téléchargé avec succes : {filename}")
    else:
        response.raise_for_status() # Remonte une erreur HTTP

if __name__ == "__main__":
    download_bce_HICP_Inflation(default_url, default_filename)