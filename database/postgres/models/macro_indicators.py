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
from database.conn_db.connect_postgresql import Base
from sqlalchemy import Column, Integer, String, Float, Date

"""Créer les modèles de la base de donnée"""

class MacroBceMRO(Base):
    __tablename__ = "t_macro_bce_mro"
    
    id_mro = Column("id", Integer, primary_key=True, autoincrement=True)
    date_mro = Column("date", Date, unique=True, nullable=False)
    rate_mro = Column("value", Float)

    # Nouvelles colonnes standardisées
    obs_status_mro = Column("obs_status", String(10))
    time_period_mro = Column("time_period", String(20))
    indicator_name_mro = Column("indicator_name", String(200))
    source_label_mro = Column("source_label", String(200))

class MacroBceInflation(Base):
    __tablename__ = "t_macro_bce_inflation"

    id_inflation = Column("id", Integer, primary_key=True, autoincrement=True)
    date_inflation = Column("date", Date, unique=True, nullable=False)
    inflation_rate = Column("value", Float)

    # Nouvelles colonnes standardisées
    obs_status_inflation = Column("obs_status", String(10))
    time_period_inflation = Column("time_period", String(20))
    indicator_name_inflation = Column("indicator_name", String(200))
    source_label_inflation = Column("source_label", String(200))

class MacroBcetauxChomage(Base):
    __tablename__ = "t_macro_bce_unemployment"

    id_unemployment = Column("id", Integer, primary_key=True, autoincrement=True)
    date_unemployment = Column("date", Date, unique=True, nullable=False)
    unemployment_rate = Column("value", Float)

    # Nouvelles colonnes standardisées
    obs_status_unemployment = Column("obs_status", String(10))
    time_period_unemployment = Column("time_period", String(20))
    indicator_name_unemployment = Column("indicator_name", String(200))
    source_label_unemployment = Column("source_label", String(200))

class MacroBceMonetaryM3(Base):
    __tablename__ = "t_macro_bce_monetary_m3"

    id_monetary_m3 = Column("id", Integer, primary_key=True, autoincrement=True)
    date_monetary_m3 = Column("date", Date, unique=True, nullable=False)
    monetary_m3_rate = Column("value", Float)

    # Nouvelles colonnes standardisées 
    obs_status_m3 = Column("obs_status", String(10))
    time_period_m3 = Column("time_period", String(20))
    indicator_name_m3 = Column("indicator_name", String(200))
    source_label_m3 = Column("source_label", String(200))


#------- Modèle qui représente la vue MacroIndicatorsDaily----------
class MacroIndicatorsDaily(Base):
    """
    Modèle SQLAlchemy mappé à la vue v_macro_indicators_daily_v1.
    
    Cette vue agrège quotidiennement les quatre indicateurs macro de la BCE.
    
    READ-ONLY : Ce modèle ne doit pas être utilisé pour INSERT/UPDATE/DELETE.
    """
    __tablename__ = "v_macro_indicators_daily_v1"
    __table_args__ = {
        'extend_existing': True,
        'info': {'read_only': True}
    }

    # Attribut Python cohérent avec les autres modèles
    date = Column("date", Date, primary_key=True)
    rate_mro = Column("rate_mro", Float)
    inflation_rate = Column("inflation_rate", Float)
    unemployment_rate = Column("unemployment_rate", Float)
    monetary_m3_rate = Column("monetary_m3_rate", Float)
