# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..", "..")))

from database.conn_db.connect_mongodb import client, MONGO_DB
from api.schemas.articles_financiers import ArticlesFinanciersResponse
from api.crud.crud_articles_financiers import get_all_articles, get_article_by_id, collection_articlesFinanciers
from setup.logger_config import setup_logger

# Mise en place d'un logger pour le module
name_file = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(name_file)

# Connexion à la base de données MongoDB
mongo_db = client[MONGO_DB]

def test_read_all_articles():
    articles = get_all_articles(collection_articlesFinanciers)
    logger.info(f"Nombre d'articles récupérés : {len(articles)}")
    if articles:
        logger.info(f"Premier article : {articles[0].title} publié le {articles[0].published_at}")


def test_read_article_by_id():
    articles = get_all_articles(collection_articlesFinanciers)
    if not articles:
        logger.info("Aucun article disponible pour le test.")
        return
    first_id = str(articles[0].id)
    article = get_article_by_id(collection_articlesFinanciers, first_id)
    if article:
        logger.info(f"Article récupéré : {article.title} depuis l'ID {first_id}")
    else:
        logger.info("Échec de récupération de l'article par ID")

if __name__ == "__main__":
    test_read_all_articles()
    test_read_article_by_id()