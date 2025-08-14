from fastapi import APIRouter, HTTPException, BackgroundTasks
from models.schemas import GitHubWebhookPayload, AgentState
from workflow.graph import create_workflow
from monitoring.metrics import (
    webhook_requests_total, 
    pull_requests_created,
    track_workflow_metrics
)
import logging
import json
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/webhook")
logger = logging.getLogger(__name__)
workflow = create_workflow()

@track_workflow_metrics("full_workflow")
async def process_github_webhook_with_metrics(payload: GitHubWebhookPayload):
    """Processa webhook do GitHub com métricas"""
    repo_name = payload.repository.get("name", "unknown")
    
    webhook_requests_total.labels(
        action=payload.action,
        repository=repo_name
    ).inc()
    
    try:
        initial_state = AgentState(webhook_payload=payload)        
        result = await workflow.ainvoke(initial_state)
        
        if getattr(result, "error", None):
            logger.error(f"Workflow failed for {repo_name}: {result.error}")
        else:
            logger.info(f"Workflow completed successfully for {repo_name}. PR: {result}")
            if getattr(result, "pr_url", None):
                pull_requests_created.labels(repository=repo_name).inc()
        
        return result
            
    except Exception as e:
        logger.error(f"Error processing webhook for {repo_name}: {str(e)}")
        raise

@router.post("/github")
async def github_webhook(
    payload: GitHubWebhookPayload,
    background_tasks: BackgroundTasks
):
    """Endpoint seguro para receber webhooks do GitHub"""
    
    try:
        if (payload.action == "labeled" and payload.label.get("name") == "bug"):

            background_tasks.add_task(process_github_webhook_with_metrics, payload)
            
            return {
                "status": "accepted",
                "message": "Webhook received and processing started",
                "repository": payload.repository.get("name"),
            }
        
        return {
            "status": "ignored",
            "message": "Webhook event not relevant for automation",
            "action": payload.action,
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

