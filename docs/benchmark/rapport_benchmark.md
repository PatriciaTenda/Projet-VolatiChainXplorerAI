# RAPPORT DE BENCHMARK - SOLUTIONS AUTOML

**Projet :** VolatiChainXplorerAI  
**Objet :** Benchmark des solutions AutoML pour la prédiction de la volatilité du Bitcoin à 7 et 30 jours  
**Date :** 12 octobre 2026  
**Version :** 1.0  
**Statut :** Benchmark expérimental clôturé

---

## Résumé exécutif

Ce benchmark vise à comparer les solutions AutoML PyCaret et AutoGluon Tabular pour la prédiction de la volatilité future du Bitcoin à 7 et 30 jours, en s'appuyant sur un protocole expérimental commun et une baseline fondée sur la persistance de la volatilité historique.

Les résultats montrent qu'AutoGluon Tabular, avec le modèle `WeightedEnsemble_L2`, obtient les meilleures RMSE aux deux horizons, avec une réduction relative de **17,66 % à 7 jours et 17,56 % à 30 jours** par rapport à la baseline.

Toutefois, les **coefficients de détermination négatifs** observés imposent de distinguer la sélection de la solution AutoML de la validation définitive de la fiabilité prédictive.

**Recommandation :** retenir **AutoGluon Tabular**, avec le modèle `WeightedEnsemble_L2`, comme solution technologique pour la poursuite du projet VolatiChainXplorerAI, au regard des performances obtenues lors du benchmark comparatif.

---

## 1. Protocole d'évaluation

### 1.1. Critères d'évaluation

Le benchmark repose sur des indicateurs communs permettant d'apprécier la qualité prédictive et les contraintes techniques des solutions expérimentées comme suit :

- La **RMSE constitue le principal critère de classement des performances prédictives**.

- Les autres indicateurs interviennent dans l'analyse multicritère afin d'apprécier le compromis entre performance, rapidité, complexité et faisabilité technique.

- Aucun score pondéré chiffré n'a été calculé dans le cadre des expérimentations.

#### Tableau des critères d'évaluation

| Critère | Description | Méthode de mesure |
|---|---|---|
| MAE | Erreur absolue moyenne entre valeurs prédites et observées | Calcul sur les jeux de test communs |
| RMSE | Racine de l'erreur quadratique moyenne, pénalisant davantage les erreurs importantes | Calcul sur les jeux de test communs |
| R² | Performance relative à une prédiction constante égale à la moyenne des valeurs observées | Coefficient de détermination |
| Temps d'entraînement | Durée globale des procédures expérimentales | Chronométrage de l'exécution |
| Temps d'inférence | Temps nécessaire à la production des prédictions | Mesure sur 590 observations |
| CPU | Pic d'utilisation du processeur | Surveillance globale du système |
| RAM | Pic de mémoire utilisée | Surveillance globale du système |
| Coûts | Coûts logiciels et contraintes économiques | Évaluation des conditions d'utilisation |
| Déploiement | Compatibilité et réutilisabilité des modèles | Vérifications techniques |


### 1.2. Jeux de données

Les expérimentations reposent sur deux datasets destinés à la prédiction de la volatilité future réalisée du Bitcoin.

Chaque dataset comprend 15 variables explicatives numériques regroupant les rendements logarithmiques, les volatilités historiques, les variations du marché et les indicateurs macroéconomiques.

Les variables cibles sont :

- `target_volatility_7d`
- `target_volatility_30d`

Les données ont été réparties chronologiquement en ensembles d'entraînement, de validation et de test.

| Horizon | Entraînement | Validation | Test |
|---|---:|---:|---:|
| 7 jours | 4 228 | 724 | 590 |
| 30 jours | 4 182 | 701 | 590 |

Le protocole applique une purge temporelle de `horizon + 1` observations afin de limiter les chevauchements entre les fenêtres temporelles utilisées pour calculer les cibles.

Les partitions de test couvrent la même période, du **1er janvier 2025 au 13 août 2026**, permettant une comparaison sur un échantillon commun.

### 1.3. Conditions expérimentales

| Paramètre | Configuration |
|---|---|
| Infrastructure | Ordinateur local sous Windows 11 |
| Mode de calcul | CPU |
| Graine aléatoire | 42 |
| Budget expérimental | 600 secondes par horizon |
| Nombre de variables explicatives | 15 |
| Horizons | 7 et 30 jours |
| Métriques | MAE, RMSE, R² |
| Environnements | Virtuels et indépendants pour chaque outil |
| Exécution | Séquentielle |

