from agents.base_agent import BaseAgent
from models.schemas import AgentState
from services.rag_service import RAGService
import json
import logging

logger = logging.getLogger(__name__)

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
            
            logger.info(f"Init repo analysis.")

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
4. **Responda apenas com o schema de resposta sem incluir outras informações**

Schema de resposta:

{{
    "target_file": string | null,
    "change_type": string | null,
    "branch_prefix": string | null
}}

Exemplo de resposta para análise com sucesso:

{{
    "target_file": "caminho/do/arquivo",
    "change_type": "tipo de alteração",
    "branch_prefix": "prefixo-branch"
}}

Exemplo de resposta para análise sem sucesso:

{{
    "target_file": null,
    "change_type": null,
    "branch_prefix": null
}}"""
            
            response = await self.gemini_llm.ainvoke(analysis_prompt)

            logger.info(f"Repo analyser: {response}")
            
            try:
                content = response.content.strip()
        
                if content.startswith('```'):
                    start_idx = content.find('{')
                    end_idx = content.rfind('}')
                    
                    if start_idx != -1 and end_idx != -1:
                        content = content[start_idx:end_idx + 1]
                
                file_info = json.loads(content)

                state.file_info = file_info

                state.step = "repository_analyzed"
            except json.JSONDecodeError as j:
                state.error = f"Failed to parse repository analysis: {str(j)}"
            
        except Exception as e:
            state.error = f"Error analyzing repository: {str(e)}"
        
        return state