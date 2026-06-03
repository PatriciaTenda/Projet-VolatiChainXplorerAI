"""Script pour établir la connexion à la base de **données** VolatiChainXplorerAI_pg."""

# Charger les bibliothèques nécessaires
import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from setup.logger_config import setup_logger


#----------------- Mise en place des variables d'environnementet du logger -----------------#
# Mise en place d'un logger pour la connexion à la base de données postgresql
logger = setup_logger("connect_postgresql")

# Charger les variables d'environnement
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

# Récupérer les variables du fichier .env
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_DB=os.getenv("POSTGRES_DB")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT=os.getenv("POSTGRES_PORT")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")

#----------------- Connexion à la base de données -----------------#
# Définition de l' URL 
URL: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Créer le engine de SQLAlchimy
engine = create_engine(URL)

# Créer un objet Base de SQLAlchimy
Base = declarative_base()

# Créer une session 
SessionLocal= sessionmaker(bind=engine, autoflush=False, autocommit=False)

#------------------- Fonction pour gérer la session -------------------#
# Mettre en place une fonction permettant de gérer la session

def get_db():
   logger.info("Début de connexion à la base de données postgresql.")
   db: Session= SessionLocal()
   try:
        yield db
   except Exception as e:
        logger.error(f"Erreur dans l'utilisation de la session PostgreSQL : {e}")
        raise  # on relance pour ne pas masquer les exceptions métier
   finally:
        db.close()
        logger.info("Connexion PostgreSQL fermée avec succès.")


#-------------------- Test de connexion -------------------#
if __name__ == "__main__":
    """Tester la connexion à la base de données"""
    db = get_db()
    try:
        session = next(db)
        session.execute(text("SELECT 1"))
        print("Connexion réussie!")
    except Exception as e:
        logger.error(f"Erreur lors du test de connexion : {e}")
        print(f"Erreur : {e}")
    finally:
        db.close()
