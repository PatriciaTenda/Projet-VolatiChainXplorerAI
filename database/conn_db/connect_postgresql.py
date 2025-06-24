"""Script pour établir la connexion à la base de **données** VolatiChainXplorerAI_pg."""

# Charger les bibliothèques nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from contextlib import contextmanager
from setup.logger_config import setup_logger

# Mise en place d'un logger pour la connexion à la base de données postgresql
logger = setup_logger("connect_postgresql")

# Charger les variables d'environnement
load_dotenv()

# Récupérer les variables du fichier .env
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_DB=os.getenv("POSTGRES_DB")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT=os.getenv("POSTGRES_PORT")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")

# Définition de l' URL 
URL: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Créer le engine de SQLAlchimy
engine = create_engine(URL)

# Créer un objet Base de SQLAlchimy
Base = declarative_base()

# Créer une session 
SessionLocal= sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Mettre en place une foction permettant de gérer la session
#@contextmanager
def get_db():
   logger.info("Début de la connexion à la base de données postgresql.")
   db: Session= SessionLocal()
   try:
      yield db
   except Exception as e:
      logger.error(f"Erreur de connexion à PostgreSQL :{e}")
      raise RuntimeError(
         " Connexion à PostgreSQL échouée ! "
         "Cause probable : paramètres incorrects (.env), base éteinte ou réseau injoignable. "
         " Pensez à relancer le conteneur ou vérifier le fichier .env."
      ) from e
   finally:
      db.close()
      logger.info("Connexion PostgreSQL fermée avec succès.")

if __name__ == "__main__":
    """Tester la connexion à la base de données"""
      # Obtenir manuellement la session à partir du générateur
    db_gen = get_db()  # get_db() est un générateur maintenant
    session = next(db_gen)  # on "entre" dans le yield

    try:
        session.execute(text("SELECT 1"))
        print("Connexion réussie!")
    finally:
        # on "ferme" la session comme FastAPI le ferait après le yield
        try:
            next(db_gen)
        except StopIteration:
            pass
#print((type(db_gen)))