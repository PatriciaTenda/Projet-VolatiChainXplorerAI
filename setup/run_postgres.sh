#!/bin/bash

# Script Bash pour exécuter la commande Docker et créer le conteneur PostgreSQL

# Se placer à la racine du projet pour que le .env soit trouvé
cd "$(dirname "$0")/.."

# Charger les variables d’environnement depuis le fichier .env
export $(grep -v '^#' .env | xargs)

# Supprimer un éventuel ancien conteneur du même nom
docker rm -f VolatiChainXplorerAI_postgres 2>/dev/null

# Lancer le conteneur PostgreSQL
docker run --name VolatiChainXplorerAI_postgres \
  -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
  -e POSTGRES_USER=$POSTGRES_USER \
  -e POSTGRES_DB=$POSTGRES_DB \
  -p $POSTGRES_PORT:5432 \
  -v postgres-data:/var/lib/postgresql/data \
  -d postgres:latest
