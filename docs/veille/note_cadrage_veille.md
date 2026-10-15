# Note de cadrage de la veille technologique

## 1. Contexte

La veille technologique est réalisée dans le cadre du projet VolatiChainXplorerAI.

Le projet vise à prédire la volatilité future du Bitcoin à deux horizons : 7 jours et 30 jours, à partir de données historiques du Bitcoin et d’indicateurs macroéconomiques.

La veille doit permettre d’identifier des solutions d’intelligence artificielle préexistantes capables de répondre à ce besoin et de préparer leur comparaison dans le cadre d’un benchmark.

---

## 2. Objectif de la veille

L’objectif principal est d’identifier, comprendre et comparer les solutions AutoML susceptibles d’être utilisées pour la prédiction de séries temporelles.

La veille doit notamment permettre de :

- identifier les principales solutions disponibles ;
- comprendre leurs fonctionnalités ;
- vérifier leur capacité à traiter des séries temporelles ;
- identifier leurs contraintes techniques et économiques ;
- recueillir des résultats issus de publications existantes ;
- définir les critères du futur benchmark ;
- préparer la présélection des solutions les plus adaptées à VolatiChainXplorerAI.

---

## 3. Thématiques de veille

La veille est organisée autour des thématiques suivantes :

### AutoML et forecasting

Identifier les frameworks et services permettant d’automatiser l’entraînement, la comparaison et l’optimisation de plusieurs modèles.

### Séries temporelles

Étudier les méthodes et outils capables de respecter la dimension chronologique des données et de produire des prévisions à différents horizons.

### Bitcoin et données financières

Rechercher des études utilisant des données Bitcoin ou financières afin d’identifier les approches, métriques et difficultés rencontrées.

### Qualité et préparation des données

Étudier l’impact du preprocessing, du feature engineering et de la qualité des données sur les résultats des modèles AutoML.

### Sélection des modèles

Identifier les critères permettant de sélectionner une solution ou un modèle en fonction du contexte, des performances et des contraintes du projet.

---

## 4. Questions de veille

La veille doit permettre de répondre aux questions suivantes :

- Quelles solutions AutoML sont adaptées aux séries temporelles ?
- Quelles étapes du processus de modélisation automatisent-elles ?
- Quels modèles peuvent-elles entraîner et comparer ?
- Comment prennent-elles en compte la dimension temporelle ?
- Quelles métriques utilisent-elles pour évaluer les performances ?
- Peuvent-elles fonctionner localement ?
- Quels sont leurs besoins en ressources ?
- Quel est leur coût ?
- Permettent-elles d’expliquer les prédictions produites ?
- Peuvent-elles être intégrées facilement dans un environnement Python et Docker ?
- Existe-t-il des études ou benchmarks permettant d’évaluer leurs performances sur des séries temporelles financières ou Bitcoin ?

---

## 5. Sources d’information

Plusieurs catégories de sources sont utilisées.

### Documentations officielles

Elles servent à vérifier les fonctionnalités actuelles des solutions étudiées.

Solutions suivies notamment :

- PyCaret ;
- AutoGluon ;
- H2O AutoML ;
- Azure Automated ML ;
- Vertex AI.

### Publications scientifiques

Google Scholar et les plateformes académiques sont utilisés pour identifier des travaux portant sur :

- AutoML ;
- forecasting ;
- séries temporelles ;
- Bitcoin ;
- preprocessing ;
- sélection de modèles.

### Sources institutionnelles

Des sources telles que la Banque centrale européenne ou Eurostat peuvent être consultées pour suivre les évolutions liées aux indicateurs macroéconomiques utilisés dans le projet.

### Actualités techniques

Les releases, blogs officiels et dépôts techniques peuvent être utilisés pour suivre l’évolution des frameworks, modèles et bibliothèques.

---

## 6. Outils de collecte

### Feedly

Feedly est utilisé comme outil d’agrégation permettant de suivre plusieurs flux techniques et institutionnels dans une interface unique.

### Google Alerts

Google Alerts permet de surveiller automatiquement l’apparition de nouveaux contenus correspondant aux mots-clés définis.

### Google Scholar

