# Note de cadrage méthodologique et guide d’expérimentation - Benchmark AutoML

**Projet :** VolatiChainXplorerAI  
**Objet :** définir le cadre méthodologique commun du benchmark et fournir une procédure à suivre **avant, pendant et après** chaque expérimentation AutoML.  
**Document de référence :** `notebooks/04_protocole_commun_benchmark.ipynb`.

**Organisation :** la partie I définit le périmètre, les données et les conditions communes ; la partie II décrit les opérations à effectuer et les contrôles à réaliser.



# PARTIE I - Note de cadrage méthodologique

## 1. Objectifs et périmètre du benchmark

Comparer les solutions AutoML candidates pour la **régression de la volatilité future du Bitcoin** sur deux horizons distincts : **7 jours** et **30 jours**. Garantir la cohérence des données, le respect de l'ordre temporel, l'absence d'utilisation anticipée du test et une mesure harmonisée des performances et des ressources.

Chaque solution est évaluée **séparément pour chacun des deux horizons**. Les particularités des algorithmes ou des procédures de validation internes restent possibles, mais doivent être consignées afin de ne pas présenter les outils comme strictement identiques.


## 2. Données et partitions communes

### 2.1. N'utiliser que les six partitions figées

Les POC **relisent les CSV exportés par le protocole commun** : ils ne reconstruisent pas leur propre découpage.

Répertoire de référence : `data/exports/benchmark_splits/`.

| Horizon | Fichier | Nombre de lignes attendu |
|---|---|---:|
| 7 jours | `train_7d.csv` | 4 228 |
| 7 jours | `validation_7d.csv` | 724 |
| 7 jours | `test_7d.csv` | 590 |
| 30 jours | `train_30d.csv` | 4 182 |
| 30 jours | `validation_30d.csv` | 701 |
| 30 jours | `test_30d.csv` | 590 |

Chaque CSV comporte **17 colonnes** : `date`, **15 variables explicatives** et la cible propre à l'horizon.

### 2.2. Vérifier l'intégrité avant d'entraîner

Pour chaque horizon :

- [ ] Les fichiers existent, s'ouvrent et possèdent les dimensions attendues.
- [ ] Les dates sont correctement ordonnées et non dupliquées.
- [ ] Les partitions ne se chevauchent pas et respectent l'ordre **train → validation → test**.
- [ ] Les jeux de test 7 et 30 jours présentent les **mêmes dates**, dans le même ordre.
- [ ] Les 15 variables explicatives sont identiques d'un horizon à l'autre.
- [ ] Aucune variable explicative ou cible n'est manquante, non numérique ou infinie.
- [ ] Aucun retraitement indépendant ne modifie les lignes ou valeurs des partitions figées.

Les bornes utilisées pour construire les partitions sont : **début de validation le 01/01/2023**, **début du test le 01/01/2025**, **fin du test le 13/08/2026**, avec une **purge de l'horizon + 1 jour** à chaque frontière : **8 jours** pour 7 j et **31 jours** pour 30 j.

### 2.3. Séparer les entrées de la cible

- **Entrées `X` :** les 15 variables explicatives communes, **sans `date` ni cible**.
- **Cible `y` à 7 jours :** `target_volatility_7d`.
- **Cible `y` à 30 jours :** `target_volatility_30d`.
- **Date :** conservée pour les contrôles et l'alignement des résultats, pas pour l'apprentissage.

> **Règle de sécurité :** ne jamais fournir la cible future parmi les entrées utilisées pour produire les prédictions.


## 3. Conditions expérimentales communes

| Paramètre | Consigne commune |
|---|---|
| Graine aléatoire | `42` |
| Budget maximal visé par horizon | **600 secondes (10 minutes)** |
| Calcul | **CPU uniquement** |
| Matériel | **Même ordinateur** pour les solutions comparées |
| Exécution | **Séquentielle** : ne pas entraîner deux POC simultanément |
| Données | **Partitions figées identiques**, même ensemble de variables |
| Comparaison finale | **Même jeu de test et mêmes fonctions de métriques** |

Avant chaque essai :

- [ ] Sélectionner l'environnement Python propre à la solution et relever ses versions.
- [ ] Documenter les dépendances nécessaires et leur installation.
- [ ] Fermer, dans la mesure du possible, les applications consommant fortement CPU/RAM.
- [ ] Relever le nom de la solution, la version, l'horizon, les paramètres et le budget effectivement appliqués.
- [ ] Noter toute limitation de l'outil empêchant d'appliquer rigoureusement une règle commune.

**Important :** le temps limite demandé à un outil et le **temps réellement mesuré** ne sont pas forcément égaux. Toujours mesurer et conserver le temps réel.



# PARTIE II - Guide opératoire d’expérimentation des POC

## 1. Procédure d’entraînement, validation et test

### Phase A - Apprentissage des candidats

1. Charger **uniquement** les partitions `train` et `validation` correspondant à l'horizon.
2. Appliquer les paramètres communs : graine 42, CPU, budget visé de 600 s.
3. Entraîner les candidats sur **train**, sans exploiter **test**.
4. Si l'outil effectue une validation interne (validation croisée, holdout interne, ensemble), consigner sa stratégie et les éventuelles purges temporelles.
5. Mesurer le temps global d'entraînement et les ressources pendant l'exécution.

### Phase B - Validation et choix du candidat

