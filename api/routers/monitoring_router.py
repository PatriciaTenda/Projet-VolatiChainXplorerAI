# charger les librairies nécessaires
from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

router = APIRouter(
    tags=["Monitoring predictions"]
)

@router.get(
    "/metrics",
    include_in_schema=False
)
def get_metrics():
    """Récupérer les métriques Prometheus pour le monitoring des prédictions"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
        status_code=200
    )
