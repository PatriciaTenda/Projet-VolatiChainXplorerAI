"""
Module pour la construction des features et des datasets d'entraînement 
pour les horizons de volatilité à 7 et 30 jours.
"""
# Charger les librairies nécessaires
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from pandas.api.indexers import FixedForwardWindowIndexer

# Definir le chemin du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))
print(project_root)
from setup.logger_config import setup_logger

# Definir le nom du module
module_name = Path(__file__).stem
logger = setup_logger(module_name)

# Definir le chemin du dataset source
dataset_path = (
    project_root
    / "data" 
    / "exports"
    / "datasets"
    / "unprocessed"
    / "btc_macro_dataset.csv"
)

# Definir le dossier d'export des datasets
export_path = (
    project_root
    / "data"
    / "exports"
    / "datasets"
    / "processed"
)

FEATURES_COLUMNS = [
     "log_return",
    "volatility_3d",
    "volatility_7d",
    "volatility_14d",
    "volatility_30d",
    "daily_range",
    "volume_change",
    "market_cap_change",
    "rate_mro",
    "inflation_rate",
    "unemployment_rate",
    "monetary_m3_rate",
    "log_return_lag_1d",
    "log_return_lag_7d",
    "log_return_lag_30d"
]

def load_data(data_path) -> pd.DataFrame:
    """Charger le dataset source et convertir la date en datetime"""
    try:
        logger.info(
            "Chargement du dataset depuis le chemin: %s", 
            data_path
        )
        
        df = pd.read_csv(
            data_path,
            parse_dates=["date"]
        )
        
        df["date"] = pd.to_datetime(
            df["date"],
            errors="raise"
            )
        logger.info(
            "Dataset chargé avec succès, forme: %s",
            df.shape
        )
        return df
    
    except FileNotFoundError as error:
        logger.error(
            "Fichier csv du dataset introuvable : %s",
            error
        )
        raise
    except (ValueError, pd.errors.ParserError) as error:
        logger.error(
            "Le fichier ou la colonne 'date' contient une valeur invalide: %s",
            error
        )
        raise
    except KeyError as error:
        logger.error(
            "La colonne 'date' est absente du dataset: %s",
            error
        )
        raise


def prepare_data(df : pd.DataFrame) -> pd.DataFrame:
    """Trier les dates et prépare le calendrier quotidien"""
    df_daily = df.copy()
    
     # Vérifier la présence de la colonne date
    if "date" not in df_daily.columns:
        raise KeyError(
            "La colonne 'date' est absente du dataset"
        )
    # Vérifier les dates manquantes dans la colonne "date"
    if df_daily["date"].isna().any():
        raise ValueError(
            "Le dataset contient des dates manquantes"
        )
        
    # Vérifier l'absence de dates dupliquées
    if df_daily["date"].duplicated().any():
        raise ValueError(
            "Le dataset contient des dates dupliquées"
        )
        
    # Trier les dates et transformer date en index
    df_daily = (
        df_daily.sort_values("date")
        .set_index("date")
    )
    # Créer un calendrier quotidien complet
    complete_calendar = (
        pd.date_range(
            start=df_daily.index.min(),
            end=df_daily.index.max(),
            freq="D",
            name="date"
        )
    )
    # Identifier les dates qui seront ajoutées
    current_dates = pd.DatetimeIndex(
        df_daily.index,
        name="date"
    )
    missing_dates : pd.DatetimeIndex = (
        complete_calendar.difference(current_dates)
    )

    logger.info(
        "Nombre de dates absentes ajoutées : %s",
        len(missing_dates)
    )

    # Réindexer le DataFrame sur ce calendrier
    df_daily = df_daily.reindex(
        complete_calendar
    )
        
    return df_daily


