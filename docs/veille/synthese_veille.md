# Synthèse de veille

## Synthèse 01 - AutoML et sélection de modèles pour le forecasting

Les trois publications convergent sur un premier constat : l’automatisation ne supprime pas la nécessité de cadrer correctement le problème de prédiction. Yang présente l’AutoML comme un ensemble de méthodes permettant notamment d’automatiser la sélection des variables, le choix des modèles, l’optimisation des hyperparamètres et l’évaluation. Cette automatisation peut améliorer l’efficacité et la reproductibilité du processus de modélisation, mais elle reste dépendante des espaces de recherche et des objectifs définis.     

Les deux autres publications complètent cette vision. Dallasta et al. montrent que les performances obtenues par un système AutoML peuvent être fortement influencées par la qualité du preprocessing réalisé en amont. Leur étude souligne donc que la préparation et le contrôle des données doivent être considérés comme une véritable composante du pipeline de forecasting et non comme une simple étape de nettoyage.    

Lamiry adopte pour sa part une approche centrée sur le contexte : le choix d’un modèle doit dépendre des caractéristiques des données et des besoins opérationnels. Il prend notamment en compte l’interprétabilité, la robustesse, la scalabilité et la capacité de représentation, et rappelle qu’aucun modèle n’est universellement adapté à tous les contextes.   

Pour VolatiChainXplorerAI, ces travaux conduisent à ne pas limiter le futur benchmark AutoML à la seule performance prédictive. Le travail de préparation et de validation des datasets réalisé en amont doit être conservé comme prérequis du benchmark. La comparaison des solutions devra ensuite intégrer plusieurs dimensions : performance, robustesse, interprétabilité, scalabilité, reproductibilité, sensibilité au preprocessing et adéquation au contexte du projet. Ces trois publications permettent donc de construire les premiers critères du benchmark, mais elles ne permettent pas encore de déterminer quelle solution AutoML sera retenue. Cette décision devra être complétée par l’étude des caractéristiques et contraintes des solutions effectivement présélectionnées.

## Points clés à retenir
- L’AutoML automatise une partie importante de la modélisation.
- La qualité du preprocessing influence les résultats.
- Le choix d’un modèle dépend du contexte d’utilisation.
- La performance prédictive ne doit pas être le seul critère de comparaison.
- Les premiers critères du benchmark commencent à être identifiés.

## Conséquences pour VolatiChainXplorerAI
- Conserver les datasets préparés et validés comme base commune du benchmark.
- Comparer les solutions avec plusieurs critères, pas uniquement MAE/RMSE.
- Compléter la veille scientifique par les documentations officielles des solutions AutoML.

## Prochaine étape de veille
Étudier les sources officielles de :
- PyCaret
- H2O AutoML
- Azure Automated ML
- Vertex AI