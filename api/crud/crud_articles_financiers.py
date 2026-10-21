# Charger les librairies nécessaires
import os
import sys

# Ajouter le dossier racine au PATH pour les imports relatifs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from bson import ObjectId
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from api.schemas.articles_financiers import ArticlesFinanciersResponse
from database.conn_db.connect_mongodb import MONGO_DB, client
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
    if not ObjectId.is_valid(article_id):
        logger.warning("ID invalide : %s", article_id)
        return None

    try:
        doc = collection.find_one({"_id": ObjectId(article_id)})
    except PyMongoError:
        logger.exception("Erreur MongoDB pour l'article %s", article_id)
        raise

    if doc is None:
        logger.info("Aucun article trouvé pour l'ID %s", article_id)
        return None

    logger.info("Article %s récupéré avec succès", article_id)
    return ArticlesFinanciersResponse(**doc)
       
