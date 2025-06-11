""" Script to scrape data from the X API (formerly Twitter API).
    This script collects tweets from a specific user and saves them in a JSON file. 
"""
# Importer les bibliothèques nécessaires
import os
from dotenv import load_dotenv
import json, time
import tweepy
from tweepy.errors import TooManyRequests
from datetime import timezone, datetime, timedelta

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer les variables d'environnement
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Vérifier si le token est défini
if not BEARER_TOKEN:
    raise ValueError(" Le BEARER_TOKEN n'est pas défini dans le fichier .env.")

# Autentification avec le token bearer
client = tweepy.Client(bearer_token= BEARER_TOKEN)
print("Authentification réussie avec le token bearer.")

# Requête de récupération des tweets
query = '(bitcoin volatilité OR "volatilité du bitcoin") lang:fr -is:retweet'
# Note: Le paramètre 'lang:fr' est utilisé pour filtrer les tweets en français.
# Le paramètre '-is:retweet' est utilisé pour exclure les retweets.

now = datetime.now(timezone.utc)  # Date et heure actuelles
start_time = (now - timedelta(days=7))  # Date et heure de début (7 jours avant la date actuelle)
end_time = now - timedelta(seconds=10) # Date et heure de fin (10 secondes avant la date actuelle)
# Effectuer la requête pour récuperer les tweets
# Note: En cas de trop nombreuses requêtes, le script attend 15 minutes avant de réessayer.

# Gestion des exceptions pour les requêtes trop nombreuses
tweets = None  # Initialiser la variable tweets
try :
    tweets = client.search_recent_tweets(
        query = query,
        max_results = 10,  # Nombre maximum de tweets à récupérer
        start_time = start_time.isoformat() ,  # Date de début
        end_time = end_time.isoformat(),  # Date de fin
        tweet_fields = ["created_at", "text", "author_id", "public_metrics"],  # Champs des tweets à récupérer
    )
except TooManyRequests as e:
    print("Trop de requêtes, attente de 15 minutes avant de réessayer...")
    time.sleep(15 * 60)
    # Réessayer la requête après 15 minutes
    tweets = client.search_recent_tweets(
        query=query,
        max_results=10,
        start_time=start_time.isoformat(),
        end_time=end_time.isoformat(),
        tweet_fields=["created_at", "text", "author_id", "public_metrics"]
    )
except Exception as e:
    print(f"Erreur lors de la récupération des tweets: {e}")

# Chemin du fichier JSON pour enregistrer les tweets
filename ="data/raw/tweets/tweets_bitcoin_volatilities.jsonl"  # Chemin du fichier JSON
os.makedirs(os.path.dirname(filename), exist_ok=True)  # Créer le répertoire si nécessaire

# Enregistrer les tweets dans un document JSON
with open (filename, "w", encoding="utf-8") as f:
    # Vérifier si des tweets ont été récupérés
    if tweets and tweets.data :
        print(f"Nombre de tweets récupérés: {len(tweets.data)}")
        for tweet in tweets.data:
            # Créer un document pour chaque tweet
            document = {
                "id": tweet.id,
                "text": tweet.text,
                "author_id": tweet.author_id,
                "public_metrics": tweet.public_metrics,
                "Date of publication": tweet.created_at.isoformat(),  # Date de publication du tweet
                "created_at": datetime.now(timezone.utc).isoformat() # Date et heure de l'extraction
            }
        f.write(json.dumps(document, ensure_ascii= False)+"\n")
    else:
        print("Aucun tweet trouvé pour la requete spécifiée.")
        
print(f"Les tweets ont été enregistrés dans le fichier {filename}.")
# Fin du script
