# Charger les bibliothèques nécessaires
from datetime import datetime, timezone
from bs4 import BeautifulSoup
import requests
import dateparser
import json
import os
from slugify import slugify

# Definir l'URL de la page à scraper
url = "https://cryptoast.fr/consolider-epargne-melant-or-bitcoin-btc-gold-avenue/"

# Définir les en-têtes pour simuler un navigateur
headers = { 
        "User-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        }

# Envoyer une requête GET à l'URL
response = requests.get(url, headers = headers, )
# Vérifier le statut de la réponse
print(response.status_code)
#print(response.text[:500])  # Afficher les 500 premiers caractères de la réponse
# Set le contenu de la réponse dans BeautifulSoup pour le parser
soup = BeautifulSoup(response.content, "lxml")

# Extraction des données nécessaires
title = soup.find("h1", class_="article-title" ).get_text(strip=True) # Récupérer le titre de l'article

# Extraction de la date et de l'auteur
date_and_author_div = soup.find("div", class_="article-date-and-author")  # Trouver la div contenant la date et l'auteur

 # Récupérer la date de publication
date_and_read_time_div = date_and_author_div.find("div", class_="d-flex date-and-read-time flex-column")
date_tag = date_and_read_time_div.find("p", class_="ms-2") 
raw_date = date_tag.get_text(strip=True) if date_tag else None 
date_parse = dateparser.parse(raw_date) if raw_date else None  # Convertir la date en objet datetime
date = date_parse.date().isoformat() if date_parse else "Date inconnue"  # Formater la date en ISO 8601

# Récupérer le nom de l'auteur
author_tag = date_and_author_div.find("a") 
author = author_tag.get_text(strip=True) if author_tag else "Auteur inconnu"  

# Récupérer le contenu de l'article
content_div = soup.find("div", class_="article-content")
elements = content_div.find_all(["h2", "p"]) if content_div else []
trash_keywords = ["codecryptoast", "ouvrez votre compte","copié", "30 € de réduction", "inscrivez-vous", 
            "🔥", "figure", "lire aussi", "visionnez", "réduction", 
            "1436 articles", "feed/", "partenaire nous reverse" "🎥", "affiliés", "👌", "💡"]
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
print(f"Contenu structuré (premiers 500 caractères): {content_structured_flat}")  # Afficher les 500 premiers caractères du contenu structuré
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
    filename = "data/raw/articles_financiers/artcile_financier_cryptoast.json"
    # Enregister les données dans le fichier JSON
    save_to_json(article, filename)
# Fin du script