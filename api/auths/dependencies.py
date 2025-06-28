from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database.conn_db.connect_postgresql import get_db
from api.auths.auth_services import AuthService
from api.exceptions.user_exceptions import ValidationError

# Sécurité HTTP Bearer (pour récupérer le token des headers)
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Dépendance pour récupérer l'utilisateur actuel"""
    try:
        token = credentials.credentials
        user = AuthService.get_current_user(db, token)
        return user
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"}
        )

def get_current_active_user(current_user = Depends(get_current_user)):
    """Dépendance pour vérifier que l'utilisateur est actif"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utilisateur inactif"
        )
    return current_user

def require_admin(current_user = Depends(get_current_active_user)):
    """Dépendance pour vérifier que l'utilisateur est admin"""
    if current_user.role_user != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Droits administrateur requis"
        )
    return current_user

def require_user_or_admin(current_user = Depends(get_current_active_user)):
    """Dépendance pour vérifier que l'utilisateur est connecté (user ou admin)"""
    if current_user.role_user not in ["user", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentification requise"
        )
    return current_user