"""Script pour établir la connexion à la base de **données** VolatiChainXplorerAI_mongo."""

# Charger les bibliothèques nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pymongo import MongoClient
from dotenv import load_dotenv
from contextlib import contextmanager
from setup.logger_config import setup_logger
from pathlib import Path

# Mise en place d'un logger pour la connexion à la base de données 
name_file =os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(name_file)

# Charger les variables d'environnement
load_dotenv()

# Récupérer les variables du fichier .env
MONGO_USER=os.getenv("MONGO_USER")
MONGO_PASSWORD=os.getenv("MONGO_PASSWORD")
MONGO_DB=os.getenv("MONGO_DB")
MONGO_PORT=os.getenv("MONGO_PORT")


# Définition de l' URI de connexion à MongoDB
# Definir un delai d'expiration côté client à l'aide de l' option de connexion timeoutMS
URI: str = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:{MONGO_PORT}/{MONGO_DB}?authSource=admin&serverSelectionTimeoutMS=5000"

# Créer la connexion à mongoDB
client =MongoClient(URI)

# Mettre en place une foction permettant de gérer la session
@contextmanager
def get_mongodb():
   logger.info("Début de la connexion à la base de données à MONGODB.")
   
   # Connexion à la base de données MongoDB
   db = client[MONGO_DB]
  
   try:
    yield db
   except Exception as e:
      logger.error(f"Erreur de connexion à MONGODB :{e}")
      raise RuntimeError(
         " Connexion à MONGODB, échouée ! "
         "Cause probable : paramètres incorrects (.env), base éteinte ou réseau injoignable. "
         " Pensez à relancer le conteneur ou vérifier le fichier .env."
      ) from e
   finally:
      client.close()
      logger.info("Connexion MONGODB fermée avec succès.")

if __name__ == "__main__":
    with get_mongodb() as db:
        print("Connexion réussie!")
        print(f"Collections:", db.list_collection_names())