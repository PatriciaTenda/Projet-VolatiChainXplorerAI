# Étude de Vertex AI AutoML

## Positionnement

Vertex AI est la plateforme de machine learning managée de Google Cloud.

Elle propose des workflows AutoML destinés notamment aux données tabulaires ainsi qu’au forecasting.

## Automatisation

Vertex AI permet d’automatiser plusieurs étapes du pipeline de machine learning :

- découpage des données ;
- feature engineering ;
- recherche d’architecture ;
- entraînement ;
- création d’ensembles de modèles.

Le service permet également de contrôler certaines parties du pipeline lorsque l’utilisateur souhaite davantage de personnalisation.

## Séries temporelles

Vertex AI dispose d’un Tabular Workflow for Forecasting permettant de créer des modèles destinés à la prévision temporelle.

Le workflow demande notamment :
- une variable cible ;
- une colonne temporelle ;
- un horizon de prévision ;
- l’identification des séries ;
- les variables disponibles ou non au moment de la prédiction.

## Évaluation et interprétabilité

Vertex AI permet d’évaluer les modèles produits et propose des mécanismes d’explication des prédictions, notamment des valeurs d’importance des caractéristiques.

Ces informations peuvent aider à comprendre quelles variables influencent les résultats du modèle.

## Environnement

Vertex AI est une solution cloud managée.

Les données et les traitements sont intégrés à l’écosystème Google Cloud, avec notamment Cloud Storage, BigQuery et Vertex AI Pipelines.

## Intérêt pour VolatiChainXplorerAI

Vertex AI présente plusieurs avantages fonctionnels :

- forecasting ;
- AutoML ;
- automatisation du feature engineering ;
- scalabilité ;
- outils MLOps ;
- explicabilité ;
- déploiement intégré.

## Contraintes

La principale limite est similaire à celle d’Azure AutoML :

- dépendance au cloud ;
- configuration d’un projet Google Cloud ;
- utilisation de ressources cloud ;
- coûts potentiels ;
- architecture plus lourde que nécessaire pour notre projet actuel.

Par ailleurs, la documentation actuelle indique que le Tabular Workflow for Forecasting est encore proposé en Public Preview.

## Conclusion provisoire

Vertex AI constitue une solution AutoML complète permettant de comparer VolatiChainXplorerAI à une plateforme cloud industrielle.

Cependant, son caractère cloud et le statut actuel du workflow de forecasting réduisent son adéquation avec notre besoin d’une solution locale, simple et sans budget cloud obligatoire.

Il reste pertinent dans le benchmark, mais probablement moins favorable que certaines solutions open source locales.