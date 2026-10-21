
from typing import Any

from pydantic import BaseModel


class StandardResponse(BaseModel):
    """Réponse API standardisée"""
    success: bool
    message: str
    data: list[Any] | None = None
    count: int | None = None
    metadata: dict[str, Any] | None = None

def success_response(data: Any = None, message: str = "Opération réussie", count: int | None = None, metadata: dict[str, Any] | None = None):
    """Créer une réponse de succès"""
    if data is not None and not isinstance(data, list):
        data = [data]
    
    return StandardResponse(
        success=True,
        message=message,
        data=data,
        count=count or (len(data) if data else 0),
        metadata=metadata or {}
    ).model_dump()

def error_response(message: str, data: Any = None, metadata: dict[str, Any] | None = None):
    """Créer une réponse d'erreur"""
    return StandardResponse(
        success=False,
        message=message,
        data=data,
        count=0,
        metadata=metadata or {}
    ).model_dump()