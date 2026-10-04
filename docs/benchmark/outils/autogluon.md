# Étude de AutoGluon Time Series

## Positionnement

AutoGluon est un framework AutoML open source proposant un module spécifiquement consacré au forecasting de séries temporelles.

Son composant TimeSeriesPredictor automatise l’entraînement, l’optimisation, la sélection et la comparaison de plusieurs modèles de forecasting.

## Séries temporelles

AutoGluon prend directement en charge le forecasting multi-horizon.

L’utilisateur définit notamment :
- la cible ;
- la fréquence temporelle ;
- l’horizon de prédiction ;
- la métrique d’évaluation.

Le framework peut ensuite entraîner plusieurs catégories de modèles.

## Modèles

AutoGluon Time Series peut notamment combiner :
- modèles statistiques tels que ETS ;
- modèles basés sur LightGBM ;
- modèles Deep Learning ;
- modèles préentraînés de forecasting tels que Chronos ;
- ensembles de plusieurs modèles.

## Évaluation

AutoGluon produit automatiquement un leaderboard permettant de comparer les modèles entraînés.

Le leaderboard peut présenter :
- score de validation ;
- score de test ;
- temps d’entraînement ;
- temps de prédiction.

## Prévisions

AutoGluon produit également des prévisions probabilistes.

Il peut donc fournir non seulement une valeur moyenne attendue, mais également plusieurs quantiles représentant l’incertitude autour de la prévision.

## Intérêt pour VolatiChainXplorerAI

AutoGluon est particulièrement intéressant car il combine :

- forecasting natif ;
- AutoML ;
- modèles classiques ;
- machine learning ;
- deep learning ;
- modèles préentraînés ;
- ensembles ;
- fonctionnement Python.

L’article Westergaard et al. (2024) l’a également comparé à PyCaret sur un dataset Bitcoin.

## Point de vigilance

Les modèles les plus complexes peuvent nécessiter davantage de mémoire, de stockage et de temps de calcul.

Il faudra donc vérifier si les configurations retenues restent compatibles avec les ressources locales du projet.

## Conclusion provisoire

AutoGluon mérite d’être ajouté aux solutions sérieusement considérées pour le benchmark final.

Sa spécialisation actuelle dans le forecasting et la diversité de ses modèles en font un concurrent direct de PyCaret pour VolatiChainXplorerAI.