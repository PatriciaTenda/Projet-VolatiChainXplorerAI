# Formalisation du besoin de prédiction

VolatiChainXplorerAI a pour objectif de prédire la volatilité future du Bitcoin à deux horizons : **7 jours** et **30 jours**.

La prédiction repose sur des données historiques du Bitcoin ainsi que sur des indicateurs macroéconomiques préparés lors de la phase de traitement des données.

Le problème est traité comme un problème de prévision sur séries temporelles à partir de données numériques.

L’objectif est d’obtenir une **estimation de la volatilité future** permettant d’informer l’utilisateur sur l’évolution probable du niveau de volatilité du Bitcoin.

Les modèles devront être évalués dans un cadre temporel respectant l’ordre chronologique des observations afin **d’éviter toute fuite d’information entre les données d’entraînement et les données futures**.