# scripts/collect/download_bce_mro.py
""" Script pour télécharger les taux directeurs depuis le site de la Banque Centrale Européenne (BCE).
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
    /"bce_mro_updated.csv"
)
output_path.parent.mkdir(parents=True, exist_ok=True)

# Récuperer les variables
dataset_code = os.getenv("dataset_code_mro")
serie_key = os.getenv("serie_key_mro")

# Vérification des variables
if not serie_key or not dataset_code:
    raise ValueError(
        "Les variables d'environnement SERIE_KEY_MRO et DATASET_CODE_MRO sont requises."
    )

if "." not in serie_key:
    raise ValueError(
        "La clé de la série doit contenir un point ('.')"
        "pour séparer le préfixe et la clé du dataset."
    )

# Paramètres de l'URL
base = "https://data-api.ecb.europa.eu"
key_mro = serie_key.split(".",1)[1]

# Construction de l'URL
# URL direct de la page où on va télécharger le fichier csv
url = f"{base}/service/data/{dataset_code}/{key_mro}?format=csvdata" 
logger.info(f"URL de téléchargement : {url}")

def download_bce_mro(url: str, filename: Path) -> None:
    """
        Télécharge le fichier CSV depuis l'URL spécifiée et l'enregistre localement.

        Args:
            url (str): L'URL du fichier CSV à télécharger.
            filename (Path): Le chemin local où le fichier sera enregistré.
        Raises:
            requests.RequestException:
            Si la requête HTTP échoue.
        ValueError:
            Si le fichier reçu est vide.
    """
    try:  
        logger.info("Début du téléchargement des données MRO.")
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
    download_bce_mro(url, output_path)