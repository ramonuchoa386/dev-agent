from agents.base_agent import BaseAgent
from models.schemas import AgentState
import logging

logger = logging.getLogger(__name__)

class WebhookProcessorAgent(BaseAgent):
    async def execute(self, state: AgentState) -> AgentState:
        """Processa o webhook e extrai informações relevantes"""
        try:
            if not state.webhook_payload:
                state.error = "No webhook payload provided"
                return state
            
            payload = state.webhook_payload
            
            if (payload.action == "labeled" and payload.label.get("name") == "bug"):
                
                state.repo_info = {
                    "name": payload.repository["name"],
                    "full_name": payload.repository["full_name"],
                    "clone_url": payload.repository["clone_url"],
                    "default_branch": payload.repository["default_branch"]
                }
                
                # card_content = payload.project_card.get("note", "")
                state.step = "webhook_processed"
                
                logger.info(f"Webhook processed for repo: {state.repo_info['name']}")
                
            else:
                state.error = "Webhook action not relevant for automation"
                
        except Exception as e:
            state.error = f"Error processing webhook: {str(e)}"
            logger.error(state.error)
        
        return state