"""Script pour établir la connexion à la base de **données** VolatiChainXplorerAI_mongo."""

# Charger les bibliothèques nécessaires
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from pymongo import MongoClient
from dotenv import load_dotenv
from setup.logger_config import setup_logger


#----------------- Mise en place des variables d'environnementet du logger -----------------#
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


#-------------------- Connexion à la base de données --------------------#
# Définition de l' URI de connexion à MongoDB
# Definir un delai d'expiration côté client à l'aide de l' option de connexion timeoutMS
URI: str = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:{MONGO_PORT}/{MONGO_DB}?authSource=admin&serverSelectionTimeoutMS=5000"

# Créer la connexion à mongoDB
client: MongoClient = MongoClient(URI)

#------------------- Fonction pour gérer la session -------------------#
# Mettre en place une foction permettant de gérer la session
def get_mongodb():
   logger.info("Début de la connexion à la base de données à MONGODB.")
   
   # Connexion à la base de données MongoDB
   client : MongoClient = MongoClient(URI)
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

#-------------------- Test de connexion -------------------#
if __name__ == "__main__":
   db_gen = get_mongodb()
   try: 
        db = next(db_gen)
        db.command("ping")
        print("Serveur mongo joignable !")

        
        print("Collections:", db.list_collection_names())
        print("Authentification réussie.")
   except Exception as e:
         logger.error(f"Erreur lors du test de connexion à MONGODB : {e}")
         print(f"Erreur : {e}")
   finally:
      db_gen.close()