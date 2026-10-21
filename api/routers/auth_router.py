# Chargement des librairies nécessaires
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.auths.auth_services import AuthService
from api.auths.dependencies import get_current_active_user, require_admin
from api.exceptions.user_exceptions import ValidationError
from api.schemas.reponse import success_response
from api.schemas.users import UserCreate, UserLogin
from database.conn_db.connect_postgresql import get_db
from database.postgres.models.users import Users
from setup.logger_config import setup_logger

# Mise en place du logger pour ce fichier
name_file = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(name_file)

# Création du routeur FastAPI
router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/register")
def register(user_data: UserCreate, db: Annotated[Session, Depends(get_db)]):
    """Créer un nouveau compte utilisateur"""
    try:
        logger.info(f"Tentative d'inscription pour l'email : {user_data.email}")
        result = AuthService.create_user(db, user_data)
        logger.info(f"Utilisateur créé avec succès : {user_data.email}")
        return result
    except ValidationError as e:
        logger.error(f"Erreur de validation lors de l'inscription : {e.message}")
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.exception("Erreur inattendue lors de l'inscription")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def login(login_data: UserLogin, db: Annotated[Session, Depends(get_db)]):
    """Se connecter et obtenir un token JWT"""
    try:
        logger.info(f"Tentative de connexion pour l'email : {login_data.email}")
        result = AuthService.login(db, login_data)
        logger.info(f"Connexion réussie pour : {login_data.email}")
        return result
    except ValidationError as e:
        logger.error(f"Échec de la connexion (validation) : {e.message}")
        raise HTTPException(status_code=401, detail=e.message)
    except Exception as e:
        logger.exception("Erreur inattendue lors de la connexion")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
def get_me(current_user: Annotated[Users, Depends(get_current_active_user)]):
    """Récupérer les informations de l'utilisateur connecté
        Récupérer les informations de l'utilisateur actuellement connecté.

        Cette route utilise le token JWT envoyé par le client pour identifier l'utilisateur.
        Elle retourne les informations de base de l'utilisateur sans exposer le mot de passe.

        Args:
            current_user (Users): Utilisateur authentifié injecté via la dépendance `get_current_active_user`.

        Returns:
            dict: Objet de réponse structuré contenant les informations de l'utilisateur :
                - id_user (int)
                - email_user (str)
                - role_user (str)
                - is_active (bool)
                - name_user (str)    
    """

    logger.info(f"Récupération des infos pour l'utilisateur connecté : {current_user.email_user}")
    return success_response(
        data={
            "id_user": current_user.id_user,
            "name_user": current_user.name_user,
            "email_user": current_user.email_user,
            "role_user": current_user.role_user,
            "is_active": current_user.is_active
            
        },
        message="Informations utilisateur récupérées"
    )

@router.get("/users")
def get_all_users(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[Users, Depends(require_admin)]
):
    """
    Récupérer tous les utilisateurs (admin seulement).
    
    Args:
        db (Session): Session SQLAlchemy.
        current_user (Users): Utilisateur authentifié (doit être admin).

    Returns:
        dict: Réponse contenant la liste des utilisateurs.
    """
    try:
        logger.info(f"Récupération de tous les utilisateurs par l'admin : {current_user.email_user}")
        return AuthService.get_all_users(db)
    except Exception as e:
        logger.exception("Erreur lors de la récupération des utilisateurs")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/logout")
def logout(current_user: Annotated[Users, Depends(get_current_active_user)]):
    """Se déconnecter (invalidation côté client)"""
    logger.info(f"Déconnexion de l'utilisateur : {current_user.email_user}")
    return success_response(
        message=f"Déconnexion réussie pour {current_user.email_user}"
    )
