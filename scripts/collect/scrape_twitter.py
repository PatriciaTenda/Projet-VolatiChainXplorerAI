"""Script to scrape data from X(formely Tweetter) site without using the API.
This script collects tweets from a specific user and saves them in a JSON file.
La librairie snscrape est utilisée  dans un environnement python à partir de la version 3.11 et descendante. 
"""
# Chargez les bibliothèques nécessaires
import snscrape.modules.twitter as sntwitter
import json, os 

# ===== SET LES PARAMETRES DE LA REQUETE ======
# Definir la requête pour récupérer les tweets
query = '(bitcoin volatilité OR "volatilité du bitcoin") ("depuis 2018" OR "en 2024" OR "en 2023" OR "en 2022") lang:fr -is:retweet'
# Autres paramètres de la requête
min_likes = 20  # Nombre minimum de likes pour filtrer les tweets
lang = "fr"  # Langue des tweets à récupérer
since_year = 2018  # Année de début pour les tweets
until_year = 2024  # Année de fin pour les tweets
json_name = "tweets_btc_volatilities_2018_2024"  # Nom du fichier JSON

# ===== FIN DES PARAMETRES DE LA REQUETE ======

search_query = f"{query} min_retweets:0 min_faves:{min_likes} lang:{lang} since:{since_year}-01-01 until:{until_year}-12-31"

# Spécifier le chemin du fichier JSON pour enregistrer les tweets
filename = f"data/rawa/tweets/{json_name}.jsonl"  # Chemin du fichier JSON

# Créer le répertoire nécessaire
os.makedirs(os.path.dirname(filename), exist_ok=True)

# Récupérer les tweets en utilisant snscrape
with open (filename, "w", encoding = "utf-8") as f:
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_query).get_items()):
        if i >=200:  # Limiter le nombre de tweets à 200
            break
        # Extraction des informations pertinentes du tweet
        tweet_data = {
        "Id": tweet.id,
        "content": tweet.content,
        "Likes": tweet.likeCount,
        "Retweets": tweet.retweetCount,
        "Date": tweet.date.isoformat(),
        "Created_at": tweet.date.isoformat(),
        "raw_content": tweet.rawContent,
        "replies_count": tweet.replyCount,
        "retweeted_count": tweet.retweetCount,
        "likes_count": tweet.likeCount,
        "hashtags": tweet.hashtags,
        "cash_tags": tweet.cashtags if tweet.cashtags else [],  # Vérifier si les cashtags existent
        "Language": tweet.lang,
        "link": tweet.url,
        "conversation_id": tweet.conversationId,
        "jahr": tweet.date.year,
        "monat": tweet.date.month,
        "tag": tweet.date.day,
        "time": tweet.date.time().isoformat(),
        "user_id": tweet.user.id,
        "user_name": tweet.user.username,
    }  
        
        f.write(json.dumps(tweet_data, ensure_ascii=False) + "\n")  # Écrire le tweet dans le fichier JSON