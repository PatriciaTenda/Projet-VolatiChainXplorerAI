"""Ce script permet de mettre en place un logger pour journaliser les opérations"""

# Charger les librairies nécessaires
import logging
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Récupérer les variables d'environement du fichier .env
LOG = os.getenv("LOG")
LOG_MYLIB= os.getenv("LOG_MYLIB")

# Fonction pour configurer un logger
def setup_logger(name:str, level_env: str = "LOG")-> logging.Logger:
    # Charger la variable d'environnement level_env du fichier .env
    level = os.getenv(level_env, "INFO")

    # Mise en place d'un logger avec le nom fourni
    logger = logging.getLogger(name)

    # Definir le niveau du logger( DEBUG, WARNING, INFO, etc.)
    logger.setLevel(getattr(logging, level, logging.INFO))

    # Mettre en place un handlers et s'assurer de ne pas ajouter plusieurs handlers à la fois
    if not logger.handlers:
        # Definir le dossier des logs
        os.makedirs("data/logs", exist_ok=True)

        # Créer un handler de type FileHandler pour enregister les logs dans un fichier
        handler = logging.FileHandler(f"data/logs/{name}.log", encoding="utf-8")

        # Définir le format clair des logs : Date - niveau - nom du module - message
        formatter = logging.Formatter("%(asctime)s[%(levelname)s] %(name)s : %(message)s") # name c'est le nom du module
        handler.setFormatter(formatter)

        # Ajout du handler au logger
        logger.addHandler(handler)  
    
    return logger 
