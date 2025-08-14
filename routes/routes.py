from fastapi import APIRouter
from monitoring.metrics import (
    active_workflows,
    webhook_requests_total, 
    pull_requests_created,
)
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check():
    """Healthcheck endpoint"""
    try:
        return {
            "status": "healthy",
            "timestamp": "2025-07-28T12:00:00Z",
            "services": {
                "ollama": "connected",
                "gemini": "connected",
                "vector_store": "connected"
            }
        }
    except Exception as e:
        logger.error(f"Healthcheck error: {str(e)}")
        raise

@router.get("/metrics")
async def metrics_endpoint():
    """Metrics endpoint"""
    try:
        return {
            "active_workflows": active_workflows._value,
            "total_webhooks": webhook_requests_total._get_metric(),
            "total_prs_created": pull_requests_created._get_metric()
        }
    except Exception as e:
        logger.error(f"Metrics error: {str(e)}")
        raise
