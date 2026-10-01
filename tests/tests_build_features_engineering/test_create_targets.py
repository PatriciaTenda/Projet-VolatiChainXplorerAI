import sys
from pathlib import Path

import pandas as pd
import pytest

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(project_root))

from scripts.build_dataset.build_features_engineering import create_targets


@pytest.fixture
def dataset() -> pd.DataFrame:
    """Créer le dataset pour les tests."""
    
    dates = pd.date_range(
        start="2022-11-01",
        periods=50,
        freq="D"
    )
    
    dataset= pd.DataFrame(
        {
            "date" : dates,
            "log_return" : [0.01 * i for i in range(len(dates))],
            "target_7d" : [0.07 * i for i in range(len(dates))],
            "target_30d" : [0.30 * i for i in range(len(dates))],
        }
        ,
        index=dates
    )
    return dataset


def test_create_targets(dataset: pd.DataFrame):

    dataset_with_targets = create_targets(dataset)

    # Vérifier que les deux cibles ont été créées
    expected_columns = [
        "target_volatility_7d",
        "target_volatility_30d"
    ]

    for column in expected_columns:
        assert column in dataset_with_targets.columns

    # Calculer manuellement la première cible à 7 jours
    expected_target_7d = pd.Series(
        [0.01 * i for i in range(1, 8)]
    ).std()

    assert dataset_with_targets.iloc[
        0
    ]["target_volatility_7d"] == pytest.approx(
        expected_target_7d
    )

    # Calculer manuellement la première cible à 30 jours
    expected_target_30d = pd.Series(
        [0.01 * i for i in range(1, 31)]
    ).std()

    assert dataset_with_targets.iloc[
        0
    ]["target_volatility_30d"] == pytest.approx(
        expected_target_30d
    )

    # Les dernières lignes ne disposent pas d'un futur complet
    assert (
        dataset_with_targets["target_volatility_7d"]
        .tail(7)
        .isna()
        .all()
    )

    assert (
        dataset_with_targets["target_volatility_30d"]
        .tail(30)
        .isna()
        .all()
    )
 
