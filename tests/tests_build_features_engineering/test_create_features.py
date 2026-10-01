import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(project_root))



from scripts.build_dataset.build_features_engineering import create_features


@pytest.fixture
def dataset() -> pd.DataFrame:
    """Créer le dataset pour les tests."""
    
    dates = pd.date_range(
        start="2022-11-01",
        periods=40,
        freq="D"
    )
    
    dataset= pd.DataFrame(
        {
            "date" : dates,
            "close" : [100 + i for i in range(len(dates))],
            "high" : [105 + i for i in range(len(dates))],
            "low" : [95 + i for i in range(len(dates))],
            "open" : [98 + i for i in range(len(dates))],
            "volume" : [1000 + i for i in range(len(dates))],
            "market_cap" : [5000 + i for i in range(len(dates))]
        },
        index=dates
    )
    return dataset


def test_create_features(dataset: pd.DataFrame):

    dataset_with_features = create_features(dataset)

    expected_columns = [
        "log_return",
        "volatility_3d",
        "volatility_7d",
        "volatility_14d",
        "volatility_30d",
        "daily_range",
        "volume_change",
        "market_cap_change",
        "log_return_lag_1d",
        "log_return_lag_7d",
        "log_return_lag_30d"
    ]

    # Vérifier que toutes les features ont été créées
    for column in expected_columns:
        assert column in dataset_with_features.columns

    # Vérifier un calcul de rendement logarithmique
    expected_return = np.log(101 / 100)

    assert np.isclose(
        dataset_with_features.iloc[1]["log_return"],
        expected_return
    )

    # Le premier rendement doit être manquant
    assert pd.isna(
        dataset_with_features.iloc[0]["log_return"]
    )

    # Vérifier le décalage à un jour
    assert np.isclose(
        dataset_with_features.iloc[2]["log_return_lag_1d"],
        dataset_with_features.iloc[1]["log_return"]
    )

    # Vérifier qu'une volatilité à 30 jours a pu être calculée
    assert (
        dataset_with_features["volatility_30d"]
        .notna()
        .any()
    )