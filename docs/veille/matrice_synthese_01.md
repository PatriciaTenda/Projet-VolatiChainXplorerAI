# Matrice de synthèse 01 - AutoML et sélection de modèles pour le forecasting

## Objectif

Cette matrice met en perspective trois publications scientifiques sélectionnées dans le cadre de la veille technologique de VolatiChainXplorerAI.

L’objectif est d’identifier les principaux enseignements utiles au choix et au futur benchmark des solutions AutoML adaptées au projet.

## Sources comparées

### Source 1
**Yang, Zhuoran (2026)**  
*A Survey of Automated Time Series Forecasting: From Deep Learning to Foundation Models with Financial Applications*

### Source 2
**Dallasta, Guilherme Castro et al. (2026)**  
*Does Preprocessing Quality Matter for AutoML? A Case Study on Time Series Forecasting with Environmental Data*

### Source 3
**Lamiry, Ali Nabizadeh (2026)**  
*A Mathematical Pre-Screening Framework for Training-Free Model Selection in Time-Series Cashflow Forecasting*

## Matrice comparative

| Axe d’analyse | Yang, 2026 | Dallasta et al., 2026 | Lamiry, 2026 | Apport pour VolatiChainXplorerAI |
|---|---|---|---|---|
| **Rôle de l’AutoML** | L’AutoML permet notamment d’automatiser la sélection des variables, la sélection des modèles, l’optimisation des hyperparamètres et l’évaluation. | L’étude montre que les performances obtenues par les systèmes AutoML peuvent dépendre du pipeline de préparation des données utilisé en amont. | L’auteur propose une présélection des modèles en fonction du contexte avant de lancer des entraînements coûteux. | L’AutoML peut automatiser une partie importante de la modélisation, mais le problème doit être correctement cadré avant son utilisation. |
| **Qualité des données** | La qualité des données, le bruit, les valeurs manquantes et la non-stationnarité constituent des difficultés importantes pour les séries temporelles. | Le preprocessing influence les performances obtenues ensuite par les pipelines de forecasting. | Le niveau de bruit et les caractéristiques du dataset font partie des paramètres pris en compte pour orienter le choix du modèle. | Le travail de préparation et de validation des datasets réalisé avant le benchmark est indispensable. |
| **Choix du modèle** | Plusieurs familles de modèles présentent des niveaux différents d’automatisation, d’interprétabilité et d’adaptabilité. | Les résultats peuvent varier selon le framework, le modèle et le preprocessing utilisé. | Aucun modèle n’est considéré comme universellement supérieur ; sa pertinence dépend du contexte d’utilisation. | Le choix d’un modèle ne doit pas reposer uniquement sur sa performance brute. |
| **Critères de comparaison** | Automatisation, performance à long terme, interprétabilité et adaptabilité. | Qualité du preprocessing, reproductibilité, sensibilité aux données et validation temporelle. | Interprétabilité, robustesse, scalabilité et capacité de représentation. | Ces dimensions permettent de construire les premiers critères du benchmark des solutions AutoML. |
| **Coût et ressources** | L’automatisation améliore l’efficacité du processus, mais reste dépendante de l’espace de recherche et des objectifs définis. | Les choix de preprocessing et de framework peuvent modifier le coût et la complexité du pipeline. | L’auteur cherche à limiter les entraînements multiples en réalisant une présélection avant expérimentation. | Le coût computationnel et l’adéquation avec les ressources disponibles doivent être pris en compte lors du benchmark. |
| **Interprétabilité** | L’interprétabilité fait partie des dimensions utilisées pour comparer les différents paradigmes de forecasting. | L’article se concentre principalement sur l’impact de la qualité des données sur les performances AutoML. | L’interprétabilité est considérée comme une exigence opérationnelle importante dans le choix d’un modèle. | La solution retenue devra être suffisamment explicable pour comprendre les facteurs influençant les prédictions. |
| **Limites des travaux** | Il s’agit principalement d’une source de cadrage et de comparaison des approches de forecasting. | L’étude porte sur des données environnementales et non sur des données financières. | Le framework étudié concerne la prévision de trésorerie des PME et reste présenté comme une preuve de concept nécessitant davantage de validation. | Aucun de ces articles ne permet, à lui seul, de déterminer quelle solution AutoML sera la meilleure pour VolatiChainXplorerAI. |
| **Utilité principale pour le projet** | Comprendre le rôle de l’AutoML et situer les différentes approches de forecasting. | Justifier l’importance de la qualité des données et du preprocessing avant la modélisation. | Justifier une sélection tenant compte du contexte, des contraintes et de plusieurs critères. | Les trois sources fournissent ensemble une base méthodologique pour construire le benchmark AutoML. |

## Conclusion de la synthèse comparative

L’analyse croisée de ces trois publications montre que le choix d’une solution AutoML ne doit pas reposer uniquement sur les performances prédictives obtenues par les modèles.

La qualité des données et du preprocessing, les caractéristiques du problème de prédiction, les ressources disponibles ainsi que des critères tels que la robustesse, l’interprétabilité, la scalabilité et la reproductibilité doivent également être pris en compte.

Dans le cadre de VolatiChainXplorerAI, cette veille permet ainsi de définir les premiers critères du benchmark et confirme l’intérêt d’utiliser des datasets préparés et validés dans des conditions homogènes pour comparer les différentes solutions.

Les publications étudiées ne permettent toutefois pas encore de sélectionner une solution AutoML précise. La veille doit donc être complétée par l’étude des documentations officielles des solutions présélectionnées afin d’évaluer leurs fonctionnalités, leurs contraintes techniques, leur coût et leur compatibilité avec l’environnement du projet.