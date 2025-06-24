# Charger les librairies nécessaires
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi import APIRouter, HTTPException
from api.crud.crud_articles_financiers import (
    get_all_articles,
    get_article_by_id,
    collection_articlesFinanciers,
)
from api.schemas.articles_financiers import ArticlesFinanciersResponse
from setup.logger_config import setup_logger

# Mise en place d'un logger pour le module de création des collections
name_file =os.path.splitext(os.path.basename(__file__))[0]
# set le logger du module en cours
logger = setup_logger(name_file)


# Création du routeur pour les endpoints liés aux articles financiers
router = APIRouter(
    prefix="/articles-financiers",  # Préfixe pour toutes les routes de ce routeur
    tags=["Financial articles"]  # Étiquette utilisée pour la documentation Swagger
)

@router.get("/", response_model=list[ArticlesFinanciersResponse])
def read_all_articles():
    """
    Endpoint pour récupérer l'ensemble des articles financiers.

    Cette route interroge la base de données MongoDB et retourne
    tous les articles triés par date de publication décroissante.

    Returns:
        list[ArticlesFinanciersResponse]: Liste des articles financiers disponibles.
    
    Raises:
        HTTPException: Erreur 500 en cas de problème lors de la récupération.
    """
    try:
        articles = get_all_articles(collection_articlesFinanciers)
        logger.info(f"{len(articles)} article(s) renvoyé(s) via l'API.")
        return articles
    except Exception as e:
        logger.error(f"Erreur serveur : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur : {str(e)}")

@router.get("/{article_id}", response_model=ArticlesFinanciersResponse)
def read_article_by_id(article_id: str):
    """
    Endpoint pour récupérer un article spécifique à partir de son identifiant MongoDB.

    Args:
        article_id (str): L'identifiant unique (ObjectId) de l'article dans la base.

    Returns:
        ArticlesFinanciersResponse: L'article correspondant à l'identifiant fourni.
    
    Raises:
        HTTPException: 
            - 404 si aucun article ne correspond à l'ID.
            - 500 en cas d'erreur interne.

    Exemple d'ID pour les tests : 68555b524f355205f0bad159
    """
    try:
        logger.info(f"Tentative de récupération de l'article avec l'ID : {article_id}")
        article = get_article_by_id(collection_articlesFinanciers, article_id)
        
        if not article:
            logger.warning(f"Aucun article trouvé avec l'ID : {article_id}")
            raise HTTPException(status_code=404, detail="Article non trouvé")
        
        logger.info(f"Article récupéré avec succès : {article.title}")
        return article

    except Exception as e:
        logger.error(f"Erreur serveur lors de la récupération de l'article : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur serveur : {str(e)}")
