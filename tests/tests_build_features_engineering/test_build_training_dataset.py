import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(project_root))



from scripts.build_dataset.build_features_engineering import (
    FEATURES_COLUMNS,
    build_training_dataset,
)


@pytest.fixture
def featured_dataset() -> pd.DataFrame:
    """Créer un dataset contenant toutes les features nécessaires."""

    dates = pd.date_range(
        start="2022-01-01",
        periods=60,
        freq="D",
        name="date"
    )

    # Fournir une valeur complète pour chaque feature
    data = {
        column: [
            1.0 + (0.01 * i)
            for i in range(len(dates))
        ]
        for column in FEATURES_COLUMNS
    }

    # Utiliser des rendements variables pour créer les cibles
    data["log_return"] = [
        0.01 * i
        for i in range(len(dates))
    ]

    return pd.DataFrame(
        data,
        index=dates
    )
    
    
def test_build_training_dataset(
    featured_dataset: pd.DataFrame
):

    dataset_7d, dataset_30d = (
        build_training_dataset(featured_dataset)
    )

    # Vérifier les types retournés
    assert isinstance(dataset_7d, pd.DataFrame)
    assert isinstance(dataset_30d, pd.DataFrame)

    # Vérifier que la date est redevenue une colonne
    assert "date" in dataset_7d.columns
    assert "date" in dataset_30d.columns

    # Vérifier que chaque dataset contient sa propre cible
    assert "target_volatility_7d" in dataset_7d.columns
    assert "target_volatility_30d" in dataset_30d.columns

    # Vérifier que les cibles ne sont pas mélangées
    assert "target_volatility_30d" not in dataset_7d.columns
    assert "target_volatility_7d" not in dataset_30d.columns

    # Vérifier l'absence de valeurs manquantes
    assert not dataset_7d.isna().any().any()
    assert not dataset_30d.isna().any().any()

    # La cible 30 jours fait perdre plus de lignes
    assert len(dataset_30d) < len(dataset_7d)
    
    
    
def test_build_training_dataset_rejects_missing_feature(
    featured_dataset: pd.DataFrame
):
    invalid_dataset = featured_dataset.drop(
        columns=["log_return_lag_30d"]
    )

    with pytest.raises(
        KeyError,
        match="manquantes"
    ):
        build_training_dataset(invalid_dataset)