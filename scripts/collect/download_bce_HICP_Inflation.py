# scripts/collect/download_bce_HICP_Inflation.py

"""
    Télécharger les données d'inflation,
    depuis l'API de la Banque Centrale Européenne (BCE).
    
    Le fichier CSV sera utilisé pour une analyse ultérieure 
    pour les analyses financières et économiques.
"""
# Charger les bibliothèques nécessaires
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

#definir le chemin du projet
project_root = Path(__file__).resolve().parents[2]

# Ajouter la racine du projet au chemin de recherche de modules Python
sys.path.insert(0,str(project_root))

from setup.logger_config import setup_logger

# Récupérer le nom du module
name_module= Path(__file__).stem

# Configurer le logger pour ce module
logger = setup_logger(name_module)

# definir le chemin du fichier de configuration .env
path_env = project_root / ".env"

# Chargement des variables d'environnement
load_dotenv(dotenv_path=path_env)

#Chemin indépendent du dossier d'exécution
output_path = (
    project_root
    / "Data" 
    / "raw" 
    / "csvFile"
    / "bce_HICP_Inflation_updated.csv"
)

# Créer le dossier s'il n'existe pas
output_path.parent.mkdir(parents=True, exist_ok=True)

# Récuperer les variables
dataset_code = os.getenv("dataset_code_HICP")
serie_key = os.getenv("key_HICP_V2")

# Vérification des variables
if not serie_key or not dataset_code:
    raise ValueError(
        "Les variables d'environnement key_HICP_V2 et dataset_code_HICP sont requises."
    )

if "." not in serie_key:
    raise ValueError(
        "La clé de la série doit contenir un point ('.')"
        "pour séparer le préfixe et la clé du dataset."
    )

# Paramètres de l'URL
base = "https://data-api.ecb.europa.eu"
data_dataset_code = dataset_code
key = serie_key.split(".",1)[1]

# Construction de l'URL
# URL direct de la page où on va télécharger le fichier csv
default_url = (
    f"{base}/service/data/{data_dataset_code}/{key}" 
    "?format=csvdata" 
)
logger.info(f"URL de téléchargement : {default_url}")

def download_bce_HICP_Inflation(url: str, filename: Path) -> None:
    """
    Téléchargement du fichier de l'inflation HICP depuis la BCE.
    Args:
        url (str): L'URL du fichier CSV à télécharger.
        filename (Path): Le chemin local où enregistrer le fichier téléchargé.
    """
    try:
        logger.info("Téléchargement des données d'inflation HICP depuis la BCE.")
        response = requests.get(url, timeout=30)
        response.raise_for_status() # Vérifie si la requête a échoué avant de continuer et remonte une erreur HTTP
        
        filename.write_bytes(response.content)
        logger.info(f"fichier téléchargé avec succès et enregistré à : {filename}")
        
    except requests.RequestException as error:
        logger.error(f"Erreur du téléchargement du fichier : {error}")
        raise

if __name__ == "__main__":
    download_bce_HICP_Inflation(default_url, output_path)