import os
import re
import asyncio
from services.rag_service import RAGService

async def ingest_repository_markdowns(rag_service: RAGService, repo_name: str, directory_path: str):
    """
    Percorre um diretório recursivamente, lê arquivos markdown, extrai o conteúdo do código e o envia para o serviço RAG.
    """
    code_block_regex = r"```(?:tsx|typescript|jsx|javascript)?\n(.*?)```"

    print(f"Iniciando ingestão do diretório '{directory_path}' para o repositório '{repo_name}'")

    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(".md"):
                file_path = os.path.join(root, file_name)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        markdown_content = f.read()
                    
                    code_blocks = re.findall(code_block_regex, markdown_content, re.DOTALL)
                    
                    if not code_blocks:
                        continue

                    combined_code = "\n\n".join(block.strip() for block in code_blocks)
                    file_path_relative = os.path.relpath(file_path, directory_path)
                    
                    await rag_service.add_document(
                        collection='codebase',
                        repo_name=repo_name,
                        file_path=file_path_relative,
                        code_content=combined_code
                    )
                
                except Exception as e:
                    print(f"Erro ao processar o arquivo {file_path}: {e}")

async def main():
    rag_service = RAGService()
    documents_src = "./config/output"
    repository_name = ""
    
    await ingest_repository_markdowns(rag_service, repository_name, documents_src)
    
    print("\nIngestão de arquivos markdown concluída.")

if __name__ == "__main__":
    asyncio.run(main())