def create_features(df : pd.DataFrame) -> pd.DataFrame:
    """Calculerles variables explicatives"""
    
    df_daily = df.copy()

    # Calculer les rendements logarithmiques
    df_daily["log_return"] = np.log(
        df_daily["close"]/ df_daily["close"].shift(1)
    )   

    # Calculer les volatilités historique à 3, 7, 14, 30 jours
    for window in [3, 7, 14, 30]:
        df_daily[f"volatility_{window}d"] = (
            df_daily["log_return"]
            .rolling(
                window=window,
                min_periods=window
            )
            .std()
        )

    # Calculer l'amplitude journalière
    df_daily["daily_range"] = (
        df_daily["high"] - df_daily["low"]
    ) / df_daily["close"]
    
    # Calculer les variations du volume 
    df_daily["volume_change"] = (
        df_daily["volume"]
        .pct_change(fill_method=None)
    )
    
    # Calculer les variations de la capitalisation
    df_daily["market_cap_change"]  = (
        df_daily["market_cap"] 
        .pct_change(fill_method=None)
    )
    
    # Créer les variables retardées pour les rendements logarithmiques
    for lag in [1, 7, 30] :
        df_daily[f"log_return_lag_{lag}d"] = (
            df_daily["log_return"].shift(lag)
        )
    
    # Remplacer les valeurs infinies par NaN
    df_daily.replace(
        [np.inf, -np.inf], 
        np.nan, inplace=True
    )

    return df_daily


def create_targets(df : pd.DataFrame) -> pd.DataFrame:
    """Calculer les variables cibles de volatilité à 7 et 30 jours"""
    df_daily = df.copy()
    
    if "log_return" not in df_daily.columns:
        raise KeyError(
            "La colonne 'log_return' est absente du dataset."
        )
        
    # Calculer target_volatility à 7 et 30 jours
    for horizon in [7, 30]:
        forward_window = FixedForwardWindowIndexer(
             window_size=horizon
             )  
        df_daily[f"target_volatility_{horizon}d"] = (
            df_daily["log_return"]
            .shift(-1)
            .rolling(
                window=forward_window,
                min_periods=horizon
            )
            .std()
        )
    return df_daily


