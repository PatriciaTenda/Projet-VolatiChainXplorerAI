# Objectif de l'API
L’objectif de cette API est la restitution intelligente des données stockées dans tes deux bases, pour préparer l’analyse sémantique et prédictive.

# Restitution intelligente des données
```bash
api/
│
├── main.py
│
├── routers/
│   ├── auth.py            # Authentification (login)
│   ├── btc.py             # Données BTC (PostgreSQL)
│   ├── articles.py        # Données textuelles (MongoDB)
│   └── status.py          # Vérification du système
│
├── auths/
│   ├── auth_service.py    # Auth utils (JWT, hash, user)
│   └── user_db.py         # Faux utilisateur ou lien vers DB
```

#  Endpoints principaux
### Authentification (`/auth`)
- `POST /auth/login`  
  → Authentifie l’utilisateur et retourne un token JWT

### Données Bitcoin (`/btc`)
- `GET /btc/prices`  
  → Récupère les données historiques du prix du Bitcoin (depuis PostgreSQL)

###  Données textuelles (`/articles`)
- `GET /articles/`  
  → Récupère les articles/textes financiers (depuis MongoDB)

### Statut de l’API (`/status`)
- `GET /status`  
  → Vérifie l’état de l’API et la connexion aux bases de données


# Technologies et Librairies
- **Python 3.12**
- **FastAPI** - Framework web rapide et moderne
- **Uvicorn** - Serveur ASGI ultra-rapide
- **Pydantic** - Validation des données

# URLs claires et descriptives :
- /api/v1/bitcoin_prices : Toutes les données de prix Bitcoin.
- /api/v1/bitcoin_prices/{id} : Une donnée de prix Bitcoin spécifique par ID.
- /api/v1/macro_indicators : Tous les indicateurs macro.

# Format entrée / sortie des données

### `POST /auth/login`
- **Entrée** (formulaire) :
  - `username` : nom d'utilisateur
  - `password` : mot de passe

- **Sortie** :
```json
    {
    "access_token": "<token_jwt>",
    "token_type": "bearer"
    }
```

### GET /btc/prices
Entrée : aucune (authentification requise avec Bearer <token>)
Sortie :
```json
    [
        {
            "date": "2025-06-20",
            "price": 65900.0
        },
        {
            "date": "2025-06-21",
            "price": 66250.5
        }   
    ]
```
### GET /articles/
Entrée : aucune (authentification requise avec Bearer <token>)
Sortie :
```json
    [
        {
            "title": "Bitcoin atteint un nouveau sommet",
            "content": "Le Bitcoin a franchi la barre des 70 000 $...",
            "source": "CryptoNews",
            "published_at": "2025-06-19"
        }
    ]
```
# GET /status
Entrée : aucune
Sortie :
```json
    {
    "postgres": "OK",
    "mongo": "OK",
    "API": "running"
    }
```