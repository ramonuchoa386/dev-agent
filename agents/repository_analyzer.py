from agents.base_agent import BaseAgent
from models.schemas import AgentState
from services.rag_service import RAGService
import json

class RepositoryAnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.rag_service = RAGService()
    
    async def execute(self, state: AgentState) -> AgentState:
        """First bug analisys agent"""
        try:
            if not state.webhook_payload:
                state.error = "No webhook payload provided"
                return state
            
            repo_name = state.webhook_payload.repository["name"]
            bug_desc = state.webhook_payload.issue["body"]
            config_docs = await self.rag_service.similarity_search(collection='codebase', query=bug_desc, repo_name=repo_name)

            analysis_prompt = f"""Analise as seguintes informações sobre o repositório {repo_name}.

Descrição do problema:
{bug_desc}
                        
Configurações encontradas:
{json.dumps(config_docs, indent=2)}

Determine:
1. Qual arquivo deve ser modificado
2. Que tipo de alteração deve ser feita
3. Branch prefix a ser usado

Responda em formato JSON:
{{
    "target_file": "caminho/do/arquivo",
    "change_type": "tipo de alteração",
    "branch_prefix": "prefixo-branch"
}}"""

            print('-------------------------')
            print('REPO ANALIZER PROMPT: ', analysis_prompt)
            print('-------------------------')
            
            response = await self.gemini_llm.ainvoke(analysis_prompt)
            
            try:
                file_info = json.loads(response.content)
                print('-------------------------')
                print('FILE INFO: ', file_info)
                print('-------------------------')

                state.file_info = file_info
                print('-------------------------')
                print('STATE: ', state)
                print('-------------------------')

                state.step = "repository_analyzed"
                print('-------------------------')
                print('STATE: ', state)
                print('-------------------------')
            except json.JSONDecodeError:
                state.error = "Failed to parse repository analysis"
            
        except Exception as e:
            state.error = f"Error analyzing repository: {str(e)}"
        
        return state