Les deux outils ont été évalués sur les mêmes partitions chronologiques, mais leurs mécanismes de validation interne diffèrent:

- **PyCaret** utilise une validation croisée temporelle fondée sur `TimeSeriesSplit`, avec purge entre les sous-ensembles.

- **AutoGluon Tabular** utilise le jeu de validation externe transmis par `tuning_data`, sans **bagging** ni **stacking** dans la configuration expérimentée.

Ces différences n'affectent pas l'identité des jeux de test, mais limitent l'équivalence stricte des procédures internes de sélection.

Les modèles ont été entraînés sur les données d'entraînement, sélectionnés à partir des procédures de validation propres à chaque outil, puis évalués sur les jeux de test communs afin de comparer leurs performances et de déterminer la solution AutoML à retenir.

---

## 2. Résultats par approche

### 2.1. Approche A - Baseline de persistance

**Configuration :**

La baseline repose sur une méthode de **persistance de la volatilité historique.**

**Méthode:** La volatilité calculée sur les 7 ou 30 derniers jours est directement utilisée comme estimation de la volatilité future sur la période correspondante.

Cette méthode ne nécessite aucun entraînement.

**Résultats sur le jeu de test :**

| Horizon | MAE | RMSE | R² |
|---|---:|---:|---:|
| 7 jours | 0,009354 | 0,013431 | -0,4827 |
| 30 jours | 0,006931 | 0,009353 | -0,5676 |

**Observations qualitatives :**

La baseline fournit une référence simple, transparente et directement liée à la problématique financière.

Ses coefficients R² négatifs témoignent toutefois de limites prédictives par rapport à la référence constante utilisée dans le calcul de cet indicateur.

Elle constitue néanmoins un point de comparaison pertinent pour déterminer si la complexité des modèles AutoML apporte une amélioration mesurable.

### 2.2. Approche B — PyCaret

**Configuration :**

PyCaret a été utilisé pour expérimenter plusieurs modèles de régression, avec une validation croisée chronologique et un budget expérimental de 600 secondes par horizon.

Trois candidats ont été évalués sur chaque jeu de test.

**Résultats à 7 jours :**

| Modèle | MAE | RMSE | R² |
|---|---:|---:|---:|
| HuberRegressor | 0,008293 | 0,012347 | -0,253132 |
| LassoLars | 0,018931 | 0,020405 | -2,422448 |
| DummyRegressor | 0,018931 | 0,020405 | -2,422448 |

**Résultats à 30 jours :**

| Modèle | MAE | RMSE | R² |
|---|---:|---:|---:|
| Lasso | ≈ 0,019914 | ≈ 0,021169 | ≈ -7,0296 |
| LassoLars | ≈ 0,019914 | ≈ 0,021169 | ≈ -7,0296 |
| DummyRegressor | ≈ 0,019914 | ≈ 0,021169 | ≈ -7,0296 |

Les valeurs à 30 jours sont présentées sous forme arrondie ; les valeurs exactes figurent dans `pycaret_test_results.csv`.

**Observations qualitatives :**

À 7 jours, `HuberRegressor` améliore la RMSE de la baseline de persistance.

À 30 jours, les modèles PyCaret évalués présentent des performances inférieures à cette même référence.

Les résultats identiques de Lasso, LassoLars et DummyRegressor suggèrent des comportements prédictifs très proches, sans permettre d'affirmer leur équivalence exacte sans examen des prédictions individuelles.

### 2.3. Approche C — AutoGluon Tabular

**Configuration :**

AutoGluon Tabular a été utilisé pour entraîner plusieurs modèles de régression sur les partitions communes.

Le jeu de validation externe a permis de sélectionner les candidats, puis les modèles retenus ont été évalués sur les ensembles de test.

**Résultats à 7 jours :**

| Modèle | MAE | RMSE | R² |
|---|---:|---:|---:|
| WeightedEnsemble_L2 | 0,008544 | 0,011058 | -0,005152 |
| NeuralNetTorch | 0,007820 | 0,011156 | -0,023035 |
| LightGBMXT | 0,013604 | 0,015526 | -0,981313 |

**Résultats à 30 jours :**

| Modèle | MAE | RMSE | R² |
|---|---:|---:|---:|
| WeightedEnsemble_L2 | 0,006251 | 0,007711 | -0,065475 |
| NeuralNetTorch | 0,005722 | 0,008374 | -0,256412 |
| CatBoost | 0,019382 | 0,020651 | -6,642020 |

**Observations qualitatives :**

Le modèle `WeightedEnsemble_L2` présente les RMSE les plus faibles aux deux horizons.

