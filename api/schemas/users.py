
# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# ----- SCHEMAS POUR UTILISATEUR -----
class UserLogin(BaseModel):
    """ Données de connexion:
        Schéma de données utilisé pour connecter un utilisateur existant dans la base à l'API.

        Attributs :
        name_user (str) : Nom complet de l'utilisateur.
        email_user (EmailStr) : Adresse email de l'utilisateur (doit être unique).
        password_user (str) : Mot de passe en clair à hasher avant insertion en base.
        
    """    
    email: EmailStr = Field(..., description="Adresse email")
    password: str = Field(..., min_length=4, description="Mot de passe")

class UserCreate(BaseModel):
    """ Création d'utilisateur
        Schéma de données utilisé pour la création d'un nouvel utilisateur via l'API.

        Attributs :
        name_user (str) : Nom complet de l'utilisateur.
        email_user (EmailStr) : Adresse email de l'utilisateur (doit être unique).
        password_user (str) : Mot de passe en clair à hasher avant insertion en base.
        role(str) : Role de l'utilisateur.
    """
    name: str= Field(..., min_length=4, description="Nom de l'utilisateur")
    email: EmailStr = Field(..., description="Adresse email")
    password: str = Field(..., min_length=4, description="Mot de passe")
    role: str = Field("user", description="Rôle: user ou admin")

class UserResponse(BaseModel):
    """ Réponse utilisateur (sans mot de passe)
        Schéma de données utilisé pour retourner les informations d'un utilisateur.

        Attributs :
        id_user (int) : Identifiant unique de l'utilisateur.
        name_user (str) : Nom complet de l'utilisateur.
        email_user (EmailStr) : Adresse email de l'utilisateur.
        role(str) : Role de l'utilisateur.
        is_active(bool) : statut de connexion de l'utilisateur.
    """
    id_user: int
    name_user: str
    email_user: str
    role_user: str
    is_active: bool
    
    class Config:
        from_attributes = True # Permet à Pydantic de lire les données directement à partir d'un objet ORM 
                                # afin qu'on ait pas besoin de tout convertir à la main(dict ou autre)