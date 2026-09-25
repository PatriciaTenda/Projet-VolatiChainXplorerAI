import sys
from pathlib import Path

import pandas as pd
import pytest

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from scripts.build_dataset.build_features_engineering import validate_results


@pytest.fixture
def valid_datasets() -> tuple[
    pd.DataFrame, 
    pd.DataFrame
]:
    """Fixture providing a valid dataset with dates."""
    
    dates = pd.date_range(
        start="2023-01-01",
        periods=3,
        freq="D"
    )
   
    dataset_7d = pd.DataFrame(
        {
            "date": dates,
            "log_return": [0.01, 0.02, -0.01],
            "target_volatility_7d": [0.10, 0.12, 0.11]
        }
    )
    
    dataset_30d = pd.DataFrame(
        {
            "date": dates,
            "log_return": [0.01, 0.02, -0.01],
            "target_volatility_30d": [0.20, 0.22, 0.21]
        }
    )
    return dataset_7d, dataset_30d
    

def test_validate_results_accepted_valid_dataset(valid_datasets: tuple[pd.DataFrame, pd.DataFrame]):
    
    dataset_7d, dataset_30d = valid_datasets
    
    result = validate_results(
        dataset_7d, 
        dataset_30d
    )
    
    assert result is True
    
    
# Tester la présence de NaN
def test_validate_results_rejected_nan_dataset(
    valid_datasets : tuple[
        pd.DataFrame, 
        pd.DataFrame
        ]
):
    
    dataset_7d, dataset_30d = valid_datasets
    
    dataset_7d.loc[
        0,
        "target_volatility_7d"
    ] = float("nan")
    
    with pytest.raises(
        ValueError,
        match="valeurs manquantes"
    ):
        validate_results(
            dataset_7d, 
            dataset_30d
        )
        
        
def test_validate_results_rejected_empty_dataset(valid_datasets: tuple[pd.DataFrame, pd.DataFrame]):
    
    dataset_7d, dataset_30d = valid_datasets
    
    dataset_7d = dataset_7d.iloc[0:0]
    dataset_30d = dataset_30d.iloc[0:0]
    
    with pytest.raises(
        ValueError,
        match="vide"
        
    ):
        validate_results(
            dataset_7d, 
            dataset_30d
        )
        
def test_validate_results_rejects_duplicate_dates(
    valid_datasets: tuple[pd.DataFrame, pd.DataFrame]
):
    dataset_7d, dataset_30d = valid_datasets

    dataset_7d.loc[1, "date"] = dataset_7d.loc[0, "date"]

    with pytest.raises(
        ValueError,
        match="dates dupliquées"
    ):
        validate_results(
            dataset_7d,
            dataset_30d
        )
        
