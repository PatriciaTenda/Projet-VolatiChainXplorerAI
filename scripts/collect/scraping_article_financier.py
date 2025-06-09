# Charger les bibliothèques nécessaires
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import requests
import dateparser
import json
import os
import re
from slugify import slugify

# Definir l'URL de la page à scraper
url_1 = "https://cryptoast.fr/consolider-epargne-melant-or-bitcoin-btc-gold-avenue/"
url_2 = "https://cryptoast.fr/predire-evolution-bitcoin-modele-stock-to-flow/"
url_3 = "https://cryptoast.fr/retrospective-crypto-2022-evenements-marquants-ecosysteme-cryptomonnaies/"
url_4 = "https://cryptoast.fr/analyse-on-chain-bitcoin-btc-distribution-inedite-offre/"
url_5= "https://cryptoast.fr/bitcoin/" 
url = "https://fr.cointelegraph.com/news/btc-volatility-low-stablecoin-transaction-tops-visa-ark"

# Définir les en-têtes pour simuler un navigateur
headers = { 
        "User-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        }

# Envoyer une requête GET à l'URL
response = requests.get(url, headers = headers, )

# Vérifier le statut de la réponse
print(response.status_code)

soup = BeautifulSoup(response.content, "lxml")

# Extraction des données nécessaires
title = soup.find("h1", class_="article-title" ).get_text(strip=True) # Récupérer le titre de l'article

#======= Traitement de la date et de l'auteur =======
# Extraction de la date et de l'auteur
date_and_author_div = soup.find("div", class_="article-date-and-author")  # Trouver la div contenant la date et l'auteur


#======= Date de publication =======
# Récupérer la date de publication
date_and_read_time_div = date_and_author_div.find("div", class_="d-flex date-and-read-time flex-column")
date_div = date_and_read_time_div.find("div", class_ = "d-flex flex-row align-items-center date")
date_tag = date_div.find("p", class_="ms-2") 
#print(f"Date tag: {date_tag}")  # Afficher le tag de la date pour le débogage

raw_date = date_tag.get_text(strip=True) if date_tag else None 
#print(f"Raw date: {raw_date}")  # Afficher la date brute pour le débogage

# Utiliser une expression régulière pour extraire la date
pattern = r"\b(?:Modifié|Publié)\s+le\s+(\d{1,2}\s+\w+\s+\d{4})\.?\b"
date_match = re.search(pattern, raw_date, flags=re.IGNORECASE)
#print(f"Date match: {date_match}")  # Afficher le match de la date pour le débogage

# Si la date est trouvée, on la formate
if date_match:
    date_str_brut = date_match.group(1)
    print(f"Date string brut: {date_str_brut}")  # Afficher la date brute pour le débogage
    try:
        # Convertir la date en format ISO 8601
        date_parsed = dateparser.parse(date_str_brut, languages=['fr'], settings={'DATE_ORDER': 'DMY'}) 
        print(f"Parsed date: {date_parsed}")  # Afficher la date parsée pour le débogage
        date = date_parsed.strftime("%Y-%m-%d")  # Convertir la date en chaîne de caractères au format ISO 8601
    except Exception:
        date = "Date inconnue, erreur de parsing"
else:
    date = "Date inconnue, erreur de parsing"

print(f"Parsed date: {date}")  # Afficher la date parsée pour le débogage


#======= Nom de l'auteur =======
# Récupérer le nom de l'auteur
author_tag = date_and_author_div.find("a") 
author = author_tag.get_text(strip=True) if author_tag else "Auteur inconnu"  


#======= CONTENU DE L'ARTICLE =======
# Récupérer le contenu de l'article
content_div = soup.find("div", class_="article-content")
elements = content_div.find_all(["h2", "p"]) if content_div else []
trash_keywords = ["codecryptoast", "ouvrez votre compte","copié", "30 € de réduction", "inscrivez-vous", 
            "🔥", "figure", "lire aussi", "visionnez", "réduction", 
            "1436 articles", "feed/", "partenaire nous reverse" "🎥", "affiliés", "👌", "💡", "👉"]
# Nettoyer le contenu pour enlever les espaces, les caractères , les parties de texte inutiles
content_structured_flat = ""
current_section = ""
parsing_section = False  # Indicateur pour savoir si on est dans une section
for tag in elements:
    text = tag.get_text(strip=True)
    if any(x in text.lower() for x in trash_keywords):
        continue
    # Gestion des titres h2 → début d'une section
    if tag.name == "h2":
        parsing_section = True
        current_section = text.strip().upper()
        content_structured_flat += f"\n\n{current_section}\n"
        continue

    # On ne garde les <p> que si on est dans une section
    if tag.name == "p" and parsing_section:
        if len(text) >= 30:
            content_structured_flat += text + "\n"

# Nettoyage final du contenu
content_structured_flat = content_structured_flat.strip()
#print(f"Contenu structuré (premiers 500 caractères): {content_structured_flat}")  # Afficher les 500 premiers caractères du contenu structuré
#print(len(content_structured_flat))  # Afficher la longueur du contenu structuré
# Enregistrer les données dans un document JSON
article = {
    "Title": title, 
    "url": url,
    "Author": author,    
    "Date of publication": date,
    "Content": content_structured_flat,
    "scraped_at":datetime.now(timezone.utc).isoformat()  # Date et heure de l'extraction
}

def save_to_json(article, filename):
    """Enregistrer les données dans un fichier JSON."""
    # Créer le dossier si il n'existe pas
    os.makedirs(os.path.dirname(filename), exist_ok=True)    # Enregistrer le document JSON dans un fichier
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(article, f, indent=2, ensure_ascii=False)
    # Confirmer la création du document
    print("Document financicier cryptoast json crées avec succès.")


# ===== EXECUTION DU SCRIPT =====
if __name__ == "__main__":
    # Nom du fichier JSOn
    filename = "data/raw/articles_financiers/artcile_financier_cryptoast_6.json"
    # Enregister les données dans le fichier JSON
    save_to_json(article, filename)
# Fin du script 