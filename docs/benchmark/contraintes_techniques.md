# Contraintes techniques — VolatiChainXplorerAI

## Contraintes obligatoires

- La solution doit pouvoir fonctionner principalement en local.
- Elle ne doit pas dépendre obligatoirement d’un service cloud payant.
- Elle doit être compatible avec l’environnement Python du projet.
- L’utilisation de Docker est privilégiée pour isoler les dépendances et faciliter la reproductibilité.
- Le traitement doit respecter l’ordre temporel des données.
- Le pipeline doit éviter toute fuite d’information entre les données d’entraînement et les données futures.
- Le modèle retenu doit pouvoir être réutilisé dans l’application VolatiChainXplorerAI.

## Contraintes de ressources à contrôler

- La consommation mémoire doit rester compatible avec les ressources locales disponibles.
- L’espace disque utilisé par les dépendances, images Docker et modèles doit rester maîtrisé.
- Le temps d’entraînement doit rester compatible avec le calendrier du projet.
- Les solutions trop lourdes en calcul ou en stockage devront être évaluées avec attention.

## Critères de choix associés

- Performance prédictive
- Interprétabilité
- Robustesse
- Reproductibilité
- Facilité d’intégration
- Coût
- Compatibilité avec une exécution locale