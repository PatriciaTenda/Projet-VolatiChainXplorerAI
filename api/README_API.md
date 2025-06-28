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
- /bitcoin-prices : Prix journaliers du Bitcoin (PostgreSQL)
- /macro-indicators : Les indicateurs macroéconomiques de la BCE
- /articles-financiers : Articles économiques (MongoDB)

# Format entrée / sortie des données

### `POST /auth/login`
- **Entrée** (formulaire) :
  - `username` : nom d'utilisateur
  - `email`     : adresse email
  - `password` : mot de passe

- **Sortie** :
```json
    {
    "access_token": "<token_jwt>",
    "token_type": "bearer"
    }
```

### GET /bitcoin-prices
Entrée : aucune (authentification requise avec Bearer <token>)
Sortie :
```json
    [
         {
                "id_price_bitcoin": 0,
                "date_bitcoin": "2025-06-24",
                "time_open_bitcoin": "2025-06-24T15:14:46.843Z",
                "time_close_bitcoin": "2025-06-24T15:14:46.843Z",
                "time_high_bitcoin": "2025-06-24T15:14:46.843Z",
                "time_low_bitcoin": "2025-06-24T15:14:46.843Z",
                "open_price_bitcoin": 0,
                "close_price_bitcoin": 0,
                "high_price_bitcoin": 0,
                "low_price_bitcoin": 0,
                "volume_bitcoin": 0,
                "market_Cap_bitcoin": 0
       }
    ]
```
### GET /macro-indicators/inflation
Entrée : aucune (authentification requise avec Bearer <token>)
Sortie :
```json
[
  {
    "id_inflation": 0,
    "date_inflation": "2025-06-24",
    "inflation_rate": 0,
    "time_periode_inflation": "string",
    "indicator_name_inflation": "string",
    "source_label_inflation": "string"
  }
]
```


### GET /bitcoin-macro-indicators
Entrée : aucune (authentification requise avec Bearer <token>)
Sortie :
```json
[
  {
    "day": "2025-06-24",
    "close_price_bitcoin": 0,
    "rate_mro": 0,
    "inflation_rate": 0,
    "unemployment_rate": 0,
    "monetary_m3_rate": 0
  }
]
```
### GET /articles-financiers
Entrée : aucune (authentification requise avec Bearer <token>)
Sortie :
```json
    [
        {
          "_id": "string",
          "Title": "string",
          "Content": "string",
          "url": "https://example.com/",
          "Author": "string",
          "Date of publication": "2025-06-24T15:15:44.612Z",
          "scraped_at": "2025-06-24T15:15:44.612Z"
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