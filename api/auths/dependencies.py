from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from api.auths.auth_services import AuthService
from api.exceptions.user_exceptions import ValidationError
from database.conn_db.connect_postgresql import get_db
from database.postgres.models.users import Users

# Sécurité HTTP Bearer (pour récupérer le token des headers)
security = HTTPBearer(auto_error=False)

#=========================================================================================================================================

def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)]
):
    """Dépendance pour récupérer l'utilisateur actuel"""
    
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentification requise",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        
        token = credentials.credentials
        return AuthService.get_current_user(db, token)

    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error.message,
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

#=========================================================================================================================================

def get_current_active_user(current_user : Annotated[Users, Depends(get_current_user)]):
    """Dépendance pour vérifier que l'utilisateur est actif"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utilisateur inactif"
        )
    return current_user

#=========================================================================================================================================

def require_admin(current_user : Annotated[Users, Depends(get_current_active_user)]):
    """Dépendance pour vérifier que l'utilisateur est admin"""
    if current_user.role_user != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Droits administrateur requis."
        )
    return current_user

#=========================================================================================================================================

def require_user_or_admin(current_user : Annotated[Users, Depends(get_current_active_user)]):
    """Dépendance pour vérifier que l'utilisateur est connecté (user ou admin)"""
    if current_user.role_user not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Droits insuffisants."
        )
    return current_user