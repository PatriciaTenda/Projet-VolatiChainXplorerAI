# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from sqlalchemy.orm import Session
from database.postgres import Users
from api.schemas import UserCreate
from security import hash_password  # une fonction de hachage

def create_user(db: Session, user: UserCreate):
    hashed_pwd = hash_password(user.password_user)
    db_user = Users(
        name_user=user.name_user,
        email_user=user.email_user,
        password_user=hashed_pwd
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(Users).filter(Users.email_user == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(Users).filter(Users.id_user == user_id).first()
