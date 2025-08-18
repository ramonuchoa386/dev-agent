from agents.base_agent import BaseAgent
from models.schemas import AgentState
from services.git_service import GitService
import os

class CodeModifierAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.git_service = GitService()
    
    async def execute(self, state: AgentState) -> AgentState:
        """Clona repo, cria branch e modifica código"""
        try:
            if not state.repo_info or not state.file_info:
                state.error = "Missing repository or file information"
                return state
            
            repo_info = state.repo_info
            file_info = state.file_info
            
            repo_path = await self.git_service.clone_repository(
                repo_info["clone_url"],
                repo_info["name"]
            )
            
            branch_name = f"{file_info['branch_prefix']}-bug-{state.webhook_payload.label['id']}"
            await self.git_service.create_branch(repo_path, branch_name)
            state.branch_name = branch_name
            
            file_path = os.path.join(repo_path, file_info["target_file"])
            with open(file_path, 'r') as f:
                current_content = f.read()
            
            modification_prompt = f"""Você é um assistente de código especializado. Modifique o seguinte código:
Arquivo: {file_info["target_file"]}
Tipo de alteração: {file_info["change_type"]}
Contexto do card: {state.webhook_payload.issue.get('title', '')}

Código atual:
```
{current_content}
```

Retorne apenas o código modificado, sem explicações adicionais."""
            
            modified_code = await self.gemini_llm.ainvoke(modification_prompt)
            
            state.code_changes = modified_code.content
            
            with open(file_path, 'w') as f:
                f.write(modified_code.content.replace('```typescript\n', '').replace('```', ''))
            
            await self.git_service.commit_changes(
                repo_path,
                f"Auto-update: {file_info['change_type']} in {file_info['target_file']}"
            )
            
            state.step = "code_modified"
            
        except Exception as e:
            state.error = f"Error modifying code: {str(e)}"
        
        return state