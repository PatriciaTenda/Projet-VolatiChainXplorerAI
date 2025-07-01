# Charger les bibliothèques nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..", "..")))

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# Configuration JWT simple
SECRET_KEY = "cle_secrete_super_securisee_123456789"  # ⚠️ À remplacer en production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuration du contexte de hachage pour les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTHandler:
    """
    Classe utilitaire pour la gestion des mots de passe et des tokens JWT.
    
    - Fournit des méthodes pour hacher et vérifier les mots de passe.
    - Génère des tokens JWT à partir d'informations utilisateur.
    - Décode et valide les tokens JWT reçus.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hache un mot de passe en clair à l'aide de bcrypt.

        Args:
            password (str): Le mot de passe en clair à hacher.

        Returns:
            str: Le mot de passe haché.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Vérifie qu'un mot de passe en clair correspond à son hash.

        Args:
            plain_password (str): Le mot de passe fourni par l'utilisateur.
            hashed_password (str): Le mot de passe haché stocké en base.

        Returns:
            bool: True si les deux correspondent, False sinon.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user_id: int, email: str, role: str) -> str:
        """
        Crée un token JWT contenant les informations de l'utilisateur.

        Args:
            user_id (int): L'identifiant de l'utilisateur.
            email (str): L'adresse email de l'utilisateur.
            role (str): Le rôle de l'utilisateur (ex: 'admin', 'user').

        Returns:
            str: Le token JWT signé.
        """
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        payload = {
            "user_id": user_id,
            "email": email,
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow()
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        """
        Décode un token JWT et vérifie sa validité (expiration, structure).

        Args:
            token (str): Le token JWT à décoder.

        Returns:
            Optional[dict]: Les informations extraites du token (user_id, email, role),
                            ou None si le token est invalide ou expiré.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            exp = payload.get("exp")
            if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
                return None

            return {
                "user_id": payload.get("user_id"),
                "email": payload.get("email"),
                "role": payload.get("role")
            }
        except JWTError:
            return None
