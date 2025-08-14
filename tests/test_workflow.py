import pytest
from models.schemas import AgentState, GitHubWebhookPayload
from workflow.graph import create_workflow

@pytest.fixture
def sample_webhook_payload():
    return GitHubWebhookPayload(
        action="moved",
        project_card={
            "id": 12345,
            "column_name": "Ready for Development",
            "note": "Update version in config file"
        },
        repository={
            "name": "test-repo",
            "full_name": "user/test-repo",
            "clone_url": "https://github.com/user/test-repo.git",
            "default_branch": "main"
        },
        sender={"login": "testuser"}
    )

@pytest.mark.asyncio
async def test_workflow_execution(sample_webhook_payload):
    """Testa execução completa do workflow"""
    workflow = create_workflow()
    
    initial_state = AgentState(webhook_payload=sample_webhook_payload)
    
    result = await workflow.ainvoke(initial_state)
    
    assert result.step == "pr_created"
    assert result.pr_url is not None
    assert result.error is None
    
    assert workflow is not None