# Étude de H2O AutoML

## Positionnement

H2O AutoML est une solution d’Automated Machine Learning destinée à automatiser l’entraînement, l’optimisation et la comparaison de plusieurs modèles de machine learning supervisé.

Elle est accessible notamment depuis Python.

## Automatisation

L’utilisateur fournit principalement :
- les données d’entraînement ;
- les variables explicatives ;
- la variable cible ;
- éventuellement une limite de temps ou un nombre maximal de modèles.

H2O AutoML entraîne ensuite automatiquement plusieurs modèles et génère un leaderboard permettant de les classer.

Parmi les familles utilisées figurent notamment des modèles tels que :
- GLM ;
- Random Forest ;
- GBM ;
- XGBoost ;
- Deep Learning ;
- Stacked Ensembles.

## Séries temporelles

H2O AutoML n’est pas présenté dans sa documentation comme un framework de forecasting temporel natif comparable au module Time Series de PyCaret.

Pour VolatiChainXplorerAI, l’utilisation la plus naturelle serait donc de lui fournir le problème déjà transformé en régression supervisée :

variables disponibles à la date t
→
volatilité future à 7 jours ou 30 jours.

Le respect de la chronologie et la préparation des données devraient alors être maîtrisés par notre propre pipeline.

## Évaluation

Pour un problème de régression, H2O produit un leaderboard contenant plusieurs métriques, notamment RMSE, MSE et MAE.

Le leaderboard peut également afficher le temps d’entraînement et le temps nécessaire pour effectuer une prédiction.

## Interprétabilité

H2O propose des outils d’explication des modèles.

Les objets AutoML peuvent être analysés avec des fonctions permettant notamment d’obtenir :
- importance des variables ;
- partial dependence plots ;
- comparaison de plusieurs modèles ;
- explications du modèle leader.

Cet aspect est intéressant pour VolatiChainXplorerAI, qui doit pouvoir fournir une justification compréhensible du modèle retenu.

## Exécution

H2O peut fonctionner localement et dispose d’une interface Python.

Son utilisation dans Docker est également documentée.

Cela correspond aux contraintes techniques du projet.

## Intérêt pour VolatiChainXplorerAI

H2O AutoML permettrait de tester automatiquement plusieurs modèles de régression sur les datasets 7 jours et 30 jours déjà préparés.

Il constitue donc une approche différente de PyCaret :

PyCaret peut traiter directement le forecasting temporel.

H2O peut traiter notre dataset après transformation du problème temporel en régression supervisée.

## Points de vigilance

La validation temporelle et l’absence de fuite d’information devront être maîtrisées explicitement dans notre pipeline.

H2O ne doit donc pas être utilisé comme un AutoML classique avec un découpage aléatoire des observations.

## Conclusion provisoire

H2O AutoML reste pertinent pour le benchmark.

Son intérêt principal est sa capacité à automatiser l’entraînement et la comparaison de plusieurs modèles de régression tout en offrant un bon niveau d’explicabilité.

Il est cependant moins directement spécialisé dans le forecasting temporel que PyCaret.