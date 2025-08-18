from langgraph.graph import StateGraph, END
from models.schemas import AgentState
from agents.webhook_processor import WebhookProcessorAgent
from agents.repository_analyzer import RepositoryAnalyzerAgent
from agents.code_modifier import CodeModifierAgent
from agents.pr_creator import PRCreatorAgent

def should_continue(state: AgentState) -> str:
    """Determina o próximo passo baseado no state"""
    if state.error:
        return END
    
    if state.step == "webhook_processed":
        return "analyze_repository"
    elif state.step == "repository_analyzed":
        return "modify_code"
    elif state.step == "code_modified":
        return "create_pr"
    elif state.step == "pr_created":
        return END
    else:
        return END

def create_workflow():
    """Cria o workflow do LangGraph"""
    workflow = StateGraph(AgentState)
    
    workflow.add_node("process_webhook", WebhookProcessorAgent().execute)
    workflow.add_node("analyze_repository", RepositoryAnalyzerAgent().execute)
    workflow.add_node("modify_code", CodeModifierAgent().execute)
    workflow.add_node("create_pr", PRCreatorAgent().execute)
    
    workflow.set_entry_point("process_webhook")
    
    workflow.add_conditional_edges(
        "process_webhook",
        should_continue,
        {
            "analyze_repository": "analyze_repository",
            END: END
        }
    )
    
    workflow.add_conditional_edges(
        "analyze_repository",
        should_continue,
        {
            "modify_code": "modify_code",
            END: END
        }
    )
    
    workflow.add_conditional_edges(
        "modify_code",
        should_continue,
        {
            "create_pr": "create_pr",
            END: END
        }
    )
    
    workflow.add_conditional_edges(
        "create_pr",
        should_continue,
        {
            END: END
        }
    )
    
    return workflow.compile()