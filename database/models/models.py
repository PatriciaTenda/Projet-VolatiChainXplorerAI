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

# Créer les modèles de la base de donnée
# La table des utilisateurs de l'API
def Users(Base):
    __tablename__= "t_users"
    id_user = Column(primary_key=True)
    name_user = Column(String(50))
    email_user = Column()
    password_user = Column()


# La table des cours historique du bitcoin
def BitcoinPrices(Base):
    __tablename__= "t_bitcoin_prices"

    id_price_bitcoin = Column(Integer, primary_key=True, autoincrement=True)
    date_bitcoin = Column(Date, unique=True, nullable=False )
    time_open_bitcoin = Column(DateTime, unique=True, nullable=False )
    time_close_bitcoin = Column(DateTime, unique=True, nullable=False )
    time_high_bitcoin = Column(DateTime, unique=True, nullable=True )  # heure à laquelle le prix max a été atteint
    time_low_bitcoin = Column(DateTime, unique=True, nullable=True )   # heure du prix le plus bas

    open_price_bitcoin = Column(Float, nullable=False)	
    close_price_bitcoin = Column(Float, nullable=False)
    high_price_bitcoin = Column(Float, nullable=False)   
    low_price_bitcoin = Column(Float, nullable=False)   

    volume_bitcoin = Column(Float, nullable=True)
    marketCap_bitcoin = Column(Float, nullable=True)

# La table des taux directeurs (MRO) de la banque centrale europeenne

def MacroBceMRO(Base):
    __tablename__= "t_macro_bce_mro"
    
    id_mro = Column(Integer, primary_key=True, autoincrement=True)
    date_mro = Column(Date, unique=True, nullable=False)
    rate_mro = Column(Float, nullable=False)
    time_periode_mro = Column(String, nullable=True)
    indicator_name_mro = Column(String, nullable=True)  # MRO : "Main Refinancing Operations"
    source_label = Column(String, nullable=True)

def MacroBceInflation(Base):
    __tablename__="t_macro_bce_inflation"

    id_inflation = Column(Integer, primary_key=True)
    date_inflation = Column(Date, unique=True, nullable=False)
    inflation_rate = Column(Float, nullable=False)
    time_periode_inflation = Column(String, nullable=True)
    indicator_name_inflation = Column(String, nullable=True)
    source_label = Column(String, nullable=True)

def MacroBcetauxChomage(Base):
    __tablename__="t_macro_bce_taux_chomage"

    id_chomage = Column(Integer, primary_key=True)
    date_chomage = Column(Date, unique=True, nullable=False)
    taux_chomage_zone_euro = Column(Float, nullable=False)
    source_label = Column(String, nullable=True)

def MacroBceMasseMonetaire(Base):
    __tablename__="t_macro_bce_masse_monetaire"

    id_masse = Column(Integer, primary_key=True)
    date_masse = Column(Date, unique=True, nullable=False)
    masse_m3_zone_euro = Column(Float, nullable=False)
    source_label = Column(String, nullable=True)


def MacroBceIndicatorDaily(Base):
    __tablename__="t_macro_bce_indicators_daily"

    id_macro_daily = Column(Integer, primary_key=True)
    date_macro_daily = Column(Date, unique=True, nullable=False)

    taux_mro = Column(Float, nullable=True)
    inflation_zone_euro = Column(Float, nullable=True)
    taux_chomage_zone_euro = Column(Float, nullable=True)
    masse_m3_zone_euro = Column(Float, nullable=True)
    source_label = Column(String, nullable=True)