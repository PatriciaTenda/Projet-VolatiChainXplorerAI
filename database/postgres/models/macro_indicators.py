"""
Modèles ORM pour les indicateurs macro-économiques de la BCE
===========================================================

Ce module déclare les classes SQLAlchemy mappées sur la base de données **VolatiChainXplorerAI_pg**.

Tables gérées
-------------
* **t_macro_bce_mro** - Taux des opérations principales de refinancement (Main Refinancing Operations).
* **t_macro_bce_inflation** - Taux d'inflation annuel harmonisé (HICP).
* **t_macro_bce_unemployment** - Taux de chômage harmonisé de la zone euro.
* **t_macro_bce_monetary_m3** - Croissance annuelle de l'agrégat monétaire M3.

Vue en lecture seule
--------------------
* **v_macro_indicators_daily_v1** - Vue agrégée réunissant pour chaque jour
  les quatre indicateurs ci-dessus (modèle :class:`MacroIndicatorsDaily`, *read-only*).

Chaque classe :

* hérite de :class:`Base` (importée depuis *database.conn_db.connect_postgresql*),
* correspond nom-pour-nom à la table ou à la vue SQL,
* définit explicitement toutes les colonnes, leurs types et contraintes
  (clé primaire, unicité, nullabilité, autoincrément).

Ces modèles servent de couche d-accès aux données pour les analyses
macro ↔ cryptomonnaies réalisées par **VolatiChainXplorerAI**.
"""

# Charger les bibliothèques nécessaires
from sqlalchemy.orm import declarative_base
from database.conn_db.connect_postgresql import Base
from sqlalchemy import Column, Integer, String, Float, Date, DateTime

"""Créer les modèles de la base de donnée"""

class MacroBceMRO(Base):
    __tablename__= "t_macro_bce_mro"
    
    id_mro = Column(Integer, primary_key=True, autoincrement=True)
    date_mro = Column(Date, unique=True, nullable=False)
    rate_mro = Column(Float, nullable=True)
    time_periode_mro = Column(String(100), nullable=True)
    indicator_name_mro = Column(String(100), nullable=True)  # MRO : "Main Refinancing Operations"
    source_label_mro = Column(String(100), nullable=True)

class MacroBceInflation(Base):
    __tablename__="t_macro_bce_inflation"

    id_inflation = Column(Integer,autoincrement=True, primary_key=True)
    date_inflation = Column(Date, unique=True, nullable=False)
    inflation_rate = Column(Float, nullable=True)
    time_periode_inflation = Column(String(100), nullable=True)
    indicator_name_inflation = Column(String(100), nullable=True)
    source_label_inflation = Column(String(100), nullable=True)

class MacroBcetauxChomage(Base):
    __tablename__="t_macro_bce_unemployment"

    id_unemployment = Column(Integer,autoincrement=True, primary_key=True)
    date_unemployment = Column(Date, unique=True, nullable=False)
    unemployment_rate = Column(Float, nullable=True)
    indicator_name_unemployment = Column(String(100), nullable=True)
    source_label_unemployment= Column(String(100), nullable=True)

class MacroBceMonetaryM3(Base):
    __tablename__="t_macro_bce_monetary_m3"

    id_monetary_m3 = Column(Integer,autoincrement=True,  primary_key=True)
    date_monetary_m3 = Column(Date, unique=True, nullable=False)
    monetary_m3_rate  = Column(Float, nullable=True)

    indicator_name_m3= Column(String(100), nullable=True)
    source_label_m3 = Column(String(100), nullable=True)

"""
class MacroBceIndicatorDaily(Base):
    __tablename__="t_macro_bce_indicators_daily"

    id_macro_daily = Column(Integer, autoincrement=True primary_key=True)
    date_macro_daily = Column(Date, unique=True, nullable=False)

    mro_rate = Column(Float, nullable=True)
    inflation_rate = Column(Float, nullable=True)
    unemployment_rate = Column(Float, nullable=True)
    monetary_m3_rate = Column(Float, nullable=True)
    source_label = Column(String(100), nullable=True)
"""

#------- Modèle qui représente la vue MacroIndicatorsDaily----------
class MacroIndicatorsDaily(Base):
    """
    Modèle SQLAlchemy mappé à la vue v_macro_indicators_daily_v1.
    Ce modèle est en lecture seule.
    """
    __tablename__ = "v_macro_indicators_daily_v1"
    __table_args__ = {'extend_existing': True}

    day = Column(Date, primary_key=True)
    rate_mro = Column(Float)
    inflation_rate = Column(Float)
    unemployment_rate = Column(Float)
    monetary_m3_rate = Column(Float)
