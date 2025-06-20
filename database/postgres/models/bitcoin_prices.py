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
from sqlalchemy import Column, Integer, String, Float, Date, DateTime

"""Créer les modèles de la base de donnée"""

# La table des cours historique du bitcoin
class BitcoinPrices(Base):
    __tablename__= "t_bitcoin_prices"

    id_price_bitcoin = Column(Integer, primary_key=True, autoincrement=True)
    date_bitcoin = Column(Date, unique=True, nullable=False )
    time_open_bitcoin = Column(DateTime, nullable=True )
    time_close_bitcoin = Column(DateTime, nullable=True )
    time_high_bitcoin = Column(DateTime, nullable=True )  # heure à laquelle le prix max a été atteint
    time_low_bitcoin = Column(DateTime, nullable=True )   # heure du prix le plus bas

    open_price_bitcoin = Column(Float, nullable=False)	
    close_price_bitcoin = Column(Float, nullable=False)
    high_price_bitcoin = Column(Float, nullable=True)   
    low_price_bitcoin = Column(Float, nullable=True)   

    volume_bitcoin = Column(Float, nullable=True)
    market_Cap_bitcoin = Column(Float, nullable=True)

