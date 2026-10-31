import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Permettre l’import des modules du projet
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))


from api.main import app

client = TestClient(app)


def test_metrics_endpoint():
    """Vérifier que les métriques Prometheus sont accessibles."""

    response = client.get("/metrics")

    # Vérifier la réponse HTTP
    assert response.status_code == 200

    # Vérifier le format Prometheus
    assert response.headers["content-type"].startswith(
        "text/plain"
    )

    # Vérifier la présence des quatre métriques
    expected_metrics = [
        "volatichainxplorerai_prediction_counter_request_total",
        "volatichainxplorerai_prediction_duration_seconds",
        "volatichainxplorerai_predicted_volatility",
        "volatichainxplorerai_input_data_age_days",
    ]

    for metric_name in expected_metrics:
        assert metric_name in response.text