Google Scholar est utilisé pour effectuer des recherches ciblées de publications scientifiques lorsque les flux automatisés ne fournissent pas suffisamment de contenus exploitables pour le benchmark.

---

## 7. Requêtes et mots-clés

Plusieurs requêtes sont utilisées pour cibler les informations recherchées, par exemple :

- `"AutoML" "time series forecasting"`
- `"PyCaret" "time series forecasting"`
- `"AutoML" "Bitcoin volatility"`
- `Bitcoin volatility`
- `AI forecasting crypto`
- `AutoGluon time series`
- `H2O AutoML`
- `Chronos`
- `TimesFM`
- `TimeGPT`

Les requêtes peuvent évoluer en fonction des résultats obtenus et des nouveaux besoins identifiés pendant le projet.

---

## 8. Fréquence de la veille

La veille est organisée selon un rythme hebdomadaire.

Les flux sont consultés régulièrement afin d’identifier les nouvelles publications ou évolutions techniques.

Une recherche ciblée supplémentaire est réalisée lorsqu’une information particulière est nécessaire pour le projet, notamment lors de la préparation du benchmark.

---

## 9. Processus de sélection des informations

Chaque information identifiée suit le processus suivant :

1. collecte de la source ;
2. vérification de son origine ;
3. évaluation de sa fiabilité ;
4. évaluation de sa pertinence pour VolatiChainXplorerAI ;
5. décision de conserver ou d’écarter la source ;
6. inscription dans le tableau de veille ;
7. rédaction éventuelle d’une fiche détaillée ;
8. intégration des enseignements dans une synthèse.

Les sources écartées sont également enregistrées afin de conserver une trace du processus de sélection.

---

## 10. Critères de qualification des sources

Les sources sont évaluées selon plusieurs critères :

- origine de la publication ;
- autorité de l’auteur ou de l’organisme ;
- caractère officiel ou scientifique ;
- présence éventuelle d’une évaluation par les pairs ;
- date de publication ;
- transparence de la méthodologie ;
- proximité avec le besoin du projet ;
- possibilité de vérifier les informations.

Une source fiable peut être écartée si son contenu n’est pas suffisamment pertinent pour le périmètre du projet.

---

## 11. Traitement des informations

Les publications les plus pertinentes font l’objet d’une fiche de veille contenant notamment :

- la référence ;
- la thématique ;
- la problématique étudiée ;
- la méthodologie ;
- les principaux résultats ;
- les limites ;
- l’apport pour VolatiChainXplorerAI ;
- la décision de conservation.

Les différentes fiches sont ensuite rapprochées dans une matrice de synthèse afin d’identifier les convergences, divergences et enseignements utiles au benchmark.

---

## 12. Partage et archivage

Les résultats de la veille sont centralisés dans le dépôt Git du projet.

L’organisation retenue comprend notamment :

`docs/veille/`
- fiches de veille ;
- publications ;
- preuves ;
- tableau de veille ;
- matrice de synthèse ;
- synthèse de veille ;
- note de cadrage.

Les documents sont principalement conservés au format Markdown afin de faciliter leur lecture, leur versionnement et leur mise à jour.

Git permet de conserver l’historique des modifications et d’assurer la traçabilité du travail réalisé.

---

## 13. Livrables attendus

La veille doit produire les éléments suivants :

- un tableau de suivi des sources ;
- des fiches de veille ;
- une matrice de synthèse ;
- une synthèse transversale ;
- des preuves de collecte ;
- une cartographie des solutions AutoML ;
- des critères permettant de préparer le benchmark.

---

## 14. Résultat attendu

À l’issue de la veille, plusieurs solutions d’intelligence artificielle préexistantes doivent avoir été identifiées et documentées.

Les informations recueillies doivent permettre de construire une présélection de solutions et de préparer un benchmark objectif prenant en compte :

- les performances ;
- la gestion des séries temporelles ;
- les ressources nécessaires ;
- le coût ;
- l’interprétabilité ;
- la reproductibilité ;
- l’intégration technique.

La veille constitue ainsi l’étape préparatoire permettant de passer d’un besoin de prédiction à une comparaison argumentée des solutions d’intelligence artificielle disponibles.