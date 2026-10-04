# Critères du benchmark AutoML

## Objectif

Le benchmark vise à identifier la solution AutoML la plus adaptée à VolatiChainXplorerAI pour prédire la volatilité future du Bitcoin à 7 jours et 30 jours.

La comparaison doit prendre en compte non seulement les performances prédictives, mais également les contraintes techniques, économiques et opérationnelles du projet.

## Critères retenus

### 1. Adéquation avec le problème de prédiction

La solution doit pouvoir traiter une cible numérique correspondant à la volatilité future à 7 jours et 30 jours.

Deux approches sont acceptables :
- forecasting temporel natif ;
- régression supervisée à partir des datasets avec le feature engineering déjà effectué.

**Question :**
La solution permet-elle réellement de traiter notre problème de prédiction ?

---

### 2. Respect de la dimension temporelle

La solution doit permettre une validation respectant l’ordre chronologique des observations afin d’éviter toute fuite d’information entre passé et futur.

**Question :**
Peut-on entraîner sur le passé et évaluer sur des périodes futures sans mélange aléatoire des données ?

**Importance : très forte.**

---

### 3. Niveau d’automatisation

Le benchmark évaluera les étapes prises en charge automatiquement par la solution :

- entraînement de plusieurs modèles ;
- comparaison des modèles ;
- optimisation des hyperparamètres ;
- classement des résultats ;
- éventuel preprocessing ou feature engineering.

**Question :**
Quelles étapes la solution automatise-t-elle réellement ?

---

### 4. Modèles disponibles

La solution doit proposer une diversité suffisante de modèles adaptés au problème.

Exemples :
- modèles statistiques ;
- Random Forest ;
- Gradient Boosting ;
- XGBoost / LightGBM ;
- modèles d’ensemble ;
- éventuellement Deep Learning ou modèles de forecasting spécialisés.

**Question :**
La solution donne-t-elle accès à des modèles suffisamment diversifiés pour comparer plusieurs stratégies ?

---

### 5. Métriques et évaluation des performances

La solution doit fournir des métriques adaptées à une cible numérique.

Les métriques particulièrement intéressantes pour le projet sont notamment :
- MAE ;
- RMSE ;
- MAPE ou métriques similaires lorsque leur utilisation est pertinente ;
- éventuellement MASE pour le forecasting.

**Question :**
La solution permet-elle de mesurer et comparer correctement les erreurs de prédiction ?

---

### 6. Performances documentées

Les performances disponibles dans des publications scientifiques ou des benchmarks externes pourront être utilisées comme éléments de comparaison.

Une attention particulière sera portée aux études utilisant :
- des séries temporelles ;
- des données financières ;
- des données Bitcoin ;
- des conditions expérimentales comparables.

**Point de vigilance :**
Les scores provenant de datasets ou de cibles différentes ne seront pas considérés comme directement comparables aux performances de VolatiChainXplorerAI.

Ils servent de preuves externes sur les capacités des outils et non de résultats propres au projet.

---

### 7. Interprétabilité

La solution doit permettre de comprendre suffisamment le comportement du modèle retenu.

Les éléments recherchés peuvent notamment être :
- importance des variables ;
- visualisations ;
- explications globales ou locales ;
- compréhension des facteurs influençant la prédiction.

**Question :**
Peut-on expliquer pourquoi le modèle produit une prédiction donnée ?

---

### 8. Compatibilité avec les ressources du projet

La solution sera évaluée selon :
- mémoire nécessaire ;
- temps d’entraînement ;
- espace disque ;
- besoins de calcul particuliers.

**Question :**
La solution peut-elle fonctionner avec les ressources disponibles pour VolatiChainXplorerAI ?

---

### 9. Exécution locale ou dépendance au cloud

Une exécution locale est privilégiée pour le projet.

Une solution cloud reste étudiée mais sa dépendance à une infrastructure externe constitue une contrainte supplémentaire.

**Question :**
La solution fonctionne-t-elle localement ou nécessite-t-elle une plateforme cloud ?

---

### 10. Coût

Le projet ne dispose pas d’un budget cloud dédié.

Les solutions open source et utilisables gratuitement en local seront donc favorisées.

**Question :**
L’utilisation de la solution entraîne-t-elle des coûts obligatoires ?

---

### 11. Intégration technique

La solution doit pouvoir s’intégrer à l’environnement existant de VolatiChainXplorerAI.

Les éléments étudiés seront notamment :
- compatibilité Python ;
- possibilité d’intégration avec l’application ;
- sauvegarde et rechargement du modèle ;
- compatibilité avec Docker lorsque cela est possible.

**Question :**
Le modèle final pourra-t-il être facilement intégré dans notre pipeline et notre application ?

---

### 12. Reproductibilité

Les expérimentations doivent pouvoir être reproduites.

La solution sera évaluée selon sa capacité à :
- conserver les paramètres ;
- sauvegarder les modèles ;
- reproduire un entraînement ;
- documenter les résultats obtenus.

**Question :**
Une autre personne pourrait-elle reproduire notre expérience dans les mêmes conditions ?

---

### 13. Documentation et maturité

La qualité de la documentation, la disponibilité d’exemples et la maturité de la solution seront également prises en compte.

**Question :**
La solution est-elle suffisamment documentée et maintenue pour être utilisée de manière fiable dans le projet ?