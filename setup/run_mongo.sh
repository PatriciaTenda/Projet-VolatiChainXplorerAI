#!/bin/bash

# Script Bash pour exécuter la commande Docker et créer le conteneur MongoDB

# Se placer à la racine du projet pour que le .env soit trouvé
cd "$(dirname "$0")/.."

# Charger les variables d’environnement depuis le fichier .env
export $(grep -v '^#' .env | xargs)

# Supprimer un éventuel ancien conteneur du même nom
docker rm -f mongo_VolatiChainXplorerAI 2>/dev/null

# Lancer le conteneur PostgreSQL
docker run --name mongo_VolatiChainXplorerAI \
  -e MONGO_INITDB_ROOT_USERNAME=$MONGO_USER \
  -e MONGO_INITDB_ROOT_PASSWORD=$MONGO_PASSWORD \
  -e MONGO_INITDB_DATABASE=$MONGO_DB \
  -p $MONGO_PORT:27017 \
  -v mongo_data:/data/db \
  -d mongo:latest

# Massage de confirmation du lancement du conteneur
if [ $? -eq 0 ]; then
  echo "Conteneur MongoDB lancé avec succès sur le port $MONGO_PORT"
else
  echo "Échec du lancement de MongoDB" >&2
  exit 1
fi
