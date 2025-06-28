# === Import des bibliothèques nécessaires ===
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sqlalchemy.orm import Session
from database.postgres.models.users import Users
from api.schemas.users import UserCreate, UserLogin, UserResponse
from api.schemas.auth import Token
from api.schemas.reponse import success_response
from api.exceptions.user_exceptions import ValidationError
from api.auths.jwt_handler import JWTHandler
from setup.logger_config import setup_logger

# === Initialisation du logger ===
name_file = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(name_file)


class AuthService:
    """
    Service d'authentification contenant les fonctionnalités suivantes :
    - Création de compte
    - Connexion
    - Récupération de l'utilisateur via token
    - Récupération de tous les utilisateurs (admin)
    """

    @staticmethod
    def create_user(db: Session, user_data: UserCreate):
        """
        Crée un nouvel utilisateur après validation des données.

        Args:
            db (Session): Session SQLAlchemy.
            user_data (UserCreate): Données saisies par l'utilisateur (name, email, mot de passe, rôle).

        Returns:
            dict: Réponse de succès avec les infos de l'utilisateur.

        Raises:
            ValidationError: si l'email existe déjà ou si le rôle est invalide.
        """
        logger.info(f"Tentative de création d'utilisateur avec l'email : {user_data.email}")

        # Vérifie si un utilisateur avec cet email existe déjà
        existing_user = db.query(Users).filter(Users.email_user == user_data.email).first()
        if existing_user:
            logger.warning("Échec création utilisateur : email déjà utilisé")
            raise ValidationError("Un utilisateur avec cet email existe déjà")

        # Vérifie la validité du rôle
        if user_data.role not in ["user", "admin"]:
            logger.warning("Échec création utilisateur : rôle invalide")
            raise ValidationError("Le rôle doit être 'user' ou 'admin'")

        # Hache le mot de passe pour le stocker de manière sécurisée
        password_hash = JWTHandler.hash_password(user_data.password)

        # Création de l'objet utilisateur
        db_user = Users(
            name_user=user_data.name,
            email_user=user_data.email,
            hashed_password_user=password_hash,
            role_user=user_data.role
        )

        # Ajout et validation dans la base
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.info(f"Utilisateur créé avec succès : {db_user.email_user}")
        return success_response(
            data=UserResponse.from_orm(db_user),
            message="Utilisateur créé avec succès"
        )

    @staticmethod
    def login(db: Session, login_data: UserLogin):
        """
        Authentifie un utilisateur avec email et mot de passe.

        Args:
            db (Session): Session SQLAlchemy.
            login_data (UserLogin): Données de connexion (email + mot de passe).

        Returns:
            dict: Token JWT et infos utilisateur.

        Raises:
            ValidationError: si l'email ou le mot de passe est incorrect, ou si le compte est désactivé.
        """
        logger.info(f"Tentative de connexion avec l'email : {login_data.email}")

        # Recherche de l'utilisateur
        user = db.query(Users).filter(Users.email_user == login_data.email).first()
        if not user:
            logger.warning("Connexion échouée : utilisateur non trouvé")
            raise ValidationError("Email ou mot de passe incorrect")

        # Vérifie le mot de passe
        if not JWTHandler.verify_password(login_data.password, user.hashed_password_user):
            logger.warning("Connexion échouée : mot de passe incorrect")
            raise ValidationError("Email ou mot de passe incorrect")

        # Vérifie si le compte est actif
        if not user.is_active:
            logger.warning(f"Connexion échouée : compte inactif pour {user.email_user}")
            raise ValidationError("Compte désactivé")

        # Création du token d'accès
        access_token = JWTHandler.create_access_token(
            user_id=user.id_user,
            email=user.email_user,
            role=user.role_user
        )

        logger.info(f"Connexion réussie pour {user.email_user}")

        # Création de la réponse contenant le token et l'utilisateur
        token_response = Token(
            access_token=access_token,
            user=UserResponse.model_validate(user)
        )

        return success_response(
            data=token_response,
            message="Connexion réussie"
        )

    @staticmethod
    def get_current_user(db: Session, token: str) -> Users:
        """
        Récupère les informations de l'utilisateur à partir du token JWT.

        Args:
            db (Session): Session SQLAlchemy.
            token (str): Token JWT fourni par l'utilisateur.

        Returns:
            Users: Utilisateur identifié.

        Raises:
            ValidationError: si le token est invalide ou expiré, ou si l'utilisateur n'existe pas.
        """
        logger.info("Décodage du token pour récupérer l'utilisateur courant")

        # Décodage du token
        payload = JWTHandler.decode_token(token)
        if not payload:
            logger.error("Token invalide ou expiré")
            raise ValidationError("Token invalide ou expiré")

        # Recherche de l'utilisateur
        user = db.query(Users).filter(Users.id_user == payload["user_id"]).first()
        if not user:
            logger.warning("Utilisateur non trouvé via le token")
            raise ValidationError("Utilisateur non trouvé")

        if not user.is_active:
            logger.warning(f"Utilisateur {user.email_user} inactif")
            raise ValidationError("Compte désactivé")

        logger.info(f"Utilisateur courant récupéré : {user.email_user}")
        return user

    @staticmethod
    def get_all_users(db: Session):
        """
        Récupère tous les utilisateurs.

        Args:
            db (Session): Session SQLAlchemy.

        Returns:
            dict: Liste des utilisateurs avec message de succès.
        """
        logger.info("Récupération de tous les utilisateurs")

        users = db.query(Users).all()
        logger.info(f"{len(users)} utilisateurs trouvés")

        try:
            user_responses = [UserResponse.model_validate(user) for user in users]
        except Exception as e:
            logger.error(f"Erreur lors de la conversion ORM vers Pydantic : {e}")
            raise  
        return success_response(
            data=user_responses,
            message=f"{len(users)} utilisateurs trouvés"
        )