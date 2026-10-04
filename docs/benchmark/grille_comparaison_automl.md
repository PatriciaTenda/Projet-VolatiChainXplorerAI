# Grille de comparaison des solutions AutoML

## Objectif

Cette grille compare les solutions AutoML présélectionnées pour VolatiChainXplorerAI.

L’objectif est d’identifier la solution la plus adaptée à la prédiction de la volatilité future du Bitcoin à 7 jours et 30 jours, en tenant compte à la fois des capacités fonctionnelles et des contraintes techniques du projet.

## Légende

- ✅ : favorable / bien adapté
- ⚠️ : possible mais avec contrainte ou adaptation
- ❌ : peu adapté au besoin
- 🔎 : à confirmer lors de l’expérimentation ou par une source complémentaire

| Critère | PyCaret | H2O AutoML | AutoGluon TimeSeries | Azure AutoML | Vertex AI |
|---|---|---|---|---|---|
| **Type de solution** | Framework AutoML Python low-code | Framework AutoML supervisé | Framework AutoML avec module Time Series | Service AutoML cloud managé | Plateforme AutoML cloud managée |
| **Forecasting temporel natif** | ✅ Oui, module `time_series` | ⚠️ Pas de module forecasting natif équivalent ; approche régression possible | ✅ Oui, `TimeSeriesPredictor` | ✅ Oui | ✅ Oui |
| **Prédiction multi-horizon** | ✅ Oui, horizon défini avec `fh` | ⚠️ À construire via les cibles 7 j / 30 j | ✅ Oui, `prediction_length` | ✅ Oui | ✅ Oui |
| **Respect de la chronologie** | ✅ Validation temporelle disponible | ⚠️ À gérer explicitement dans notre pipeline | ✅ Validation temporelle intégrée au forecasting | ✅ Rolling Origin Cross Validation | ✅ Gestion temporelle dans le workflow forecasting |
| **Comparaison automatique de plusieurs modèles** | ✅ `compare_models()` | ✅ Leaderboard AutoML | ✅ Plusieurs modèles + leaderboard | ✅ Oui | ✅ Oui |
| **Optimisation des hyperparamètres** | ✅ `tune_model()` | ✅ Automatisée pour plusieurs familles de modèles | ✅ Automatisée | ✅ Automatisée | ✅ Automatisée |
| **Diversité des modèles** | ✅ Modèles statistiques et ML | ✅ GLM, GBM, XGBoost, Random Forest, Deep Learning, ensembles… | ✅ ARIMA, ETS, LightGBM, DeepAR, TFT, Chronos, ensembles… | ✅ Plusieurs modèles de forecasting | ✅ Recherche et entraînement automatisés |
| **Métriques de régression / forecasting** | ✅ Plusieurs métriques disponibles | ✅ RMSE, MSE, MAE, etc. | ✅ Plusieurs métriques de forecasting | ✅ MAE, RMSE et autres métriques | ✅ MAE, RMSE et autres métriques |
| **Interprétabilité** | ✅ Visualisations et diagnostics ; dépend du modèle | ✅ Outils d’explication, importance des variables, SHAP selon modèles | ⚠️ Variable selon les modèles utilisés | ✅ Outils d’explication disponibles | ✅ Feature attribution / Explainable AI |
| **Exécution locale** | ✅ Oui | ✅ Oui | ✅ Oui | ❌ Service Azure | ❌ Service Google Cloud |
| **Compatibilité Python** | ✅ Oui | ✅ Oui | ✅ Oui | ✅ SDK Python | ✅ SDK Python |
| **Compatibilité avec notre approche Docker** | ✅ Possible | ✅ Possible / documentée | ✅ Conteneurisable | ⚠️ Architecture principalement cloud | ⚠️ Architecture principalement cloud |
| **Coût obligatoire du logiciel** | ✅ Open source | ✅ Open source | ✅ Open source | ⚠️ Utilisation des ressources Azure facturable | ⚠️ Utilisation des ressources Google Cloud facturable |
| **Dépendance à une infrastructure externe** | ✅ Faible | ✅ Faible | ✅ Faible | ❌ Forte dépendance Azure | ❌ Forte dépendance Google Cloud |
| **Sauvegarde / réutilisation du modèle** | ✅ Oui | ✅ Oui | ✅ Oui | ✅ Oui | ✅ Oui |
| **Adaptation à nos datasets déjà avec feature engineering** | ✅ Oui | ✅ Très adaptée à une approche régression | ✅ Oui, avec covariables temporelles | ✅ Oui | ✅ Oui |
| **Résultats scientifiques externes sur Bitcoin disponibles** | ✅ Oui | 🔎 À rechercher précisément | ✅ Oui | 🔎 À rechercher | 🔎 À rechercher |
| **Adéquation avec ressources locales limitées** | ✅ Plutôt favorable | ✅/⚠️ Configurable mais certains entraînements peuvent être lourds | ⚠️ Certains modèles DL/foundation peuvent être plus lourds | ❌ Calcul cloud | ❌ Calcul cloud |
| **Maturité / documentation** | ✅ Bonne | ✅ Bonne | ✅ Bonne | ✅ Très importante | ✅ Très importante |
| **Adéquation provisoire à VolatiChainXplorerAI** | **Très forte** | **Forte avec adaptation temporelle** | **Très forte** | **Forte techniquement, faible économiquement** | **Forte techniquement, faible économiquement** |

