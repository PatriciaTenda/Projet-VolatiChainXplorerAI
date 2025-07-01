import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from database.conn_db.connect_postgresql import SessionLocal
from database.postgres.models.users import Users
from sqlalchemy.orm import Session
from api.auths.jwt_handler import JWTHandler
from setup.logger_config import setup_logger

# Mise en place d'un logger pour le module
name_file = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(name_file)

def create_default_users():
    """
    Crée un ensemble d'utilisateurs par défaut (admin et utilisateurs de test)
    avec des mots de passe hachés, uniquement s'ils n'existent pas déjà.
    """
    logger.info("Création des utilisateurs par défaut")
    print("=" * 40)
         
    # Utilisateurs par défaut
    default_users = [
        {
            "email": "admin@volatichain.com",
            "name" :"Maxi VolatiChain",
            "password": "admin123",
            "role": "admin"
        },
        {
            "email": "user@volatichain.com", 
            "name" :"Triore VolatiChain",
            "password": "user123",
            "role": "user"
        },
        {
            "email": "jack@volatichain.com",
            "name" :"Emile VolatiChain",
            "password": "rose123",
            "role": "user"
        }
    ]
    
    db : Session = SessionLocal()
    try:
        for user_data in default_users:
            # Vérifier si l'utilisateur existe déjà
            existing = db.query(Users).filter(Users.email_user == user_data["email"]).first()
            if existing:
                logger.info(f"{user_data['email']} existe déjà, création ignorée.")
                continue
            
            # Créer l'utilisateur
            password_hash = JWTHandler.hash_password(user_data["password"])
            
            user = Users(
                name_user= user_data["name"],
                email_user=user_data["email"],
                hashed_password_user=password_hash,
                role_user=user_data["role"]
            )
            
            db.add(user)
            logger.info(f"Créé: {user_data['email']} ({user_data['role']})")
        
        db.commit()
        logger.info("Utilisateurs créés avec succès !")
     
        return True
        
    except Exception as e:
        logger.error(f" Erreur: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    create_default_users()