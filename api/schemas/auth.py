# Charger les librairies nécessaires
from pydantic import BaseModel
from api.schemas.users import UserResponse
from typing import Optional

class Token(BaseModel):
    """Token JWT"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    """Données contenues dans le token"""
    id_user: Optional[int] = None
    email_user: Optional[str] = None
    role_user: Optional[str] = None