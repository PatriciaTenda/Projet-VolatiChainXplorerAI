# Exception de base personnalisée pour centraliser le traitement des erreurs
class BaseAPIException(Exception):
    """
    Classe de base pour toutes les exceptions personnalisées de l'API.
    Permet de centraliser le message et le code d'erreur HTTP.
    """
    def __init__(self, message: str, code: int = 400):
        self.message = message        # Message explicite pour être afficher ou être logger
        self.code = code              # Code HTTP qui va être renvoyer via HTTPException
        super().__init__(self.message)

# Exception levée lorsqu'une erreur de validation est détectée
class ValidationError(BaseAPIException):
    """
    Exception levée lorsqu'une validation de données échoue (entrée invalide, format incorrect...).
    """
    def __init__(self, message: str):
        super().__init__(message, code=422)  # 422 veut dire :Unprocessable Entity

# Exception levée lorsque les indicateurs macroéconomiques ne sont pas trouvés
class MacroIndicatorsNotFound(BaseAPIException):
    """
    Exception levée lorsque les indicateurs macroéconomiques sont introuvables
    dans la base de données pour une pagination donnée.
    """
    def __init__(self, skip: int = 0, limit: int = 100):
        # Message personnalisé avec détails de la page demandée
        message = f"Aucun indicateur macroéconomique trouvé pour la page : skip={skip}, limit={limit}"
        super().__init__(message, code=404)  # 404 veut dire : Not Found

# Exception levée lors d'un problème général de base de données (lecture, écriture, etc.)
class DatabaseError(BaseAPIException):
    """
    Exception levée lorsqu'une opération sur la base de données échoue (lecture, écriture...).
    """
    def __init__(self, operation: str):
        # Message incluant le nom de l'opération échouée
        message = f"Erreur lors de l'opération: {operation}"
        super().__init__(message, code=500)  # 500 veut dire : Internal Server Error
