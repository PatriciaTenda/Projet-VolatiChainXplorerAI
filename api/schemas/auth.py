# Charger les librairies nécessaires
from pydantic import BaseModel, ConfigDict

from api.schemas.users import UserResponse


class Token(BaseModel):
    """Token JWT"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    
    model_config = ConfigDict(from_attributes=True)

class TokenData(BaseModel):
    """Données contenues dans le token"""
    id_user: int | None = None
    email_user: str | None = None
    role_user: str | None = None

    model_config = ConfigDict(from_attributes=True)