`NeuralNetTorch` obtient les meilleures MAE, ce qui révèle une différence entre les classements selon les métriques retenues.

AutoGluon présente ainsi les meilleures performances prédictives relatives parmi les solutions effectivement expérimentées.

### 2.4. Solutions étudiées mais non expérimentées

| Solution | Statut | Justification |
|---|---|---|
| H2O AutoML | Écarté | Contraintes techniques relatives à Java et aux dépendances Python |
| Azure Automated ML | Étudié, non expérimenté | Service cloud non retenu pour les POC réalisés localement car nécessitant un budget |
| Vertex AI | Étudié, non expérimenté | Test conditionné au budget cloud, non réalisé |

Ces solutions ne disposent pas de résultats comparables sur les jeux de test communs. Leur exclusion du périmètre expérimental ne permet donc pas d'effectuer une comparaison.

---

## 3. Analyse comparative

### 3.1. Tableau récapitulatif

| Critère | Horizon 7 jours | Horizon 30 jours |
|---|---|---|
| RMSE baseline | 0,013431 | 0,009353 |
| Meilleure RMSE PyCaret | 0,012347 | 0,021169 |
| Meilleure RMSE AutoGluon | **0,011058** | **0,007711** |
| Meilleur modèle selon RMSE | WeightedEnsemble_L2 | WeightedEnsemble_L2 |
| Gain AutoGluon / baseline | **17,66 %** | **17,56 %** |
| Meilleur R² AutoML | -0,005152 | -0,065475 |

- Les résultats montrent qu'**AutoGluon** surpasse la **baseline de persistance** sur les deux horizons selon la RMSE.

- **PyCaret** apporte une amélioration à 7 jours avec **HuberRegressor**, mais pas à 30 jours parmi les candidats évalués.

### 3.2. Visualisation comparative

Les histogrammes comparatifs réalisés dans le notebook `08_analyse_comparative_automl.ipynb` représentent les RMSE des modèles à 7 et 30 jours, avec une ligne verticale indiquant la valeur de référence de la baseline. 

Ils permettent de distinguer visuellement les modèles dont la RMSE est inférieure ou supérieure à la méthode de persistance.

**Figures à intégrer dans la version finale du rapport :**

- Graphique comparatif des RMSE à 7 jours.
- Graphique comparatif des RMSE à 30 jours.

Les graphiques devront être exportés depuis le notebook d'analyse afin de préserver la correspondance avec les résultats expérimentaux. Image correspondante dans `preuve_by_sprint/sprint_02/`

### 3.3. Analyse des temps d'entraînement et d'inférence

**Durées expérimentales :**

| Solution | 7 jours | 30 jours |
|---|---:|---:|
| PyCaret | 41,14 s | 36,94 s |
| AutoGluon | 89,37 s | 44,10 s |

PyCaret présente les durées expérimentales les plus courtes aux deux horizons.

Cette comparaison doit toutefois être nuancée puisque les outils n'utilisent pas les mêmes mécanismes internes d'entraînement et de sélection.

**Temps d'inférence de WeightedEnsemble_L2 :**

| Horizon | Durée sur 590 observations |
|---|---:|
| 7 jours | 0,1591 s |
| 30 jours | 0,0781 s |

Ces mesures correspondent à des prédictions par lot et ne doivent pas être assimilées à la latence d'une prédiction individuelle au sein d'une application.

### 3.4. Ressources matérielles et coûts

Les deux solutions ont atteint** un pic d'utilisation globale du CPU de 100 % **pendant les expérimentations.

Les pics de mémoire système observés se situent **approximativement entre 15 160 et 15 355 Mo**.

Ces mesures ne permettent pas de quantifier précisément la consommation propre à chaque modèle.

PyCaret et AutoGluon ont été utilisés **sans coût d'acquisition logicielle ni service cloud facturé**.

Les coûts **énergétiques, d'hébergement futur et de maintenance n'ont pas été chiffrés**.

### 3.5. Analyse des forces et faiblesses

| Solution | Forces | Limites |
|---|---|---|
| **Baseline de persistance** | Simplicité ; transparence ; reproductibilité ; absence d'entraînement | Performances prédictives inférieures à celles des meilleurs modèles AutoGluon |
| **PyCaret** | Durées expérimentales plus courtes ; validation croisée temporelle configurable | Pas d'amélioration par rapport à la baseline à 30 jours parmi les modèles testés |
| **AutoGluon Tabular** | Meilleures RMSE aux deux horizons ; amélioration mesurable par rapport à la baseline ; sauvegarde et restauration réussies des prédicteurs | R² négatifs ; durées expérimentales supérieures ; dépendances à maîtriser pour l'intégration applicative |
---

