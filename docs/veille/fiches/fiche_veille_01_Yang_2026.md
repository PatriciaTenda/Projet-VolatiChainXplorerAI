# Fiche de veille 01 — Yang, 2026

## Référence
**Titre :** A Survey of Automated Time Series Forecasting: From Deep Learning to Foundation Models with Financial Applications  
**Auteur :** Zhuoran Yang  
**Année :** 2026  
**Type de source :** Publication académique / actes de conférence AITIA 2026  
**DOI :** 10.70267/aitia.2026316325

## Thématique
AutoML, forecasting de séries temporelles, modèles de fondation, applications financières.

## Problème étudié
L’article étudie l’évolution des méthodes de prévision de séries temporelles, depuis les modèles statistiques traditionnels jusqu’aux approches AutoML, modèles de fondation et agents intelligents. Il compare ces différentes approches selon leur niveau d’automatisation, leur capacité de prévision à long terme, leur interprétabilité et leur adaptabilité.

## Principaux enseignements
L’AutoML permet d’automatiser plusieurs étapes du pipeline de forecasting : sélection des variables, choix du modèle, optimisation des hyperparamètres et évaluation des performances.

Son principal intérêt est de réduire l’intervention humaine et d’améliorer l’efficacité, la reproductibilité et l’accessibilité du processus de prévision.

L’article souligne cependant que l’AutoML reste dépendant des espaces de recherche et des objectifs d’optimisation définis à l’avance.

## Apports sur les séries financières
Les séries financières sont particulièrement difficiles à prédire en raison de leur non-linéarité, de leur volatilité, du bruit, des ruptures structurelles et de leur sensibilité à des événements externes comme les politiques économiques, les événements géopolitiques ou le sentiment des investisseurs.

## Apport pour VolatiChainXplorerAI
Cette publication permet de mieux contextualiser la problématique fonctionnelle de VolatiChainXplorerAI en montrant les difficultés propres aux séries temporelles financières et l’intérêt des approches automatisées de forecasting.

Elle fournit également une synthèse conceptuelle de l’AutoML, de ses apports et de ses limites, ce qui aide à justifier la démarche de benchmark des solutions retenues dans le projet.

## Éléments utiles pour le benchmark
- Niveau d’automatisation
- Performance à long terme
- Interprétabilité
- Adaptabilité
- Robustesse
- Coût computationnel

## Fiabilité de la source
Source académique récente, publiée dans les actes d’une conférence, avec DOI et références scientifiques nombreuses.

Cette publication constitue surtout une source de cadrage théorique. Elle ne permet pas, à elle seule, de conclure sur les performances comparées de PyCaret, H2O AutoML, Azure AutoML ou Vertex AI.

## Décision
**Conserver**

## Utilisation prévue
- Partie veille du Livrable E2
- Contextualisation du forecasting automatisé
- Justification du recours à l’AutoML
- Construction des critères du benchmark