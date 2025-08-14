from agents.base_agent import BaseAgent
from models.schemas import AgentState
from services.github_service import GitHubService

class PRCreatorAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.github_service = GitHubService()
    
    async def execute(self, state: AgentState) -> AgentState:
        """Cria pull request"""
        try:
            if not state.repo_info or not state.branch_name:
                state.error = "Missing repository info or branch name"
                return state
            
            repo_info = state.repo_info
            
            repo_path = f"./repos/{repo_info['name']}"
            await self.github_service.push_branch(repo_path, state.branch_name)
            
            pr_title = f"Auto-update: {state.file_info['change_type']}"
            pr_body = f"""This PR was automatically created based on project card movement.
**Changes made:**
- Modified: {state.file_info['target_file']}
- Type: {state.file_info['change_type']}

**Original card note:**
{state.webhook_payload.project_card.get('note', 'No note provided')}

**Branch:** {state.branch_name}"""
            
            pr_url = await self.github_service.create_pull_request(
                repo_info["full_name"],
                pr_title,
                pr_body,
                state.branch_name,
                repo_info["default_branch"]
            )
            
            state.pr_url = pr_url
            state.step = "pr_created"
            
        except Exception as e:
            state.error = f"Error creating PR: {str(e)}"
        
        return state