# Charger les librairies nécessaires
import os
import sys
# Ajouter le dossier racine au PATH pour les imports relatifs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pymongo.collection import Collection
from bson import ObjectId
from api.schemas.articles_financiers import ArticlesFinanciersResponse
from database.conn_db.connect_mongodb import client, MONGO_DB
from setup.logger_config import setup_logger

# Mise en place d'un logger pour le module
name_file = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(name_file)

# Connexion à la base de données MongoDB
mongo_db = client[MONGO_DB]

# Accès à la collection des articles financiers
collection_articlesFinanciers = mongo_db["articles_financiers"]



# Récupère tous les articles de la collection MongoDB
def get_all_articles(collection: Collection) -> list[ArticlesFinanciersResponse]:
    """
    Récupère tous les articles financiers stockés dans la base MongoDB,
    triés par date de publication décroissante (plus récents d'abord).

    Args:
        collection (Collection): La collection MongoDB contenant les articles.

    Returns:
        list[ArticlesFinanciersResponse]: Liste des articles sous forme d'objets Pydantic.
    """
    articles_cursor = collection.find().sort("published_at", -1)  # -1 = tri descendant
    articles = []

    for doc in articles_cursor:
        # On convertit chaque document MongoDB (dict) en objet Pydantic
        article = ArticlesFinanciersResponse(**doc)  # **doc décompose les paires clé-valeur du dictionnaire MongoDB
                                                     # et les passe en tant qu'arguments nommés à Pydantic → ArticlesFinanciersResponse(**doc)                                         
        articles.append(article)
    logger.info(f"{len(articles)} articles récupérés avec succès.")
    return articles

# Récupère un article unique par son identifiant MongoDB
def get_article_by_id(collection: Collection, article_id: str) -> ArticlesFinanciersResponse | None:
    """
    Récupère un article unique à partir de son ID MongoDB.

    Args:
        collection (Collection): La collection MongoDB contenant les articles.
        article_id (str): L'identifiant de l'article (format ObjectId).

    Returns:
        ArticlesFinanciersResponse | None: L'article trouvé, ou None si aucun résultat.
    """
    try:
        doc = collection.find_one({"_id": ObjectId(article_id)})
        logger.info("Les articles ont été récupérés avec succès.")
        if doc:
            return ArticlesFinanciersResponse(**doc)
        return None
    except Exception as e:
        if not ObjectId.is_valid(article_id):
            logger.error(f"ID invalide : {article_id}")
        return None
       
