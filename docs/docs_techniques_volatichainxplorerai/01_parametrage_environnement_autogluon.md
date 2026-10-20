# Documentation technique - Paramétrage de l’environnement AutoGluon

**Projet :** VolatiChainXplorerAI  
**Service d’IA :** AutoGluon Tabular  
**Objet :** Configuration de l’environnement d’exécution du service d’intelligence artificielle  
**Statut :** Environnement configuré et modèles réutilisables

## 1. Objectif

Dans le cadre de VolatiChainXplorerAI, AutoGluon Tabular a été retenu comme solution AutoML pour la prédiction de la volatilité future du Bitcoin à 7 jours et 30 jours.

Afin d’isoler les dépendances nécessaires au fonctionnement d’AutoGluon et de limiter les risques de conflit avec l’environnement principal du projet, nous avons créé un environnement Python dédié.

Cet environnement a été utilisé pour :

- installer et exécuter AutoGluon ;
- entraîner les modèles de prédiction ;
- sauvegarder les prédicteurs ;
- recharger les modèles sauvegardés ;
- vérifier leur capacité à produire des prédictions sans nouvel entraînement ;
- préparer leur future intégration dans l’architecture applicative.

---

## 2. Environnement d’exécution

L’environnement AutoGluon est installé séparément de l’environnement Python principal de VolatiChainXplorerAI.

**Chemin de l’environnement :**

```text
D:\venvs\autogluon
```

**Version de Python :**

```text
Python 3.12.9
```

**Version principale d’AutoGluon :**

```text
autogluon.tabular == 1.6.3
```

L’environnement principal du projet et l’environnement AutoGluon utilisent tous les deux **Python 3.12.9**, ce qui facilite leur compatibilité future.

---

## 3. Activation de l’environnement

Sous PowerShell, l’environnement AutoGluon peut être activé avec la commande suivante :

```powershell
D:\venvs\autogluon\Scripts\Activate.ps1
```

Lorsqu’un autre environnement virtuel est déjà actif, celui-ci doit d’abord être quitté :

```powershell
deactivate
```

L’environnement AutoGluon peut ensuite être activé.

---

## 4. Dépendances principales

Les principales bibliothèques installées et utilisées dans l’environnement sont notamment :

```text
Python                  3.12.9
autogluon.tabular       1.6.3
autogluon.core          1.6.3
autogluon.common        1.6.3
autogluon.features      1.6.3
numpy                   2.5.3
pandas                  2.3.3
pydantic                2.14.0
```

La cohérence des dépendances a été vérifiée avec :

```powershell
python -m pip check
```

**Résultat obtenu :**

```text
No broken requirements found.
```

Cette vérification confirme qu’aucune dépendance cassée n’a été détectée dans l’environnement au moment du contrôle.

---

## 5. Isolation par rapport à l’environnement principal

VolatiChainXplorerAI dispose également d’un environnement Python principal utilisé notamment par l’API FastAPI existante.

Au moment du paramétrage, l’environnement principal utilisait notamment :

```text
Python      3.12.9
FastAPI     0.115.13
NumPy       2.2.6
Pandas      2.2.3
Pydantic    2.11.7
```

AutoGluon n’était pas installé dans cet environnement principal.

Inversement, l’environnement dédié AutoGluon ne contenait pas encore FastAPI.

Nous avons donc conservé les deux environnements séparés afin de ne pas modifier prématurément l’environnement applicatif existant.

La compatibilité des dépendances devra être validée avant l’intégration définitive d’AutoGluon dans l’API FastAPI.

---

## 6. Sauvegarde des modèles

Deux prédicteurs AutoGluon ont été conservés, correspondant aux deux horizons de prédiction du projet.

```text
data/exports/autogluon_models/
├── predictor_7d/
└── predictor_30d/
```

Le premier prédicteur est associé à la cible :

```text
target_volatility_7d
```

Le second est associé à :

```text
target_volatility_30d
```

Le modèle retenu pour les deux horizons est :

```text
WeightedEnsemble_L2
```

Les modèles ont été sauvegardés afin de pouvoir être réutilisés ultérieurement sans relancer l’ensemble du processus d’entraînement.

---

## 7. Vérification du rechargement des prédicteurs

La réutilisabilité des modèles a été vérifiée avec la méthode suivante :

```python
from autogluon.tabular import TabularPredictor

predictor = TabularPredictor.load("chemin_du_modele")
```

Les deux prédicteurs ont été rechargés depuis leurs répertoires de sauvegarde sans lancer de nouvel entraînement.

Cette vérification permet de confirmer que les artefacts produits peuvent être restaurés et réutilisés dans un environnement d’exécution indépendant de la phase d’entraînement.

---

## 8. Validation technique de la réutilisabilité des modèles

La faisabilité technique de la réutilisation des modèles a été vérifiée dans le notebook :

```text
notebooks/09_validation_deploiement_autogluon.ipynb
```