## 4. Recommandation

### 4.1. Solution recommandée

**AutoGluon Tabular - modèle `WeightedEnsemble_L2` pour les horizons de 7 et 30 jours.**

### 4.2. Justification du choix

La sélection d'AutoGluon repose sur plusieurs éléments convergents :

1. **Performance prédictive :** le modèle `WeightedEnsemble_L2` obtient la RMSE minimale aux deux horizons.
2. **Amélioration par rapport à la baseline :** la réduction de RMSE atteint 17,66 % à 7 jours et 17,56 % à 30 jours.
3. **Faisabilité technique :** les prédicteurs sauvegardés ont été restaurés avec succès dans un notebook indépendant.
4. **Réutilisabilité :** cinq prédictions numériques ont été obtenues pour chacun des horizons sans réentraînement.
5. **Compatibilité :** l'environnement Windows/CPU a été validé après résolution d'une difficulté ponctuelle liée à la longueur des chemins d'installation.

Ces éléments justifient le choix d'AutoGluon comme solution privilégiée pour la poursuite du projet.

### 4.3. Limites de la recommandation

L'ensemble des modèles évalués présente des **coefficients R² négatifs**.

Même si AutoGluon surpasse la baseline historique en RMSE, ses performances restent inférieures, selon le R², à celles d'une prédiction constante égale à la moyenne réelle du jeu de test.

Il convient également de rappeler que les méthodes internes de validation des deux outils diffèrent et que les résultats du benchmark correspondent aux modèles initialement entraînés, sans réentraînement final sur `train + validation`.

### 4.4. Axes d'amélioration

Les travaux ultérieurs devront porter sur :

1. L'analyse détaillée des erreurs prédictives, notamment lors des épisodes de forte volatilité.
2. L'établissement de critères métier d'acceptation des performances.
3. La préparation d'une procédure de réentraînement et de versionnement des modèles.
4. L'intégration des prédicteurs dans une chaîne applicative reproductible.
5. La validation des ressources, de la latence et de la robustesse dans l'environnement applicatif cible.

---

## 5. Annexes

### 5.1. Résultats expérimentaux

Les fichiers suivants constituent les principales preuves quantitatives :

- `docs/benchmark/results_benchmark/pycaret_test_results.csv`
- `docs/benchmark/results_benchmark/autogluon_test_results.csv`
- `docs/benchmark/results_benchmark/baseline_test_results.csv`
- `docs/benchmark/results_benchmark/benchmark_results.csv`

Le fichier consolidé `docs/benchmark/results_benchmark/benchmark_results.csv` permet de centraliser les résultats mesurés ainsi que le statut des solutions étudiées et non expérimentées.

### 5.2. Notebooks de référence

| Notebook | Fonction |
|---|---|
| `04_protocole_commun_benchmark.ipynb` | Préparation du protocole expérimental commun |
| Notebooks POC PyCaret et AutoGluon | Entraînement, validation et tests des modèles |
| `07_baseline_volatilite.ipynb` | Construction et évaluation de la baseline |
| `08_analyse_comparative_automl.ipynb` | Analyse comparative, gains et visualisations |
| `09_validation_deploiement_autogluon.ipynb` | Vérification du chargement et de la réutilisation des modèles |

### 5.3. Documentation méthodologique

La note de cadrage et le guide d'application du protocole commun complètent les résultats expérimentaux en définissant les règles de comparaison.

Les différences entre les stratégies de validation interne, ainsi que les limites relatives à l'utilisation du jeu de test et au réentraînement final, doivent être conservées dans la documentation du benchmark.

---

## Conclusion générale

Le benchmark AutoML de VolatiChainXplorerAI a permis de comparer expérimentalement PyCaret et AutoGluon Tabular sur des partitions chronologiques communes, puis de confronter leurs performances à une baseline fondée sur la persistance de la volatilité historique.

Les résultats démontrent un avantage prédictif relatif d'AutoGluon, particulièrement avec le modèle `WeightedEnsemble_L2`, sur les horizons de 7 et 30 jours.

La faisabilité technique de la restauration et de la réutilisation des modèles a également été vérifiée.

**AutoGluon Tabular est donc retenu comme solution technologique privilégiée pour la poursuite du projet.**

Toutefois, les R² négatifs et les limites méthodologiques identifiées nécessitent une particulère visant à approfondir la validation complémentaire de la robustesse prédictive.

Le présent rapport constitue une pièce justificative du livrable E2 et assure la transition vers le Sprint 3, consacré à l’intégration du modèle dans l’application et à la mise en place de son monitoring.
