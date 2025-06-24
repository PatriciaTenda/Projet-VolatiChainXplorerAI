
# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from pydantic import BaseModel, EmailStr

# ----- SCHEMAS POUR UTILISATEUR -----

class UserCreate(BaseModel):
    """
    Schéma de données utilisé pour la création d'un nouvel utilisateur via l'API.

    Attributs :
        name_user (str) : Nom complet de l'utilisateur.
        email_user (EmailStr) : Adresse email de l'utilisateur (doit être unique).
        password_user (str) : Mot de passe en clair à hasher avant insertion en base.
    """
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """
    Schéma de données utilisé pour retourner les informations d'un utilisateur.

    Attributs :
        id_user (int) : Identifiant unique de l'utilisateur.
        name_user (str) : Nom complet de l'utilisateur.
        email_user (EmailStr) : Adresse email de l'utilisateur.
    """
    id_user: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True # Permet à Pydantic de lire les données directement à partir d'un objet ORM 
                        # afin qu'on ait pas besoin de tout convertir à la main(dict ou autre)

