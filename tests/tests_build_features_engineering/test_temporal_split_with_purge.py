import sys
from pathlib import Path

import pandas as pd
import pytest

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from scripts.build_dataset.build_features_engineering import temporal_split_with_purge


@pytest.fixture
def temporal_dataset() -> pd.DataFrame:
    """Créer un dataset quotidien traversant les frontières temporelles."""
    
    dates = pd.date_range(
        start="2022-11-01",
        end="2025-02-01",
        freq="D",
    )
    
    df = pd.DataFrame(
        {
            "date" : dates,
            "value" : range(len(dates))
        }
    )
    return df

@pytest.mark.parametrize(
    "horizon",
    [7, 30]
)
def test_temporal_split_with_purge(
    temporal_dataset: pd.DataFrame,
    horizon: int, 
):

# Appeler la fonction temporal_split_with_purge avec le dataset et l'horizon donnés.
    train, validation, test = temporal_split_with_purge(
        temporal_dataset,
        horizon,
    )

# Vérifier que les ensembles de données ne sont pas vides.
    assert not train.empty
    assert not validation.empty
    assert not test.empty
    
# Vérifier les frontières  temporelles entre les ensembles de données.
    assert train["date"].max() < pd.Timestamp("2023-01-01")
    assert validation["date"].min() == pd.Timestamp("2023-01-01")
    assert validation["date"].max() < pd.Timestamp("2025-01-01")
    assert test["date"].min() == pd.Timestamp("2025-01-01")
    
# Vérifier la zone de purge avant la validation.
    assert train["date"].max() + pd.Timedelta(days=horizon) < validation["date"].min()
    
# Vérifier la zone de purge avant le test.
    assert validation["date"].max() + pd.Timedelta(days=horizon) < test["date"].min()
    
    
def test_temporal_split_rejects_invalid_horizon(
    temporal_dataset : pd.DataFrame,
):
    with pytest.raises(
        ValueError,
        match="7 soit 30"
    ):
        temporal_split_with_purge(
            temporal_dataset,
            horizon=14
        )