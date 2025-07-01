class UserException(Exception):
    """Exception de base pour les erreurs liées aux utilisateurs."""
    def __str__(self):
        return self.message


class UserNotFound(UserException):
    """Utilisateur non trouvé."""
    def __init__(self, id_user: int):
        self.message = f"Utilisateur avec ID {id_user} introuvable"
        super().__init__(self.message)


class UserAlreadyExists(UserException):
    """Un utilisateur avec cet email existe déjà."""
    def __init__(self, email: str):
        self.message = f"Un utilisateur avec l'email '{email}' existe déjà."
        super().__init__(self.message)


class AuthenticationError(UserException):
    """Échec de l'authentification."""
    def __init__(self):
        self.message = "Échec de l'authentification : email ou mot de passe incorrect."
        super().__init__(self.message)


class PermissionDenied(UserException):
    """Accès refusé pour l'utilisateur connecté."""
    def __init__(self, action: str = "effectuer cette action"):
        self.message = f"Vous n'avez pas les droits nécessaires pour {action}."
        super().__init__(self.message)


class ValidationError(UserException):
    """Erreur de validation des données utilisateur."""
    def __init__(self, message: str):
        self.message = f"Erreur de validation : {message}"
        super().__init__(self.message)


class DatabaseError(UserException):
    """Erreur rencontrée lors d'une opération en base de données."""
    def __init__(self, operation: str):
        self.message = f"Erreur lors de l'opération sur la base de données : {operation}"
        super().__init__(self.message)
