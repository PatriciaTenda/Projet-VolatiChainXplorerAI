# Charger les librairies nécessaires
# Ajout du chemin de base
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from typing import Optional
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field, HttpUrl
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler
from pydantic_core.core_schema import ValidationInfo

class PyObjectId(ObjectId):
    """
    Type personnalisé pour permettre la validation d'un ObjectId de MongoDB avec Pydantic v2.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """
        Remplace __modify_schema__ en Pydantic v2.
        Spécifie que ce champ est converti en chaîne lors de la sérialisation.
        """
        return core_schema.no_info_wrap_validator_function(
            cls.validate,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def validate(cls, v, info: ValidationInfo = None):
        """
        Vérifie que l'ObjectId est valide.
        """
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

# ----------------- SCHÉMA DE SORTIE -----------------

class ArticlesFinanciersResponse(BaseModel):
    """
    Modèle de réponse utilisé pour renvoyer les articles stockés dans MongoDB.
    
    Attributs :
        id (str) : Identifiant unique MongoDB (_id).
        title (str) : Titre de l'article.
        content (str) : Contenu de l'article.
        source (str | None) : Source ou média de l'article.
        url (HttpUrl | None) : Lien vers l'article original.
        published_at (datetime | None) : Date de publication.
    """

    id: PyObjectId = Field(alias="_id")
    title: str = Field(alias="Title")
    content: str = Field(alias="Content")
    url: Optional[HttpUrl]
    author: Optional[str] = Field(alias="Author", default=None)
    published_at: Optional[datetime] = Field(alias="Date of publication", default=None)
    scraped_at: Optional[datetime] = Field(alias="scraped_at", default=None)


    class Config:
        populate_by_name = True  # Anciennement allow_population_by_field_name en v1
        frozen = True  # Rend les objets Pydantic immuables (comme des tuples)
        from_attributes = True  # Permet de lire à partir d'attributs (comme un ORM)
        json_encoders = {ObjectId: str}  # Permet de convertir automatiquement ObjectId en str
        arbitrary_types_allowed = True  # Permet d'utiliser des types personnalisés comme PyObjectId

