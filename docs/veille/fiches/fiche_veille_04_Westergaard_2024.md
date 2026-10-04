# Fiche de veille 04 — Westergaard et al., 2024

## Référence

**Titre :** Time Series Forecasting Utilizing Automated Machine Learning (AutoML): A Comparative Analysis Study on Diverse Datasets  
**Auteurs :** George Westergaard, Utku Erden, Omar Abdallah Mateo, Sullaiman Musah Lampo, Tahir Cetin Akinci, Oguzhan Topsakal  
**Année :** 2024  
**Revue :** Information, volume 15, numéro 1  
**Type :** Article scientifique peer-reviewed  
**DOI :** 10.3390/info15010039  
**Lien :** https://escholarship.org/uc/item/7zk102mt

---

## Thématique

Comparaison de frameworks AutoML appliqués à la prévision de séries temporelles, notamment sur des données Bitcoin.

---

## Problème étudié

L’étude cherche à déterminer dans quelle mesure différents outils AutoML sont capables de traiter efficacement des problèmes de prévision sur séries temporelles.

Les auteurs comparent trois frameworks :

- AutoGluon ;
- Auto-Sklearn ;
- PyCaret.

Ils cherchent notamment à mesurer leurs performances sur des jeux de données présentant des caractéristiques différentes. 

---

## Message principal

Il n’existe pas de framework AutoML universellement meilleur.

Les performances dépendent fortement :

- des caractéristiques du dataset ;
- des algorithmes utilisés ;
- de la stratégie d’optimisation des hyperparamètres ;
- du temps d’entraînement ;
- des ressources disponibles.

Le choix d’un outil AutoML doit donc être effectué en fonction du problème et des données à traiter.

---

## Méthodologie

Les auteurs utilisent trois jeux de données temporelles :

- Bitcoin ;
- données météorologiques ;
- données COVID-19.

Le dataset Bitcoin contient des données allant de 2014 à 2022. L’objectif de l’expérience est de prédire la valeur `Adj Close` du Bitcoin.

Les outils sont comparés principalement à partir de métriques de prévision telles que :

- RMSE ;
- MASE ;
- MAPE ;
- MAE selon les expériences.

Les expérimentations utilisent un découpage entraînement/test de 90 % / 10 %.

---

## Critères utilisés pour sélectionner les outils AutoML

Les auteurs retiennent plusieurs critères pour choisir les frameworks à étudier :

- capacité à traiter les séries temporelles ;
- popularité ;
- performance ;
- facilité d’utilisation ;
- caractère open source ;
- développement actif.

Ces critères peuvent également servir de base à la construction du benchmark de VolatiChainXplorerAI.

---

## Enseignements concernant PyCaret

PyCaret est présenté comme une bibliothèque Python open source et low-code permettant d’automatiser différentes étapes du workflow de machine learning.

L’outil permet notamment :

- le preprocessing ;
- la sélection de variables ;
- la sélection des modèles ;
- l’optimisation des hyperparamètres ;
- la comparaison de plusieurs modèles.

Dans l’expérience décrite par les auteurs, les principales fonctions utilisées sont :

- `setup()` pour initialiser le workflow ;
- `compare_models()` pour entraîner et comparer plusieurs modèles ;
- `plot_model()` pour visualiser les performances ;
- `evaluate_model()` pour analyser les modèles.

PyCaret classe ensuite les modèles selon leurs performances.

---

## Résultats concernant le Bitcoin

Dans cette étude, PyCaret teste plusieurs modèles sur le dataset Bitcoin.

Parmi les modèles les mieux classés figurent notamment :

- Decision Tree ;
- Light Gradient Boosting ;
- ARIMA ;
- Extreme Gradient Boosting ;
- Gradient Boosting.

Les auteurs indiquent que, dans leur expérimentation sur le Bitcoin, PyCaret obtient le RMSE le plus faible parmi les trois outils étudiés.

Ils précisent cependant que ces résultats dépendent du dataset, des algorithmes sélectionnés, de l’optimisation des hyperparamètres et du temps d’entraînement.

---

## Apport pour VolatiChainXplorerAI

Cette publication est particulièrement pertinente pour VolatiChainXplorerAI car elle :

- étudie directement des outils AutoML ;
- travaille sur des séries temporelles ;
- utilise un dataset Bitcoin ;
- inclut PyCaret dans le benchmark ;
- fournit des métriques quantitatives ;
- propose des critères permettant de comparer différents frameworks AutoML.

Elle confirme également que le choix d’un outil AutoML ne doit pas reposer uniquement sur ses performances brutes mais également sur son adéquation avec le dataset, les ressources disponibles et le contexte d’utilisation.

---

## Point de vigilance pour VolatiChainXplorerAI

L’objectif de cette étude n’est pas exactement le même que celui de VolatiChainXplorerAI.

Les auteurs cherchent à prédire le **prix ajusté de clôture du Bitcoin (`Adj Close`)**, alors que VolatiChainXplorerAI cherche à prédire la **volatilité future du Bitcoin à 7 jours et 30 jours**.

Les métriques publiées peuvent donc servir de **référence externe pour évaluer les capacités de PyCaret sur des données Bitcoin**, mais elles ne peuvent pas être considérées comme les performances attendues de VolatiChainXplorerAI.

---

## Éléments utiles pour le benchmark

Cette publication permet de retenir plusieurs critères pour notre propre comparaison :

- capacité à traiter les séries temporelles ;
- diversité des modèles disponibles ;
- automatisation de la sélection des modèles ;
- optimisation des hyperparamètres ;
- RMSE ;
- MAE ;
- MAPE ;
- MASE ;
- facilité d’utilisation ;
- temps d’entraînement ;
- ressources nécessaires ;
- caractère open source ;
- qualité de la documentation.

Elle permet également de disposer de résultats scientifiques publiés concernant PyCaret sur un dataset Bitcoin.

---

## Limites de l’étude

Les auteurs signalent plusieurs limites :

- les performances sont fortement dépendantes des datasets utilisés ;
- l’AutoML évolue rapidement ;
- les métriques seules ne suffisent pas toujours pour déterminer le meilleur outil ;
- les grands datasets peuvent nécessiter beaucoup de temps et de ressources ;
- les séries très volatiles comme le Bitcoin restent difficiles à prédire.

L’étude utilise également essentiellement les configurations par défaut des différents outils, sans chercher à rendre leurs paramétrages parfaitement identiques.

---

## Fiabilité de la source

**Fiabilité : élevée.**

Justifications :

- publication scientifique ;
- article peer-reviewed ;
- méthodologie comparative ;
- plusieurs datasets utilisés ;
- plusieurs métriques d’évaluation ;
- DOI disponible ;
- limites de l’étude explicitement présentées par les auteurs.

---

## Décision

**À conserver.**

Cette source est directement utile à la construction du benchmark AutoML de VolatiChainXplorerAI.

---

## Utilisation prévue

Cette publication sera utilisée pour :

- justifier l’utilisation de frameworks AutoML pour les séries temporelles ;
- alimenter la cartographie des solutions AutoML existantes ;
- documenter PyCaret ;
- définir certains critères du benchmark ;
- fournir des métriques externes issues d’une expérimentation sur Bitcoin ;
- justifier qu’un outil AutoML doit être sélectionné en fonction du contexte et du dataset ;
- alimenter la partie « Réalisation du benchmark de services existants » du livrable E2.