"""
Ce module définit les modèles de données SQLAlchemy pour la base de données VolatiChainXplorerAI_pg.
Il inclut les tables suivantes :
- t_users : stocke les informations des utilisateurs de l'API (identifiant, nom, email, mot de passe).
- t_bitcoin_prices : enregistre l'historique des prix du Bitcoin (date, prix d'ouverture et de clôture, variation en pourcentage, volatilité, volume, capitalisation de marché).
Chaque modèle correspond à une table de la base de données et définit les colonnes et leurs types associés.

"""
# Charger les bibliothèques nécessaires
from database.conn_db.connect_postgresql import Base
from sqlalchemy import Column, Integer, Date, DateTime, String, UniqueConstraint, Numeric
from sqlalchemy.sql import func


"""Créer les modèles de la base de donnée"""

# La table des cours historique du bitcoin
class BitcoinPrices(Base):
    __tablename__ = "t_bitcoin_prices"

    __table_args__ = (
        UniqueConstraint(
            "date",
            "source",
            "currency",
            "granularity",
            name="uq_t_bitcoin_prices_date_source_currency_granularity",
        ),
    )

    id_price = Column("id", Integer, primary_key=True, autoincrement=True)

    # Colonnes principales demandées
    date = Column("date", Date, nullable=False)
    open_price = Column("open", Numeric(18, 8), nullable=False)
    high_price = Column("high", Numeric(18, 8))
    low_price = Column("low", Numeric(18, 8))
    close_price = Column("close", Numeric(18, 8), nullable=False)
    volume = Column("volume", Numeric(24, 8))
    market_cap = Column("market_cap", Numeric(28, 8))

    # Nouvelles colonnes
    source = Column("source", String(50), nullable=False, default="CoinMarketCap")
    currency = Column("currency", String(10), nullable=False, default="EUR")
    granularity = Column("granularity", String(20), nullable=False, default="1d")
    collected_at = Column("collected_at", DateTime(timezone=True), nullable=False, server_default=func.now())

