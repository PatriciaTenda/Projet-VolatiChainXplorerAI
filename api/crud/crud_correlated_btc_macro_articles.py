# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","..")))

from setup.logger_config import setup_logger
from database.conn_db.connect_mongodb import client, MONGO_DB
from database.conn_db.connect_postgresql import SessionLocal
from sqlalchemy.orm import Session
from datetime import date, datetime
from fastapi import HTTPException
from api.schemas.correlated_btc_rates_articlesFi import BtcIndicatorsArticlesResponse, CorrelatedResponse
from api.schemas.aggregate_btc_Macro_Indicators import BitcoinMacroIndicatorsResponse
from api.crud.crud_aggregate_btc_Macro_Indicators import get_bitcoin_macro_indicators_range
# intialisation du logger
name_module= os.path.basename(__file__).split(".")[0]  # Récupère le nom du fichier sans l'extension

# Set le logger du module en cours
logger= setup_logger(name_module)

# Connecter à la base de données MongoDB
db = client[MONGO_DB]
logger.info(f"Connexion de la base de données Mongo établie avec succès : {MONGO_DB}")

# Set le nom de la collection
collection = db["collection_name"]  # Remplacez "collection_name" par le nom de votre collection

def get_number_of_articles(db, start_date: date, end_date: date)-> int:
    """
    Récupère le nombre d'articles financiers contenant le mot "bitcoin" publiés entre deux dates données.

    Args:
        db (client): Client MongoDB actif.
        start_date (str): Date de début au format YYYY-MM-DD.
        end_date (str): Date de fin au format YYYY-MM-DD.

    Returns:
        int: Nombre d'articles trouvés.
    """
   
    # Vérification des dates
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        logger.error("Les dates doivents être des objets de types 'date'.")
        raise ValueError("Les dates doivents être des objets de types 'date'. Veuillez vérifier les paramêtres fournis et réessayer.")
    
    """# Parse les dates de début et de fin avant de les
    start_date = datetime.combine(start_date, datetime.min.time())
    end_date = datetime.combine(end_date, datetime.max.time())
"""

    # Essayer de récupérer les articles financiers contenant le mot "bitcoin"
    # entre les dates de début et de fin
    try:
        start_str = start_date.strftime("%Y-%m-%d")
        end_str = end_date.strftime("%Y-%m-%d")

        collection = db["articles_financiers"]

        query = {
            "Date of publication": {"$gte": start_str, "$lte": end_str},
            "Content": {"$regex": "bitcoin", "$options": "i"}
        }

        count = collection.count_documents(query)
        logger.info(f"{count} articles trouvés entre {start_str} et {end_str}.")
        return count

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des articles : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des articles.")
    
def get_articles_btc_macroRates_by_date_range(pg_db, db_mongo, start_date: date, end_date: date) -> CorrelatedResponse:
    """ Cette fonction permet de récupérer le nombre d'articles contenant le mot "bitcoin, ainsi que les prix du bitcoin et les indicateurs macroéconomiques (inflation, chômage, M3, MRO) pour une période donnée.
        Elle est utilisée pour fournir un aperçu croisé de l'évolution des facteurs économiques et de l'intensité médiatique autour du Bitcoin, en vue de futures analyses de corrélation ou de prédiction.
    
    Returns:
        list: le nombre d'article ainsi que les prix du bitcoin et les indicateurs macroéconomiques pour une période donnée.
    """
    """# Connexion à la base de données PostgreSQL
    pg_db: Session = SessionLocal()"""
 
    # Vérification des dates
    if not isinstance(start_date, date) or not isinstance(end_date, date):
        logger.error("Les dates doivent être des objets de types 'date'.")
        raise ValueError("Les dates doivent être des objets de types 'date'. Veuillez vérifier les paramètres fournis et réessayer.")   
    
    # Récupération des données aggregées de la vue PostgreSQL et du nombre d'articles dans MongoDB dans une période donnée
    try:
        # Connexion à la base de données MongoDB
        db_mongo = client[MONGO_DB]

        btc_and_macroRates = get_bitcoin_macro_indicators_range(pg_db,start_date, end_date)
        count_articles = get_number_of_articles(db_mongo, start_date, end_date)
        logger.info(f"Nombre d'articles contenant 'bitcoin' : {count_articles}")
        logger.info(f"Connexion de la base de données PostgreSQL établie avec succès.")
        logger.info(f"Les données récupérées : {btc_and_macroRates}")

        results =[
                    BtcIndicatorsArticlesResponse(
                        day=row[0],
                        close_price_bitcoin=row[1],
                        rate_mro=row[2],
                        inflation_rate=row[3],
                        unemployment_rate=row[4],
                        monetary_m3_rate=row[5]
                    )
                    for row in btc_and_macroRates
                 ]
        
        return  CorrelatedResponse(
                    article_count=count_articles,
                    results=results
                )

    except Exception as e:
        logger.error(f"Erreur réelle : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des données")    
    finally:
        pg_db.close()


if __name__ == "__main__":
    # Exemple d'utilisation de la fonction  
    from datetime import date
    from database.conn_db.connect_mongodb import client, MONGO_DB
    db = client[MONGO_DB]  
    print(f"Connexion de la base de données Mongo établie avec succès : {MONGO_DB}")
    getArticle = db["articles_financiers"]
    print("Nombre total d'articles dans la collection :", getArticle.count_documents({}))
    count = get_number_of_articles(db, date(2022, 12, 31), date(2023, 1, 31))
    print(f"Nombre d'articles contenant 'bitcoin' : {count}")

    # Exemple d'utilisation de la fonction get_articles_btc_macroRates_by_date_range
    db_pg : Session = SessionLocal()
    print("Connexion de la base de données PostgreSQL établie avec succès.")
    datas = get_articles_btc_macroRates_by_date_range(db_pg,db, date(2022,12,31), date(2023, 1, 31 ))
    print(f"Les données récupérer : {datas}")