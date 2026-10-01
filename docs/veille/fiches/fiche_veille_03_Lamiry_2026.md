# Fiche de veille 03 — Lamiry, 2026

## Référence
**Titre :** A Mathematical Pre-Screening Framework for Training-Free Model Selection in Time-Series Cashflow Forecasting  
**Auteur :** Ali Nabizadeh Lamiry  
**Année :** 2026  
**Type de source :** Article de recherche / prépublication  
**DOI :** 10.21203/rs.3.rs-11051613/v1

## Thématique
Sélection de modèles, forecasting de séries temporelles, aide à la décision, interprétabilité, robustesse, scalabilité, contexte d’utilisation.

## Problème étudié
L’article cherche à déterminer comment présélectionner un modèle de machine learning adapté à un problème de prévision avant de lancer des entraînements coûteux.

L’auteur considère que le choix du modèle doit dépendre des caractéristiques des données et des besoins de l’utilisateur plutôt que de rechercher un algorithme universellement meilleur.

## Message principal
Le choix d’un modèle peut être considéré comme un problème de compatibilité entre le contexte du projet et les capacités des différents algorithmes.

L’article prend notamment en compte :
- le volume des données ;
- le niveau de bruit ;
- la granularité ;
- le ratio entre le nombre de variables et le nombre d’observations ;
- l’expertise de l’utilisateur.

Ces caractéristiques sont ensuite mises en relation avec quatre besoins opérationnels :
- interprétabilité ;
- robustesse ;
- scalabilité ;
- capacité de représentation.

## Méthode proposée
L’auteur propose un framework de présélection permettant de recommander un modèle avant entraînement.

Le principe est de :
1. caractériser le contexte du problème ;
2. transformer ce contexte en besoins opérationnels ;
3. décrire les capacités des modèles candidats ;
4. calculer un score de compatibilité entre les besoins et les capacités ;
5. recommander le modèle le plus compatible.

La méthode cherche ainsi à limiter les essais coûteux et le recours à des entraînements multiples.

## Principaux constats
Les résultats montrent qu’aucun modèle ne domine dans tous les contextes.

Les performances varient selon les caractéristiques des données et les besoins de l’utilisateur.

Sur certains jeux de données, des modèles simples obtiennent des performances proches de modèles plus complexes, tandis que dans d’autres contextes, des modèles plus sophistiqués deviennent plus adaptés.

Cela confirme l’intérêt d’une sélection de modèle fondée sur le contexte plutôt que sur une logique de modèle universellement supérieur.

## Apport pour VolatiChainXplorerAI
Cet article montre que le choix d’un modèle ou d’une solution AutoML ne doit pas reposer uniquement sur la performance prédictive.

Pour VolatiChainXplorerAI, il fournit plusieurs critères intéressants pour le futur benchmark :
- robustesse ;
- interprétabilité ;
- scalabilité ;
- capacité à représenter des relations complexes ;
- coût de sélection ou d’expérimentation ;
- adéquation entre la solution et le contexte du projet.

Il soutient également l’idée qu’une présélection documentaire peut être réalisée avant les tests expérimentaux afin d’éviter de tester inutilement toutes les solutions disponibles.

## Éléments utiles pour le benchmark
- Interprétabilité
- Robustesse
- Scalabilité
- Capacité de représentation
- Coût computationnel
- Adéquation au contexte
- Besoin d’entraînement préalable
- Transparence du processus de sélection
- Reproductibilité

## Fiabilité de la source
Article récent proposant une méthode explicite, accompagnée d’une validation sur plusieurs jeux de données financiers et d’une implémentation Python disponible publiquement.

La source est utile pour la réflexion méthodologique sur la sélection des modèles.

Cependant, plusieurs limites doivent être conservées :
- le domaine étudié est la prévision de trésorerie des PME et non la volatilité du Bitcoin ;
- le framework est présenté comme une preuve de concept ;
- les auteurs reconnaissent qu’une validation plus large sur d’autres domaines et jeux de données est encore nécessaire.

## Décision
**Conserver**

## Utilisation prévue
- Partie veille du Livrable E2
- Construction des critères du benchmark
- Justification d’une présélection documentaire avant expérimentation
- Réflexion sur le compromis entre performance, coût, interprétabilité et robustesse