---

## Pondération des critères

Afin de limiter l’arbitraire dans la comparaison des solutions AutoML, les critères du benchmark sont classés selon trois niveaux d’importance.

### Barème retenu

- **Obligatoire : 3 points**
- **Très important : 2 points**
- **Secondaire : 1 point**

Cette classification est définie à partir des besoins fonctionnels et des contraintes techniques de VolatiChainXplorerAI.

### Classification des critères

| Critère | Niveau | Points | Justification |
|---|---|---:|---|
| Adéquation avec le problème de prédiction | Obligatoire | 3 | La solution doit permettre de prédire une cible numérique correspondant à la volatilité future à 7 et 30 jours. |
| Respect de la dimension temporelle | Obligatoire | 3 | L’entraînement et l’évaluation doivent respecter l’ordre chronologique afin d’éviter toute fuite d’information. |
| Performances / métriques | Obligatoire | 3 | La solution doit permettre de mesurer objectivement la qualité des prédictions avec des métriques adaptées. |
| Intégration Python / application | Obligatoire | 3 | Le modèle retenu devra pouvoir être intégré au pipeline et à l’application VolatiChainXplorerAI. |
| Reproductibilité | Obligatoire | 3 | Les expériences, paramètres et résultats doivent pouvoir être reproduits et documentés. |
| Exécution locale et coût | Très important | 2 | Le projet privilégie une exécution locale et ne dispose pas d’un budget cloud dédié. |
| Interprétabilité | Très important | 2 | Il est souhaitable de pouvoir comprendre les facteurs influençant les prédictions du modèle. |
| Ressources nécessaires | Très important | 2 | La solution doit rester compatible avec les ressources matérielles disponibles. |
| Automatisation | Secondaire | 1 | L’automatisation facilite les expérimentations, mais une automatisation maximale n’est pas indispensable au fonctionnement du projet. |
| Documentation / maturité | Secondaire | 1 | Une documentation claire et une solution mature facilitent l’utilisation, mais ne déterminent pas directement la validité de la prédiction. |

### Calcul des pondérations

Le total obtenu est de :

**23 points**

La pondération de chaque critère est calculée selon la formule suivante :

**Poids du critère = (nombre de points du critère / nombre total de points) × 100**

Ainsi :

- critère obligatoire : `3 / 23 × 100 = 13,04 %`
- critère très important : `2 / 23 × 100 = 8,70 %`
- critère secondaire : `1 / 23 × 100 = 4,35 %`

### Pondération finale

| Critère | Niveau | Poids |
|---|---|---:|
| Adéquation avec le problème de prédiction | Obligatoire | 13,04 % |
| Respect de la dimension temporelle | Obligatoire | 13,04 % |
| Performances / métriques | Obligatoire | 13,04 % |
| Intégration Python / application | Obligatoire | 13,04 % |
| Reproductibilité | Obligatoire | 13,04 % |
| Exécution locale et coût | Très important | 8,70 % |
| Interprétabilité | Très important | 8,70 % |
| Ressources nécessaires | Très important | 8,70 % |
| Automatisation | Secondaire | 4,35 % |
| Documentation / maturité | Secondaire | 4,35 % |
| **Total** |  | **100 %** |

## Règle d’interprétation

Les critères qualifiés d’« obligatoires » correspondent aux éléments les plus déterminants pour la validité et l’intégration de la solution dans VolatiChainXplorerAI.

Une solution présentant une incompatibilité majeure avec le problème de prédiction ou ne permettant pas de respecter correctement la dimension temporelle pourra être écartée, même si son score global reste élevé.

Cette méthode de pondération permet de rendre le benchmark plus transparent et de justifier les différences d’importance accordées aux différents critères.
---

## Échelle de notation

Chaque solution pourra être évaluée sur une échelle de 0 à 5 :

- **0** : critère non satisfait ;
- **1** : très faible ;
- **2** : faible ;
- **3** : satisfaisant ;
- **4** : bon ;
- **5** : très bon.

Le score final sera calculé en appliquant la pondération de chaque critère.

---

## Interprétation provisoire

La comparaison documentaire fait apparaître trois positionnements différents.

**PyCaret et AutoGluon** apparaissent comme les solutions les plus naturellement alignées avec le besoin de forecasting temporel et la contrainte d’exécution locale.

**H2O AutoML** constitue une alternative particulièrement intéressante pour exploiter les datasets 7 jours et 30 jours déjà transformés en problèmes de régression supervisée. La gestion de la validation temporelle devra cependant rester sous le contrôle du pipeline VolatiChainXplorerAI.

**Azure AutoML et Vertex AI** disposent de fonctionnalités avancées de forecasting et d’industrialisation, mais leur dépendance à une infrastructure cloud et leurs coûts potentiels sont moins compatibles avec les contraintes actuelles du projet.

Cette première analyse ne constitue pas encore la recommandation finale. Elle sert à identifier les solutions qui méritent d’être conservées pour la suite du benchmark.