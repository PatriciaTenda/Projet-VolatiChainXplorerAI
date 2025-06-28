"""
Ce module définit les modèles de données SQLAlchemy pour la base de données VolatiChainXplorerAI_pg.
Il inclut les tables suivantes :
- t_users : stocke les informations des utilisateurs de l'API (identifiant, nom, email, mot de passe).
"""
# Charger les bibliothèques nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..", "..")))
"""print("Chemins de recherche :")
for p in sys.path:
    print(p)
"""
from database.conn_db.connect_postgresql import Base
from sqlalchemy import Column, Integer, String, Boolean

"""Créer les modèles de la base de donnée"""

# La table des utilisateurs de l'API
class Users(Base):
    __tablename__= "t_users"
    id_user = Column(Integer, primary_key=True, autoincrement=True,)
    name_user = Column(String(50), nullable=False)
    email_user = Column(String(100), unique=True, nullable=False)
    hashed_password_user = Column(String(100), nullable=False)
    role_user = Column(String(20), nullable=False, default="user")  
    is_active = Column(Boolean, nullable=False, default=True)
