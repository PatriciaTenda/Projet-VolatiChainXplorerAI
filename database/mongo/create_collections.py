"""
Script : create_collections.py
Projet : VolatiChainXplorerAI
Date : 2025-06-20

Description :
    Ce script initialise les collections nécessaires dans la base de données MongoDB
    utilisée pour stocker les données du projet VolatichainXplorerAI.

Fonctionnalités :
    - Vérifie l'existence des collections
    - Crée les collections manquantes

Collections Mongo concernées :
    - articles
    - tweets
    - logs

Pré-requis :
    - Fichier .env correctement configuré
    - Conteneur MongoDB actif
    - Connexion valide à la base VolatichainXplorerAI_mongo

Usage :
    python create_collections.py
"""
# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pymongo import MongoClient
from dotenv import load_dotenv
from setup.logger_config import setup_logger
from typing import Dict

# Mise en place d'un logger pour le module de création des collections
name_file =os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(name_file)

# Charger les variables d'environnement
load_dotenv()

# Récupérer les variables d'environnement du fichier .env
MONGO_USER=os.getenv("MONGO_USER")
MONGO_PASSWORD=os.getenv("MONGO_PASSWORD")
MONGO_DB=os.getenv("MONGO_DB")
MONGO_PORT=os.getenv("MONGO_PORT")

# Définition de l' URI de connexion à MongoDB
# Definir un delai d'expiration côté client à l'aide de l' option de connexion timeoutMS
URI: str = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:{MONGO_PORT}/{MONGO_DB}?authSource=admin&serverSelectionTimeoutMS=5000"

# Fonction de créaton des collections dans la base de données VolatichainXplorerAI_mongo
def create_collections(uri: str, name_db, collections_name: list[str])->None:
    """Crée les collections nécessaires dans la base de données MongoDB spécifiée,
    si elles n'existent pas déjà.

    Paramètres :
        uri (str) : URI de connexion MongoDB.
        name_db (str) : Nom de la base de données MongoDB.
    """
    try :
        # Créer la connexion à mongoDB
        client =MongoClient(uri)

        # Etablir la connexion à la base de données
        db = client[name_db] 

        for col_name in collections_name:

            if col_name not in db.list_collection_names():
                db.create_collection(col_name)
                logger.info(f"Collection '{col_name}' créée.")
            else:
                logger.info(f"Collection '{col_name}' existe déjà.")
    except Exception as e :
        logger.error(f" Erreur lors de la création des collections : {e}")
        raise
    finally:
            client.close()
    


if __name__ == "__main__":
     
    # Vérifier si la collection à créer est déja existante, sinon créer  
    collections_name = ["articles_financiers", "logs", "tweets"]
    create_collections(URI, MONGO_DB,collections_name=collections_name)
    print("Créations éffectuées avec succès")