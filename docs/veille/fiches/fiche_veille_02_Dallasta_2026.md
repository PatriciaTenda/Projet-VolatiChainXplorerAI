# Fiche de veille 02 — Dallasta et al., 2026

## Référence
**Titre :** Does Preprocessing Quality Matter for AutoML? A Case Study on Time Series Forecasting with Environmental Data  
**Auteurs :** Guilherme Castro Dallasta, Jan N. van Rijn, Andre Carlos Ponce de Leon Ferreira de Carvalho  
**Année :** 2026  
**Type de source :** Publication académique — AutoML 2026  
**Institutions :** University of São Paulo / Leiden University

## Thématique
AutoML, forecasting de séries temporelles, qualité des données, preprocessing, valeurs manquantes, imputation.

## Problème étudié
L’article étudie l’influence de la qualité du prétraitement des données sur les performances des systèmes AutoML appliqués aux séries temporelles.

Il cherche notamment à déterminer si les valeurs manquantes, les mesures aberrantes et les stratégies d’imputation peuvent affecter les performances de prévision obtenues ensuite par les pipelines AutoML.

## Message principal
La performance d’un système AutoML dépend en partie de la qualité du prétraitement des séries temporelles.

Les problèmes présents dans les données en amont peuvent se propager dans le pipeline et influencer la sélection des modèles, l’optimisation des hyperparamètres et les performances finales de forecasting.

Un prétraitement adapté peut donc améliorer les performances, tandis qu’un traitement insuffisant ou inadapté peut dégrader les résultats.

## Méthodologie
Les auteurs comparent deux frameworks de forecasting :

- AutoGluon-TimeSeries
- sktime

Ils utilisent les mêmes quatre modèles dans les deux environnements :

- DeepAR
- XGBoost
- SARIMA
- Prophet

Cette méthodologie permet de limiter l’influence de la disponibilité des modèles et de mieux étudier l’impact du pipeline de preprocessing.

Trois stratégies de prétraitement sont comparées, dont un pipeline hiérarchique utilisant plusieurs méthodes de traitement des valeurs manquantes.

## Principaux résultats
L’expérience montre que l’amélioration du preprocessing peut avoir un impact important sur les performances de forecasting.

Les résultats ne sont cependant pas identiques pour tous les modèles et tous les frameworks.

AutoGluon-TimeSeries bénéficie de l’amélioration du preprocessing dans plusieurs situations, tandis que les résultats obtenus avec sktime sont plus variables.

L’effet du prétraitement dépend donc du framework, du modèle et des caractéristiques des données.

## Apport pour VolatiChainXplorerAI
Cet article montre que les performances d’un modèle ne dépendent pas uniquement du modèle lui-même, mais également du framework utilisé et de la qualité du preprocessing des données.

Pour VolatiChainXplorerAI, cette publication renforce l’importance du travail réalisé lors du Sprint 0 sur la préparation, le contrôle et la validation des datasets avant le benchmark AutoML.

Elle montre également que, pour comparer plusieurs solutions AutoML, il est important de leur fournir des données préparées de manière cohérente afin que les différences de performances observées ne proviennent pas simplement de différences de qualité des données.

## Éléments utiles pour le benchmark
- Qualité du preprocessing
- Gestion des valeurs manquantes
- Reproductibilité du pipeline
- Sensibilité des modèles au preprocessing
- Méthode de validation temporelle
- Métriques de forecasting
- Comparabilité des conditions expérimentales

## Fiabilité de la source
Publication académique récente réalisée par des chercheurs de l’University of São Paulo et de Leiden University.

L’étude repose sur une expérimentation documentée utilisant :
- deux frameworks AutoML ;
- quatre modèles de forecasting ;
- plusieurs stratégies de preprocessing ;
- un découpage temporel des données ;
- plusieurs métriques d’évaluation.

Les auteurs fournissent également le code, les données et les notebooks nécessaires à la reproduction d’une grande partie des expériences.

La principale limite est que l’étude concerne des données environnementales et non des séries financières ou des cryptomonnaies.

## Décision
**Conserver**

## Utilisation prévue
- Partie veille du Livrable E2
- Justification de l’importance du preprocessing
- Justification du travail réalisé pendant le Sprint 0
- Construction des critères du benchmark AutoML
- Justification de conditions de comparaison homogènes entre les solutions