Ce notebook a permis de contrôler :

1. la présence des prédicteurs sauvegardés à 7 jours et 30 jours ;
2. leur rechargement avec `TabularPredictor.load()` ;
3. l’identification des cibles associées à chaque prédicteur ;
4. l’utilisation explicite du modèle `WeightedEnsemble_L2` ;
5. la production de nouvelles prédictions sans relancer l’entraînement.

Des prédictions ont ainsi été obtenues pour plusieurs observations sur les deux horizons.

Ces tests ont confirmé que les modèles peuvent :

- être chargés depuis le disque ;
- recevoir des variables explicatives compatibles avec celles utilisées lors de l’entraînement ;
- produire une valeur numérique de volatilité prédite ;
- fonctionner sans réentraînement.

Cette étape constitue une **validation technique de la réutilisabilité des modèles** avant leur intégration dans l’API applicative.

Elle ne constitue pas encore un déploiement applicatif complet, puisque l’intégration dans FastAPI et l’exposition des prédictions via des endpoints restent à réaliser.

---

## 9. Contraintes et points de vigilance

Plusieurs points doivent être pris en compte pour la suite du projet.

### Compatibilité des environnements

L’environnement FastAPI existant et l’environnement AutoGluon utilisent des versions différentes de certaines dépendances.

Il n’est donc pas prévu d’installer directement AutoGluon dans l’environnement principal sans avoir auparavant vérifié la compatibilité de l’ensemble des bibliothèques.

### Ressources

AutoGluon peut entraîner plusieurs modèles et ensembles de modèles.

Son utilisation peut donc nécessiter une quantité importante de mémoire, de stockage et de puissance de calcul selon la configuration retenue.

### Chemins d’installation

Une difficulté liée à la longueur de certains chemins Windows a été rencontrée lors de la mise en place de l’environnement.

Cet incident fait partie des éléments techniques à conserver dans la documentation des incidents du projet.

### Dimension temporelle

AutoGluon Tabular est utilisé ici comme outil de régression supervisée.

Le respect de la chronologie des données n’est donc pas entièrement délégué au framework. Il reste assuré par le protocole de préparation et de partitionnement des données de VolatiChainXplorerAI.

---

## 10. Intégration prévue dans l’architecture

VolatiChainXplorerAI dispose déjà d’une API FastAPI mise en place lors du Bloc 1.

L’objectif n’est donc pas de créer une seconde API indépendante, mais d’étendre l’architecture existante afin d’y intégrer le service de prédiction.

L’architecture cible est la suivante :

```text
Streamlit
    │
    ▼
API FastAPI existante
    │
    ├── Accès aux données
    │      ├── PostgreSQL
    │      └── MongoDB
    │
    └── Service de prédiction
           ├── predictor_7d
           └── predictor_30d
```

L’API devra charger les prédicteurs sauvegardés puis exposer les prédictions de volatilité à 7 et 30 jours.

Cette intégration fera l’objet d’une documentation technique distincte.

---

## 11. Vérifications réalisées

À l’issue du paramétrage et des tests techniques, les contrôles suivants ont été réalisés :

- environnement Python dédié créé ;
- Python 3.12.9 utilisé ;
- AutoGluon Tabular 1.6.3 installé ;
- cohérence des dépendances vérifiée ;
- modèles 7 jours et 30 jours sauvegardés ;
- modèles rechargés sans réentraînement ;
- cible de chaque prédicteur vérifiée ;
- modèle `WeightedEnsemble_L2` utilisé explicitement ;
- prédictions de test obtenues sur les deux horizons ;
- réutilisabilité technique des artefacts confirmée.

L’environnement est donc fonctionnel pour le chargement et l’inférence des modèles AutoGluon.

L’intégration complète avec FastAPI ainsi que le monitorage applicatif seront réalisés dans les étapes suivantes du projet.

---

## 12. Documents et preuves associés

Les principaux éléments associés à cette documentation sont :

```text
notebooks/
└── 09_validation_deploiement_autogluon.ipynb

data/
└── exports/
    └── autogluon_models/
        ├── predictor_7d/
        └── predictor_30d/
```

Le notebook `09_validation_deploiement_autogluon.ipynb` constitue la preuve technique du rechargement et de la réutilisation des modèles sauvegardés sans nouvel entraînement.

La documentation technique du projet sera complétée progressivement dans le répertoire :

```text
docs/
└── docs_technique_volatichainxplorerai/
    ├── 01_parametrage_environnement_autogluon.md
    ├── 02_integration_fastapi_autogluon.md
    ├── 03_documentation_applicative.md
    ├── 04_monitoring_service_ia.md
    └── 05_incidents_techniques.md
```

Les notebooks expérimentaux et les résultats du benchmark constituent quant à eux les preuves ayant conduit au choix d’AutoGluon Tabular comme solution technologique pour VolatiChainXplorerAI.