1. Produire les prédictions sur **validation** (directement ou selon les mécanismes documentés de l'outil).
2. Calculer **MAE** et **RMSE** sur les valeurs réelles de validation.
3. Classer les candidats avec un critère annoncé **avant** de consulter le test (RMSE comme métrique principale si tel est le choix retenu, MAE en complément).
4. Consigner le modèle retenu et la raison du choix.
5. Ne pas utiliser `test` pour sélectionner un modèle ni pour ajuster des hyperparamètres.

### Phase C - Réentraînement final prévu par le protocole initial

Le notebook source **prévoit** qu'après sélection de la solution et du modèle, le candidat retenu soit **réentraîné sur `train + validation`**, puis évalué une seule fois sur `test`.

- [ ] Vérifier que l'outil permet cette étape et définir sa mise en œuvre **avant l'accès au test**.
- [ ] Si cette étape ne peut pas être réalisée, **documenter explicitement l'écart** et conserver la distinction entre « procédure prévue » et « procédure exécutée ».
- [ ] Ne jamais écrire « réentraîné sur train + validation » si le modèle a seulement été restauré ou réutilisé sans réentraînement.

### Phase D - Évaluation finale unique

1. **Après sélection du candidat**, accéder pour la première fois au jeu `test` de l'horizon.
2. Prédire sur les **590 observations communes**, sans utiliser la cible comme entrée.
3. Calculer les métriques à l'aide des **mêmes fonctions externes**, indépendamment des scores propres à chaque outil :

   ```python
   from sklearn.metrics import mean_absolute_error, mean_squared_error
   import numpy as np

   mae = mean_absolute_error(y_test, y_pred)
   rmse = np.sqrt(mean_squared_error(y_test, y_pred))
   ```

4. Mesurer le temps nécessaire à la prédiction du lot de test.
5. Sauvegarder les résultats **sans retour à l'optimisation sur le test**.

> **Règle de comparaison :** seules les métriques calculées avec les mêmes vérités terrain et la même fonction sont directement comparables. Les scores internes affichés par PyCaret ou AutoGluon ne remplacent pas ce calcul commun.


## 2. Procédure de mesure des temps et ressources

Utiliser `time.perf_counter()` pour mesurer le temps réel des opérations. Pendant l'entraînement, suivre périodiquement les indicateurs avec `psutil` :

- **Temps d'entraînement global** (`training_time_seconds`) ;
- **Pic CPU observé** (`peak_cpu_percent`) ;
- **Pic de RAM utilisée** (`peak_ram_mb`) ;
- **Temps d'inférence sur le lot de test** (`inference_time_seconds`) ;
- Si utile : **temps moyen par ligne**, en précisant qu'il s'agit d'une moyenne sur lot.

**Précaution :** si `psutil` relève le CPU et la RAM **de tout le système**, ces pics **ne correspondent pas à la consommation propre du modèle ni au coût d'un candidat individuel**. L'indiquer dans le compte rendu. Les mesures globales d'un POC ne doivent pas être attribuées séparément à chacun de ses modèles.


## 3. Enregistrement des résultats et preuves

Le notebook source prépare les champs suivants :

| Champ | Consigne de remplissage |
|---|---|
| `solution` | Nom de l'outil AutoML |
| `horizon_days` | 7 ou 30 |
| `model` | Nom exact du candidat évalué |
| `evaluation_set` | `validation` ou `test` |
| `mae`, `rmse` | Métriques recalculées de manière commune |
| `training_time_seconds` | Durée réelle de l'expérimentation concernée |
| `inference_time_seconds` | Durée réelle pour le lot prédit |
| `inference_time_per_row_ms` | Moyenne sur le lot, si calculée |
| `peak_cpu_percent`, `peak_ram_mb` | Pics mesurés, avec le **périmètre** précisé |
| `estimated_cost_eur` | Coût estimé **uniquement s'il existe une méthode de chiffrage** ; sinon « non estimé » |
| `notes` | Environnement, écart au protocole, incident, limite de comparabilité |

Conserver en outre, si disponibles : version Python, version de la bibliothèque, identifiant de l'exécution, paramètres de validation interne, chemin d'artefact et horodatage.


## 4. Vérifications de conformité et clôture

- [ ] Les deux horizons 7 j et 30 j ont été traités conformément aux règles annoncées, ou les écarts sont notés.
- [ ] Les prédictions ont été produites avec les **15 variables communes** et les modèles sélectionnés.
- [ ] Les métriques communes de validation et de test ont été enregistrées.
- [ ] Aucun réglage n'a été effectué en fonction des performances de test.
- [ ] Les mesures de temps et de ressources indiquent leur **périmètre réel**.
- [ ] Les artefacts et fichiers de résultats sont conservés et retrouvables.
- [ ] Les incidents techniques, contraintes de dépendances et décisions d'exclusion éventuelles sont documentés.
- [ ] Le notebook expérimental, les exports et la grille de résultats constituent une preuve reproductible.


## 5. Traçabilité des écarts au protocole

Pour tout changement imposé par un outil ou découvert en cours d'expérimentation, renseigner un tableau **distinct du présent guide** :

| Date / POC | Règle prévue | Comportement réellement appliqué | Motif | Incidence sur la comparaison | Décision / preuve |
|---|---|---|---|---|---|
| À renseigner | À renseigner | À renseigner | À renseigner | À renseigner | À renseigner |

Exemples de points à surveiller : stratégie interne de validation temporelle, budget réellement consommé, utilisation de l'ensemble de validation, présence ou absence de réentraînement `train + validation`, modèle explicitement demandé lors de l'inférence.


## 6. Références internes

- `notebooks/04_protocole_commun_benchmark.ipynb` : **source des règles et des partitions**.
- `data/exports/benchmark_splits/` : six CSV communs.
- Notebooks propres à chaque POC : **traces d'exécution**, distinctes du présent guide.
- Dossier de résultats du benchmark : métriques et preuves d'évaluation.

**Principe directeur :** *mêmes données, mêmes cibles, mêmes contraintes générales et même calcul final des métriques ; particularités de chaque outil documentées ; test protégé des décisions d'entraînement et de sélection.*
