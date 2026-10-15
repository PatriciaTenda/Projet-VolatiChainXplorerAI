
# Dossier `notebooks/`

Ce dossier contient l'ensemble des notebooks Jupyter du projet **VolatiChainXplorerAI**.  
Ils couvrent le cycle complet du projet : cadrage méthodologique, exploration des données, ingénierie des features, benchmark des frameworks AutoML, et validation du modèle retenu.

Les notebooks sont numérotés de `00` à `09` et doivent être exécutés dans l'ordre pour garantir la reproductibilité des résultats.  
Deux notebooks dédiés au scraping de données (`scrape_reddit.ipynb`, `scrape_twitter.ipynb`) complètent le dossier.

### Environnements requis

| Environnement | Usage |
|---------------|-------|
| `autogluon` | Notebooks `06`, `09` et tout ce qui implique AutoGluon |
| `.venv_pycaret` | Notebook `05` (PyCaret) |
| `.venv` | Notebooks généraux (`00` à `04`, `07`, `08`) |

---

## Notebooks associés (`notebooks/`)

| # | Notebook | Contenu |
|---|----------|---------|
| 00 | `00_cadre_theorique_et_methodologique.ipynb` | Cadre théorique et approche méthodologique |
| 01 | `01_etat_des_lieux_dataset.ipynb` | Exploration et état des lieux du dataset |
| 02 | `02_feature_engineering_bitcoin.ipynb` | Feature engineering Bitcoin |
| 03 | `03_analyse_statistique_modelisation.ipynb` | Analyse statistique et modélisation |
| 04 | `04_protocole_commun_benchmark.ipynb` | Protocole commun de benchmark |
| 05 | `05_poc_pycaret.ipynb` | Preuve de concept PyCaret |
| 06 | `06_poc_autogluon.ipynb` | Preuve de concept AutoGluon |
| 07 | `07_baseline_volatilite.ipynb` | Baseline volatilité |
| 08 | `08_analyse_comparative_automl.ipynb` | Analyse comparative AutoML |
| 09 | `09_validation_deploiement_autogluon.ipynb` | Validation et déploiement AutoGluon |

---

## Notes techniques

- La version d'AutoGluon doit être lue via `importlib.metadata.version("autogluon")` — le module racine n'expose pas `__version__` directement.
- Les environnements virtuels dédiés sont `.venv_autogluon` et `.venv_pycaret`.
