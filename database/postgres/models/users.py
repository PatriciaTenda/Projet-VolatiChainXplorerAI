"""
Ce module définit les modèles de données SQLAlchemy pour la base de données VolatiChainXplorerAI_pg.
Il inclut les tables suivantes :
- t_users : stocke les informations des utilisateurs de l'API (identifiant, nom, email, mot de passe).
- t_bitcoin_prices : enregistre l'historique des prix du Bitcoin (date, prix d'ouverture et de clôture, variation en pourcentage, volatilité, volume, capitalisation de marché).
Chaque modèle correspond à une table de la base de données et définit les colonnes et leurs types associés.

"""
# Charger les bibliothèques nécessaires
from sqlalchemy.orm import declarative_base
from database.conn_db.connect_postgresql import Base
from sqlalchemy import Column, Integer, String

"""Créer les modèles de la base de donnée"""

# La table des utilisateurs de l'API
class Users(Base):
    __tablename__= "t_users"
    id_user = Column(Integer, primary_key=True, autoincrement=True,)
    name_user = Column(String(50), nullable=False)
    email_user = Column(String(100), unique=True, nullable=False)
    password_user = Column(String(100), nullable=False)


