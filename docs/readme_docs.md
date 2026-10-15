# Documentation du projet - VolatiChainXplorerAI

Ce dossier centralise l'ensemble des livrables documentaires du projet : veille technologique, benchmark AutoML, preuves de sprint et référentiels de données.  
Tous les fichiers sont au format Markdown ou CSV afin de garantir la traçabilité, la lisibilité et la facilité de mise à jour.

---

## Arborescence du dossier `docs/`

```
docs/
├── readme_docs.md                          ← ce fichier
│
├── veille/                                 ← veille technologique
│   ├── fiches/
│   │   ├── fiche_veille_01_Yang_2026.md
│   │   ├── fiche_veille_02_Dallasta_2026.md
│   │   ├── fiche_veille_03_Lamiry_2026.md
│   │   └── fiche_veille_04_Westergaard_2024.md
│   ├── publications/
│   ├── preuve_veille/
│   ├── besoin_prediction.md
│   ├── matrice_synthese_01.md
│   ├── synthese_veille.md
│   └── tableau_veille.csv
│
├── benchmark/                              ← benchmark AutoML
│   ├── outils/
│   │   ├── autogluon.md
│   │   ├── pycaret.md
│   │   ├── azure_automl.md
│   │   ├── h2o_automl.md
│   │   └── vertex_ai.md
│   ├── results_benchmark/
│   │   ├── benchmark_results.csv
│   │   ├── autogluon_test_results.csv
│   │   ├── pycaret_test_results.csv
│   │   └── baseline_test_results.csv
│   ├── contraintes_techniques.md
│   ├── criteres_benchmark.md
│   ├── grille_comparaison_automl.md
│   ├── note_cadrage_et_guide_experimentation_benchmark_automl.md
│   └── preselection_frameworks.md
│
└── preuves_sprint_0/                       ← preuves et références du sprint 0
    ├── dictionnaire_variables.md
    └── tests_pytest_build_features_engineering_11_passed.png
```