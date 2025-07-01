class BitcoinPricesNotFound(Exception):
    """Cours du bitcoin non trouvé"""
    def __init__(self, skip: int=0, limit: int=100 ):
        self.message = f"Aucun prix du Bitcoin trouvé pour la page : skip={skip}, limit={limit}"
        super().__init__(self.message)

class ValidationError(Exception):
    """Erreur de validation des données"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DatabaseError(Exception):
    """Erreur de base de données"""
    def __init__(self, operation: str):
        self.message = f"Erreur lors de l'opération: {operation}"
        super().__init__(self.message)