import logging
from dotenv import load_dotenv
from config import setup
from fastapi import APIRouter, Query
from typing import List, Dict
from services.rag_service import RAGService

load_dotenv()

router = APIRouter(prefix="/collections")
logger = logging.getLogger(__name__)
rag_service = RAGService()

@router.get("/get-collection-docs")
async def get_collection_docs(
    collection: str = Query(..., description="Collection name.")
) -> List[Dict]:
    """Get all docs from a collection"""
    return await rag_service.get_collection_docs(collection)

@router.get("/similarity-search")
async def similarity_search(
    query: str = Query(..., description="Search parameters."),
    collection: str = Query(..., description="Collection name."),
    n_results: int = Query(3, description="Number of results.")
) -> List[Dict]:
    """Perform a similarity search inside collection"""
    return await rag_service.similarity_search( collection, query, n_results)

@router.post("/ingest-markdowns")
async def ingest_markdowns_endpoint():
    await setup.main()
    return {"status": "ok", "message": "Ingestão concluída"}
