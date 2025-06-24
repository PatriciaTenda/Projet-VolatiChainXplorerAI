from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel

# Charger l'API
app = FastAPI()

# Modèle pydantic pour valider les données
class Passenger(BaseModel):
    id: int
    name: str
    sex:str
    age : Optional[float]
    survived:int
    pclass: int
    fare: Optional[float]

# les données en dur - 10premiers passagers du Titanic
passengers_data = [
    {"id": 1, "name": "Braund, Mr. Owen Harris", "sex": "male", "age": 22.0, "survived": 0, "pclass": 3, "fare": 7.25},
    {"id": 2, "name": "Cumings, Mrs. John Bradley", "sex": "female", "age": 38.0, "survived": 1, "pclass": 1, "fare": 71.28},
    {"id": 3, "name": "Heikkinen, Miss. Laina", "sex": "female", "age": 26.0, "survived": 1, "pclass": 3, "fare": 7.92},
    {"id": 4, "name": "Futrelle, Mrs. Jacques Heath", "sex": "female", "age": 35.0, "survived": 1, "pclass": 1, "fare": 53.10},
    {"id": 5, "name": "Allen, Mr. William Henry", "sex": "male", "age": 35.0, "survived": 0, "pclass": 3, "fare": 8.05},
    {"id": 6, "name": "Moran, Mr. James", "sex": "male", "age": None, "survived": 0, "pclass": 3, "fare": 8.46},
    {"id": 7, "name": "McCarthy, Mr. Timothy J", "sex": "male", "age": 54.0, "survived": 0, "pclass": 1, "fare": 51.86},
    {"id": 8, "name": "Palsson, Master. Gosta Leonard", "sex": "male", "age": 2.0, "survived": 0, "pclass": 3, "fare": 21.08},
    {"id": 9, "name": "Johnson, Mrs. Oscar W", "sex": "female", "age": 27.0, "survived": 1, "pclass": 3, "fare": 11.13},
    {"id": 10, "name": "Nasser, Mrs. Nicholas", "sex": "female", "age": 14.0, "survived": 1, "pclass": 2, "fare": 30.07}
]

# Page1: Page d'accueil
@app.get("/")
def welcome():
    """Page d'acuueil de l'API"""
    return {"message" : "Bienvenue sur l'API Titanic !"}

# Page2: Page pour voir tous les passagers
@app.get("/passagers", response_model=List[Passenger])
def get_all_passangers():
    """Récupérer tous  les passagers"""
    return passengers_data

# Page3: Page pour voir un passager
@app.get("/passengers/{passager_id}", response_model= Passenger)
def get_passenger(passenger_id: int):
    passenger = next((p for p in passengers_data if p["id"]== passenger_id), None)
    if not passenger:
        raise HTTPException(status_code=404, detail="Passager non trouvé")
    return passenger

# Page4: Page pour voir uniquement les passagers survivant
@app.get("/passengers/search/survivors")
def get_survivors():
    """Récupérer les passagers survivant"""
    survivors = [p for p in passengers_data if p["survived"]==1]
    return {"count": len(survivors), "survivors": survivors}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)