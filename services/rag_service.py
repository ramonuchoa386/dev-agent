import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class RAGService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./vector_store", settings=Settings(anonymized_telemetry=False))        
        self.code_collection = self.client.get_or_create_collection("codebase")
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')

    async def get_collection_docs(self, collection: str) -> List[Dict]:
        """Get all documents from a collection"""
        col = self.client.get_collection(name=collection)
        
        results = col.get()
        
        return [
            {
                "content": doc,
                "metadata": meta
            }
            for doc, meta in zip(
                results.get("documents", []),
                results.get("metadatas", [])
            )
        ]
    
    async def add_document(self, collection: str, repo_name: str, file_path: str, code_content: str):
        """Add a single document to a collection."""
        
        embedding = self.encoder.encode([code_content])
        document_id = f"{repo_name}_{file_path.replace('/', '_').replace('.', '_')}"

        col = self.client.get_collection(name=collection)
        
        col.add(
            embeddings=embedding.tolist(),
            documents=[code_content],
            metadatas=[{
                "repo_name": repo_name,
                "file_path": file_path,
                "document_type": "code"
            }],
            ids=[document_id]
        )
        
        print(f"Documento de código '{file_path}' do repositório '{repo_name}' adicionado com sucesso.")
    
    async def similarity_search(self, collection: str, query: str, n_results: int = 3, **filters) -> List[Dict]:
        """Performa a similarity search on entire collection."""
        embedding = self.encoder.encode([query])
        col = self.client.get_collection(collection)

        where_filter = {}

        for key, value in filters.items():
            where_filter[key] = {"$eq": value}
        
        results = col.query(
            query_embeddings=embedding.tolist(),
            n_results=n_results,
            where=where_filter
        )
        
        return [
            {
                "content": doc,
                "metadata": meta
            }
            for doc, meta in zip(
                results.get("documents", []),
                results.get("metadatas", [])
            )
        ]