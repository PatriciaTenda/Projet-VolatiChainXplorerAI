"""
Script de test unitaire pour vérifier le bon fonctionnement de l'endpoint /status de l'API FastAPI.

Ce script utilise TestClient de FastAPI pour envoyer une requête HTTP GET à l'URL "/status"
et vérifie que :
- le code de réponse HTTP est 200 (OK),
- la réponse JSON contient une clé "API" avec la valeur "running".

Le chemin vers le répertoire racine du projet est ajouté dynamiquement à sys.path
pour permettre l'import du module `api.main`.

Ce script peut est exécuté indépendamment pour lancer le test mannuellement.

Usage :
    python tests/test_status.py

Date : 23/06/2025
"""

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_status():
    response = client.get("/status")
    print("Status code:", response.status_code)
    print("Response JSON:", response.text)
    assert response.status_code == 200
    assert response.json()["API"] == "running"


if __name__=="__main__":
    test_status()