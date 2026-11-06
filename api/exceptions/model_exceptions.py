class ModelUnavailableError(RuntimeError):
    """Exception déclenche lorsque le modèle de prédiction demandé est indisponible."""
    def __init__(self, message: str):
        self.message = f"Modèle indisponible : {message}"
        super().__init__(self.message)
class InferenceError(RuntimeError):
    """Exception déclenchée lorsque l’inférence du modèle échoue."""
    def __init__(self, message: str):
        super().__init__(f"Échec de l’inférence : {message}")