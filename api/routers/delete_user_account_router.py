# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from fastapi import Depends, HTTPException, status, APIRouter
from api.auths.auth_services import AuthService  # récupère l'utilisateur connecté
from sqlalchemy.orm import Session
from database.conn_db.connect_postgresql import get_db
from database.postgres.models.users import Users
from setup.logger_config import setup_logger

# Mise en place d'un logger pour le module de création des collections
name_file =os.path.splitext(os.path.basename(__file__))[0]
# set le logger du module en cours
logger = setup_logger(name_file)

# Création d’un routeur dédié aux routes relatives au Bitcoin
router = APIRouter(
    prefix="/api/v1/delete-user-account", # Préfixe commun pour toutes les routes 
    tags=["delete user account"]    # Étiquette utilisée dans la documentation Swagger
)


@router.delete("/", status_code=204)
def delete_account(
    db: Session = Depends(get_db),
    current_user: Users= Depends(AuthService.get_current_user)
    
):
    user = db.query(Users).filter(Users.id_user == current_user.id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    db.delete(user)
    db.commit()
    return {"message": "Compte supprimé avec succès"}
