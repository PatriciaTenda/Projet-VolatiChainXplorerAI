# Charger les librairies nécessaires
from pydantic import BaseModel

from api.schemas.users import UserResponse


class Token(BaseModel):
    """Token JWT"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    """Données contenues dans le token"""
    id_user: int | None = None
    email_user: str | None = None
    role_user: str | None = None