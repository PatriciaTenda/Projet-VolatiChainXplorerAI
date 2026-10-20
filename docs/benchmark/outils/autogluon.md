# Étude d'AutoGluon - Time Series et Tabular

## Positionnement

AutoGluon est un framework AutoML open source permettant d'automatiser l'entraînement, l'optimisation, la sélection et la comparaison de modèles de Machine Learning.

Il propose notamment deux modules pertinents pour les problématiques de prédiction financière :

- **AutoGluon Time Series**, dédié au forecasting de séries temporelles ;
- **AutoGluon Tabular**, spécialisé dans les problèmes de classification et de régression supervisée sur données tabulaires.

Ces deux modules répondent à des approches prédictives différentes.

## Séries temporelles et données tabulaires

**AutoGluon Time Series**

Le module `TimeSeriesPredictor` permet de prévoir l'évolution d'une série temporelle sur plusieurs pas de temps futurs.

L'utilisateur définit notamment :
- la variable cible ;
- la fréquence temporelle ;
- l'horizon de prévision ;
- la métrique d'évaluation.

Le module prend en charge le forecasting multi-horizon et peut produire des prévisions probabilistes.

**AutoGluon Tabular**

Le module `TabularPredictor` permet d'entraîner des modèles supervisés à partir de variables explicatives et d'une variable cible.

L'utilisateur définit notamment :
- la variable cible ;
- le type de problème ;
- la métrique d'évaluation ;
- les contraintes de temps d'entraînement.

Il permet notamment d'aborder un problème de prédiction temporelle sous forme de régression supervisée, lorsque les variables explicatives et les cibles ont été préalablement construites.

## Modèles

**AutoGluon Time Series** peut notamment combiner :
- des modèles statistiques, tels que ETS (Error, Trend, Seasonality - Erreur, Tendance, Saisonnalité);
- des modèles fondés sur le Machine Learning ;
- des modèles de Deep Learning ;
- des modèles préentraînés de forecasting, tels que Chronos ;
- des ensembles de modèles.

**AutoGluon Tabular** peut notamment combiner :
- LightGBM ;
- CatBoost ;
- XGBoost ;
- des réseaux de neurones ;
- des ensembles de plusieurs modèles.

La disponibilité des modèles dépend des dépendances installées et des configurations retenues.

## Évaluation

AutoGluon dispose d'un tableau comparatif des modèles (*leaderboard*) permettant de consulter et de comparer les performances des modèles entraînés.

Selon le module utilisé et les données fournies, ce tableau peut notamment présenter :

- les scores obtenus sur les données de validation ;
- les scores obtenus sur un jeu de test, lorsqu'il est fourni ;
- les temps d'entraînement des modèles ;
- les temps nécessaires à la génération des prédictions.

Les métriques d'évaluation sont configurables selon la nature du problème étudié.

Le *leaderboard* facilite ainsi l'analyse comparative des modèles et l'identification des candidats les plus prometteurs.

## Prévisions

AutoGluon Time Series est conçu pour produire des prévisions successives sur un horizon temporel déterminé. Il peut également fournir plusieurs quantiles pour représenter l'incertitude des prévisions.

AutoGluon Tabular permet notamment de prédire directement une valeur numérique continue dans le cadre d'une régression.

La principale distinction réside donc dans la nature de la sortie attendue : une séquence de prévisions temporelles ou une valeur cible définie à partir de variables explicatives.

## Intérêt pour VolatiChainXplorerAI

AutoGluon présente un intérêt pour le projet en raison de :
- ses fonctionnalités AutoML ;
- la diversité de ses algorithmes ;
- ses capacités de régression et de forecasting ;
- l'automatisation de plusieurs étapes de modélisation ;
- son intégration dans un environnement Python.

L'article de **Westergaard et al. (2024)**, identifié lors de la veille scientifique et conservé dans le tableau de veille, a contribué à la découverte d'AutoGluon et à sa présélection parmi les solutions à étudier.

L'analyse des besoins de VolatiChainXplorerAI conduit ensuite à distinguer deux approches possibles.

| Critère | Time Series | Tabular |
|---|---|---|
| Approche | Forecasting temporel | Régression supervisée |
| Données attendues | Historique chronologique | Variables explicatives et cible |
| Sortie principale | Prévisions successives | Valeur cible prédite |
| Gestion multi-horizon | Native | Par définition de cibles distinctes |
| Adéquation au besoin actuel | Adaptation méthodologique nécessaire | Directe |


Elle a enfin conduit à privilégier l'étude du module AutoGluon Tabular, en raison de son adéquation avec la formulation du problème en régression supervisée sur données tabulaires.

## Justification du choix d'AutoGluon Tabular

Le besoin de VolatiChainXplorerAI consiste à estimer une **valeur synthétique de volatilité future sur 7 ou 30 jours**, à partir de variables financières et macroéconomiques.

Il ne s'agit pas, à ce stade, de prévoir individuellement la volatilité de chacune des journées futures.

Le problème est donc formulé comme une **régression supervisée sur données tabulaires**, avec une cible distincte pour chaque horizon.

Dans ce contexte, AutoGluon Tabular apparaît plus directement adapté à la structure des données et à l'objectif prédictif retenu.

AutoGluon Time Series demeure une solution intéressante, notamment dans la perspective d'une évolution du projet vers la prévision quotidienne multi-horizon et la production de prévisions probabilistes.

Ce choix repose sur l'adéquation fonctionnelle au besoin actuel et ne préjuge pas des performances prédictives respectives des deux modules.

## Points de vigilance

AutoGluon Tabular ne garantit pas automatiquement le respect de l'ordre chronologique des observations lors de ses validations internes.

Une attention particulière devra donc être portée à la préparation des données, à la stratégie de validation et à la prévention des fuites temporelles.

Par ailleurs, certains modèles peuvent nécessiter des ressources importantes en mémoire, en stockage et en temps de calcul.

Il conviendra de vérifier leur compatibilité avec les contraintes de l'environnement local.

## Conclusion provisoire

AutoGluon constitue une solution pertinente à considérer dans le benchmark AutoML de VolatiChainXplorerAI.

À l'issue de cette étude préalable, **le module Tabular est privilégié** en raison de son adéquation avec la formulation du problème en régression supervisée et les cibles de volatilité à 7 et 30 jours.

Sa pertinence prédictive et opérationnelle devra être confirmée par les expérimentations et la comparaison avec les autres solutions présélectionnées.