from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class GitHubWebhookPayload(BaseModel):
    action: str
    issue: Dict[str, Any]
    label: Dict[str, Any] = None
    repository: Dict[str, Any]
    organization: Dict[str, Any]
    sender: Dict[str, Any]

class AgentState(BaseModel):
    webhook_payload: Optional[GitHubWebhookPayload] = None
    repo_info: Optional[Dict[str, Any]] = None
    file_info: Optional[Dict[str, Optional[str]]] = None
    repository_context: Optional[str] = None
    code_changes: Optional[str] = None
    branch_name: Optional[str] = None
    pr_url: Optional[str] = None
    error: Optional[str] = None
    step: Optional[str] = None

class RepositoryConfig(BaseModel):
    repo_name: str
    target_files: List[str]
    branch_prefix: str = "auto-update"
    pr_template: Optional[str] = None