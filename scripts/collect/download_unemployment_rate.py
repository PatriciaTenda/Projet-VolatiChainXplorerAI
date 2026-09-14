# scripts/collect/download_unemployment_rate.py

""" Script pour télécharger les taux de chômage depuis le site de la Banque Centrale Européenne (BCE).
    Ce script automatise la récupération des données au format CSV pour une utilisation ultérieure dans des analyses financières ou économiques.
"""
# Charger les bibliothèques nécessaires
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# Chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

# Chemin du fichier ".env"
env_path = project_root / ".env" 

# Chargement des variables d'environnement
load_dotenv(dotenv_path=env_path)

# Récupération du nom du module logger
from setup.logger_config import setup_logger

module_name = Path(__file__).stem
logger = setup_logger(module_name)

# Créer le le dossier qui contiendra le fichier CSV téléchargé
output_path = (
    project_root 
    / "data" 
    /"raw"
    /"csvFile"
    /"bce_unemployment_rate_updated.csv"
)
output_path.parent.mkdir(parents=True, exist_ok=True)

# Récuperer les variables
dataset_code = os.getenv("dataset_code_Unemployment")
serie_key = os.getenv("key_Unemployment")

# Vérification des variables
if not serie_key or not dataset_code:
    raise ValueError("Les variables d'environnement key_Unemployment et dataset_code_Unemployment sont requises.")

if "." not in serie_key:
    raise ValueError(
        "La clé de la série doit contenir un point ('.')"
        "pour séparer le préfixe et la clé du dataset."
    )
    
# Paramètres de l'URL
base = "https://data-api.ecb.europa.eu"
key = serie_key.split(".",1)[1]

# Construction de l'URL
# URL direct de la page où on va télécharger le fichier csv
url = f"{base}/service/data/{dataset_code}/{key}?format=csvdata" 
logger.info(f"URL de téléchargement : {url}")

def download_bce_unemployment_rate(
    url: str,
    filename: Path,
) -> None:
    """
    Télécharger le fichier CSV des taux de chômage.

    Args:
        url: URL du fichier CSV.
        filename: Chemin local du fichier de destination.

    Raises:
        requests.RequestException:
            Si la requête HTTP échoue.
        ValueError:
            Si le fichier reçu est vide.
    """    
    try:
        logger.info("Début du téléchargement des données des taux de chômage.")
        response = requests.get(
            url,
            timeout=30
        )
        response.raise_for_status()

        if not response.content:
            raise ValueError("Le fichier reçu est vide.")

        filename.write_bytes(response.content)
        logger.info(
            "Fichier téléchargé avec succes : %s",
            filename
        )
    except requests.RequestException as error:
        logger.error(
            "Erreur lors du téléchargement du fichier : %s",
            error
        )
        raise

if __name__ == "__main__":
    download_bce_unemployment_rate(url, output_path)
    
    import pandas as pd
    
    df = pd.read_csv(output_path)
    
    print("Clé :", df["KEY"].unique())
    print("Colonnes :", df.columns.tolist())
    print("Première période :", df["TIME_PERIOD"].min())
    print("Dernière période :", df["TIME_PERIOD"].max())
    print("Titre :", df["TITLE"].dropna().unique())
    print("Titre complet :", df["TITLE_COMPL"].dropna().unique())