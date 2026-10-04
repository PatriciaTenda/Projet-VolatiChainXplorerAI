# Étude de PyCaret

## Positionnement

PyCaret est une bibliothèque Python open source et low-code permettant d’automatiser une partie importante du workflow de machine learning.

Elle permet notamment de préparer un environnement d’expérimentation, entraîner plusieurs modèles, comparer leurs performances, optimiser certains modèles, effectuer des prédictions et sauvegarder le modèle retenu.

## Automatisation

PyCaret permet de comparer automatiquement plusieurs modèles avec `compare_models()` et de classer leurs performances selon une métrique choisie.

L’utilisateur garde cependant la responsabilité de définir :
- la cible ;
- l’horizon de prédiction ;
- la stratégie de validation ;
- les données utilisées ;
- les métriques pertinentes ;
- l’interprétation finale des résultats.

## Séries temporelles

PyCaret possède un module spécifique `time_series`.

Il permet de définir un horizon de prévision avec `fh`, d’entraîner plusieurs modèles de forecasting, de les comparer, de produire des prévisions et de sauvegarder le modèle final.

PyCaret est donc capable de traiter directement un problème de forecasting temporel, sans nécessairement transformer le problème en régression classique.

## Validation temporelle

Le module Time Series prend en compte la structure temporelle des données.

Ce point est important pour VolatiChainXplorerAI puisque les observations passées doivent servir à prédire des observations futures sans mélange aléatoire entre passé et futur.

## Intérêt pour VolatiChainXplorerAI

PyCaret présente plusieurs avantages :

- fonctionnement en Python ;
- possibilité d’exécution locale ;
- caractère open source ;
- approche low-code ;
- module spécifique pour les séries temporelles ;
- comparaison automatique de plusieurs modèles ;
- visualisation des performances ;
- possibilité de finaliser et sauvegarder le modèle sélectionné.

Ces caractéristiques sont cohérentes avec les contraintes de VolatiChainXplorerAI, notamment l’exécution locale, la reproductibilité et l’absence de budget cloud obligatoire.

## Éléments externes disponibles

Westergaard et al. (2024) ont utilisé PyCaret dans une comparaison de frameworks AutoML appliqués à différents jeux de données temporels, dont Bitcoin.

Dans leur expérimentation, PyCaret obtient des résultats intéressants sur le dataset Bitcoin.

Ces résultats constituent une référence documentaire utile, mais concernent la prédiction du prix `Adj Close` et non la volatilité future à 7 et 30 jours.

Ils ne peuvent donc pas être considérés comme les performances attendues de VolatiChainXplorerAI.

## Points de vigilance

Le caractère automatisé de PyCaret ne dispense pas de préparer correctement les données ni de définir une méthodologie temporelle rigoureuse.

Le meilleur modèle identifié automatiquement dépend du dataset, des métriques utilisées et de la configuration de l’expérience.

## Conclusion provisoire

PyCaret apparaît comme une solution fortement compatible avec VolatiChainXplorerAI.

Sa prise en charge native du forecasting, son intégration Python et son fonctionnement local justifient son maintien parmi les candidats au benchmark final.