def build_training_dataset(df : pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Créer les datasets complets pour les 2 horizons de volatilité"""
    df_daily = df.copy()
    
    # créer les variables cibles pour les horizons de volatilité à 7 et 30 jours
    df_daily = create_targets(df_daily)
        
    # Vérifier la présence des colonnes nécessaires
    
    features_required = FEATURES_COLUMNS + [
        "target_volatility_7d", 
        "target_volatility_30d"
    ]
    
    missing_columns = [
        col for col in features_required
        if col not in df_daily.columns
    ]
    
    if missing_columns:
        raise KeyError(
        f"Les colonnes suivantes sont manquantes dans le dataset : {missing_columns}"
    )
    
    # Colonnes completes pour chaque dataset final
    dataset_7d_columns = FEATURES_COLUMNS + ["target_volatility_7d"]
    dataset_30d_columns = FEATURES_COLUMNS + ["target_volatility_30d"]

    # Construire les datasets finaux pour chaque horizon de volatilité
    # à 7 jours
    dataset_7d =(
        df_daily[dataset_7d_columns]
        .dropna()
        .reset_index()
        .copy()
    )
    
     # à 30 jours
    dataset_30d = (
        df_daily[dataset_30d_columns]
        .dropna()
        .reset_index()
        .copy()
    )

    return dataset_7d, dataset_30d

def temporal_split_with_purge(
    dataset : pd.DataFrame, 
    horizon : int
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Créer les ensembles train, validation et test avec ambargo"""
    
    dataset = dataset.copy()
    
    # Vérifier la présence de la colonne date
    if "date"  not in dataset.columns:
        raise KeyError(
            "La colonne 'date' est manquante dans le dataset"               
        )
    
    # Vérifier que horizon vaut 7 ou 30
    if horizon not in [7, 30]:
        raise ValueError(
            "L'horizon doit être soit 7 soit 30"
        )
    # Convertir date en datetime 
    dataset["date"] = pd.to_datetime(
        dataset["date"],
        errors="raise"
    )
    
    # Trier le dataset chronologiquement
    dataset = (
        dataset
        .sort_values("date")
        .reset_index(drop=True)
    ).copy()
    
    # Définir les frontières
    validation_start = pd.Timestamp("2023-01-01")
    test_start = pd.Timestamp("2025-01-01")
    
    # Calculer les dernières dates autorisées avant les frontières
    # Dernière date autorisée dans l'entraînement
    train_end = (
        validation_start - pd.Timedelta(
            days=horizon + 1
        )
    )
    
    # Dernière date autorisée dans la validation
    validation_end = (
        test_start - pd.Timedelta(
            days=horizon +1
        )
    )
    
    # validation à partir du 2023-01-01
    train = (
        dataset.loc[
            dataset["date"] <= train_end
        ]
    ).copy()
    
    # validation entre 2023-01-01 et 2025-01-01
    validation = (
        dataset.loc[
            dataset["date"].between(
                left=validation_start,
                right=validation_end
            )
        ]
    ).copy()
    
    # test à partir du 2025-01-01
    test = (
        dataset.loc[
            dataset["date"] >= test_start
        ]
    ).copy()
                
    return train, validation, test

def validate_results(
    dataset_7d : pd.DataFrame, 
    dataset_30d : pd.DataFrame
) -> bool:
    """Contrôle de la qualité des datasets pour les horizons de volatilité à 7 et 30 jours"""
    for name, dataset in {
        "7d": dataset_7d,
        "30d": dataset_30d
    }.items():
        if dataset.empty:
            raise ValueError(
                f"Le dataset pour l'horizon {name} est vide"
            )
        if "date" not in dataset.columns:
            raise ValueError(
                f"Le dataset pour l'horizon {name} ne contient pas de colonne 'date'"
            )
        if dataset["date"].duplicated().any():
            raise ValueError(
                f"Le dataset pour l'horizon {name} contient des dates dupliquées"
            )
        if not dataset["date"].is_monotonic_increasing:
            raise ValueError(
                f"Le dataset pour l'horizon {name} n'est pas trié par date croissante"
            )
        if dataset.isna().any().any():
            raise ValueError(
                f"Le dataset pour l'horizon {name} contient des valeurs manquantes"
            )
    return True

def export_datasets(
    dataset_7d: pd.DataFrame,
    dataset_30d: pd.DataFrame,
    export_path: Path
) -> tuple[Path, Path]:
    """Exporter les datasets validés à 7 et 30 jours."""

    # Vérifier les datasets avant leur export
    validate_results(
        dataset_7d,
        dataset_30d
    )

    # Créer le dossier d'export s'il n'existe pas
    export_path = Path(export_path)

    export_path.mkdir(
        parents=True,
        exist_ok=True
    )

    # Définir les chemins des fichiers
    path_7d = export_path / "dataset_7d.csv"
    path_30d = export_path / "dataset_30d.csv"

    # Exporter les datasets
    dataset_7d.to_csv(
        path_7d,
        index=False,
        date_format="%Y-%m-%d"
    )

    dataset_30d.to_csv(
        path_30d,
        index=False,
        date_format="%Y-%m-%d"
    )

    return path_7d, path_30d

def main():
    """Point d'entrée principal pour la construction et l'export des datasets."""
    
    # Charger et préparer les données
    df = load_data(dataset_path)
    df_daily = prepare_data(df)
    
    # Créer les variables explicatives(les features)
    df_daily = create_features(df_daily)
    
    # Contruire les datasets d'entrainement pour les horizons à 7 et 30 jours
    dataset_7d, dataset_30d = build_training_dataset(df_daily)
    
    # Vérifier la qualité du dataset
    validate_results(dataset_7d, dataset_30d)
    
    # Créer les séparations temporelles 
    train_7d, validation_7d, test_7d = temporal_split_with_purge(dataset_7d, 7)
    train_30d, validation_30d, test_30d = temporal_split_with_purge(dataset_30d, 30)
    
    # Journaliser les dimensions des  ensembles
    logger.info(
        "Split 7 jours : train=%s, validation=%s, test=%s",
        len(train_7d),
        len(validation_7d),
        len(test_7d)
    )       
    
    logger.info(
            "Split 30 jours : train=%s, validation=%s, test=%s",
            len(train_30d),
            len(validation_30d),
            len(test_30d)
        )

    # Exporter les datatsets validés
    path_7d, path_30d = export_datasets(
        dataset_7d,
        dataset_30d,
        export_path
    )
    logger.info(
        "Datasets exportés : %s, %s",
        path_7d,
        path_30d
    )
        
if __name__ == "__main__":
    main()
