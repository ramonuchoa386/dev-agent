from functools import wraps
from models.schemas import AgentState
import logging

logger = logging.getLogger(__name__)

def handle_agent_errors(func):
    """Decorator para tratamento de erros em agentes"""
    @wraps(func)
    async def wrapper(self, state: AgentState) -> AgentState:
        try:
            return await func(self, state)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            state.error = f"Error in {func.__name__}: {str(e)}"
            return state
    return wrapper