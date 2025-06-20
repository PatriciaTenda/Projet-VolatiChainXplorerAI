"""
Script : python injection_logs.py
Projet : VolatichainXplorerAI
Date : 2025-06-20

Description :
    Ce script insère automatiquement tous les informations de journalisations des scripts
    depuis des fichiers .log dans la collection MongoDB "logs".

Usage :
    python injection_logs.py
"""
# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pymongo import MongoClient
from dotenv import load_dotenv
from setup.logger_config import setup_logger



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

# Dossier contenant les logs
logs_dir = "data/logs"

def insert_logs(name_db: str, uri: str, name_collection: str):
    # Vérifier sur les articles existes
    if not os.path.exists(logs_dir):
        logger.error(f" Dossier introuvable : {logs_dir}")
        return
    
    # Connexion à la base de donnée
    client = MongoClient(uri)
    db = client[name_db]
    # Connexion à la collection souhaitée
    collection=db[name_collection]

    inserted = 0
    for filename in os.listdir(logs_dir):
        if filename.endswith(".log"):
            file_path = os.path.join(logs_dir,filename)
            try:
                # Charger les fichiers json depuis data/raw/articles_financiers
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.read()
                    data = [{"filename": filename,
                              "line": lines.strip()}
                              for line in lines if lines.strip()]
                    
                # Si le fichier contient une liste d'articles
                if isinstance(data, list):
                    result = collection.insert_many(data)
                    inserted+=len(result.inserted_ids)
                else:
                    result = collection.insert_one(data)
                    inserted+=1
                logger.info(f"Données insérées depuis {filename}")
            except Exception as e :
                logger.error(f"Erreur lors de l'insertion du fichier {filename} : {e}")
    
    client.close( )
    logger.info(f"Total des documents insérés : {inserted}")

if __name__ == "__main__":
    # Insérer les documents dans les collections respectives
    collection_name = "logs"
    insert_logs(MONGO_DB, URI, collection_name)
    print("Insertions complètes avec succès")