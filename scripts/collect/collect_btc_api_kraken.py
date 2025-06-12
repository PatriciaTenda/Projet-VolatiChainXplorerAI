# Retrieve 5m OHLC data on BTC/USD.
"""
Récupère les données OHLC (Open, High, Low, Close) en intervalle de 5 minutes pour la paire BTC/EUR depuis l'API publique de Kraken,
les convertit en DataFrame pandas, ajoute une colonne datetime, affiche les 100 premières lignes, puis sauvegarde les données dans un fichier CSV.
Étapes principales :
- Envoie une requête GET à l'endpoint public OHLC de Kraken pour BTC/EUR avec un intervalle de 5 minutes.
- Décode la réponse JSON et extrait les données OHLC.
- Crée un DataFrame pandas avec les données extraites et ajoute une colonne datetime.
- Affiche les 100 premières lignes du DataFrame.
- Sauvegarde le DataFrame dans un fichier CSV à l'emplacement 'data/raw/btc_api_kraken.csv'.
"""
# Endpoint does not require authentication,
# but has utility functions for authentication.

import http.client
import urllib.request
import urllib.parse
import hashlib
import hmac
import base64
import json
import time
import pandas as pd

# 
def request(method: str = "GET", path: str = "", query: dict | None = None, body: dict | None = None, public_key: str = "", private_key: str = "", environment: str = "") -> http.client.HTTPResponse:
   url = environment + path
   query_str = ""
   if query is not None and len(query) > 0:
      query_str = urllib.parse.urlencode(query)
      url += "?" + query_str
   nonce = ""
   if len(public_key) > 0:
      if body is None:
         body = {}
      nonce = body.get("nonce")
      if nonce is None:
         nonce = get_nonce()
         body["nonce"] = nonce
   headers = {}
   body_str = ""
   if body is not None and len(body) > 0:
      body_str = json.dumps(body)
      headers["Content-Type"] = "application/json"
   if len(public_key) > 0:
      headers["API-Key"] = public_key
      headers["API-Sign"] = get_signature(private_key, query_str+body_str, nonce, path)
   req = urllib.request.Request(
      method=method,
      url=url,
      data=body_str.encode(),
      headers=headers,
   )
   return urllib.request.urlopen(req)

def get_nonce() -> str:
   return str(int(time.time() * 1000))

def get_signature(private_key: str, data: str, nonce: str, path: str) -> str:
   return sign(
      private_key=private_key,
      message=path.encode() + hashlib.sha256(
            (nonce + data)
         .encode()
      ).digest()
   )
 
def sign(private_key: str, message: bytes) -> str:
   return base64.b64encode(
      hmac.new(
         key=base64.b64decode(private_key),
         msg=message,
         digestmod=hashlib.sha512,
      ).digest()
   ).decode()

# Fonction qui permet de récupérer les données de l'API Kraken
def main():
   response = request(
      method="GET",
      path="/0/public/OHLC",
      query={
         "pair": "BTC/EUR",
         "interval": 5,
      },
      environment="https://api.kraken.com",
   )

   # Récupération des données HTTPResponse en string
   response_string = response.read().decode()

   # Transformation des données au format JSON
   data = json.loads(response_string)
   print(type(data))
   print(data.keys())
   data_result = data["result"]
   btc_eur = data_result["BTC/EUR"]

   column_names = [
    'timestamp', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'] # liste de Colonnes
   
   # Création d'un DataFrame pandas à partir des données OHLC récupérées
   df_btc = pd.DataFrame(btc_eur, columns= column_names)
   #print(df_btc.head())
   df_btc["datetime"] = pd.to_datetime(df_btc["timestamp"], unit="s")
   print(df_btc.head(100))

   filename = "data/raw/btc_api_kraken.csv"   # path du fichier csv
   
   with open(filename, "w", encoding="utf-8") as f:# sauvegarde des données dans un fichier csv
      df_btc.to_csv(filename, sep=",")

if __name__ == "__main__":
   main()