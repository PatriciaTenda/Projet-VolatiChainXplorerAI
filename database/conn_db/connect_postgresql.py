"""
Script pour établir la connexion à la base de ddonnées VolatiChainXplorerAI_pg.

"""
# Charger les bibliothèques nécessaires

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from contextlib import contextmanager
import os
# Charger les variables d'environnement
load_dotenv()
# Récupérer les variables du fichier .env
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_DB=os.getenv("POSTGRES_DB")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT=os.getenv("POSTGRES_PORT")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")

# Définition de l' URL 
URL= f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Créer le engine de SQLAlchimy
engine = create_engine(URL)

# Créer un objet Base de SQLAlchimy
Base = declarative_base()

# Créer une session 
SessionLocal= sessionmaker(engine)

# Mettre en place une foction permettant de gérer la session
@contextmanager
def get_db():
   db = SessionLocal()
   try:
    yield db
   except Exception as e:
      print(f"Echec de connexion : {e}")
      raise
   finally:
      db.close()
   

if __name__ == "__main__":
    with get_db() as session:
       session.execute(text("SELECT 1"))
       print("Connexion réussie!")