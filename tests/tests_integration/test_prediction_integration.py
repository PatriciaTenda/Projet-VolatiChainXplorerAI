import math

import pytest
from fastapi.testclient import TestClient

from api.auths.dependencies import require_user_or_admin
from api.main import app

client = TestClient(app)

def fake_authenticated_user():
    """Simmuler smplement un utilisateur authentifié"""
    return object()


@pytest.mark.integration
@pytest.mark.parametrize(
    "horizon_days, expected_target",
    [
        (7, "target_volatility_7d"),
        (30, "target_volatility_30d"),
    ],
)
def test_real_prediction_chain(
    horizon_days,
    expected_target,
):
    """cette fonction teste la chaîne de prédiction réelle pour différents horizons de jours et cibles attendues."""
    app.dependency_overrides[require_user_or_admin] =(
        fake_authenticated_user
    )
    try:
        response = client.post(
            f"/api/v1/bitcoin/volatility/predictions/latest/{horizon_days}"
        )
        assert response.status_code == 200
        results = response.json()
        assert results["horizon_days"] == horizon_days
        assert results["target"] == expected_target
        assert results["model_name"] == "WeightedEnsemble_L2"
        predicted_volatility = results["predicted_volatility"]
        assert isinstance(predicted_volatility,float)
        assert math.isfinite(predicted_volatility)
        assert predicted_volatility >=0
        assert results["predicted_volatility_percent"] == pytest.approx(predicted_volatility*100)
        assert results["data_date"] is not None
    finally:
        app.dependency_overrides.pop(
            require_user_or_admin,
            None,
        )