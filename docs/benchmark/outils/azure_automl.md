# Étude de Azure Automated ML

## Positionnement

Azure Automated ML est le service AutoML de Microsoft Azure Machine Learning.

Il permet d’automatiser l’entraînement, la comparaison et la sélection de modèles pour différents problèmes de machine learning, notamment le forecasting de séries temporelles.

## Automatisation

Azure AutoML entraîne et évalue plusieurs modèles et différentes configurations d’hyperparamètres.

Pour le forecasting, le service compare plusieurs familles de modèles puis sélectionne les meilleurs résultats selon une métrique principale définie par l’utilisateur.

Il peut également construire des modèles d’ensemble à partir des meilleurs candidats.

## Séries temporelles

Azure AutoML possède une prise en charge spécifique du forecasting.

L’utilisateur peut définir :
- la colonne temporelle ;
- la cible ;
- l’horizon de prévision ;
- les lags ;
- les fenêtres glissantes ;
- les métriques d’évaluation.

Cette approche est directement compatible avec un problème de prévision temporelle.

## Validation temporelle

Azure AutoML propose une validation spécifique aux séries temporelles appelée Rolling Origin Cross Validation.

Le principe consiste à avancer progressivement dans le temps :

passé -> validation future,
puis davantage de passé -> nouvelle validation future.

Cette méthode respecte donc l’ordre chronologique des observations.

## Métriques

Azure fournit plusieurs métriques utilisables pour la régression et le forecasting, notamment :
- MAE ;
- RMSE ;
- MAPE ;
- métriques normalisées ;
- R².

Le choix de la métrique principale peut être configuré.

## Interprétabilité

Azure Machine Learning propose également des fonctions permettant d’expliquer certains modèles et d’étudier l’importance des variables.

## Intérêt pour VolatiChainXplorerAI

Fonctionnellement, Azure AutoML est très adapté à notre problème :

- forecasting natif ;
- gestion des horizons ;
- validation temporelle ;
- automatisation de la sélection des modèles ;
- métriques adaptées ;
- possibilité d’industrialisation.

## Contraintes

La principale limite pour VolatiChainXplorerAI est l’environnement cloud.

L’utilisation nécessite un environnement Azure Machine Learning et des ressources de calcul Azure.

Cela implique une dépendance à une infrastructure externe et potentiellement des coûts d’utilisation.

Notre projet privilégie actuellement une exécution locale et ne dispose pas d’un budget cloud dédié.

## Conclusion provisoire

Azure AutoML constitue une solution techniquement très complète et particulièrement adaptée au forecasting.

Il est pertinent comme référence dans le benchmark.

Cependant, sa dépendance au cloud et les coûts potentiels diminuent son adéquation avec les contraintes actuelles de VolatiChainXplorerAI.

Il pourrait donc obtenir une excellente note fonctionnelle mais une note plus faible sur les critères coût et exécution locale.