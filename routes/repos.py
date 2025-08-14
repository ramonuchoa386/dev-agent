import logging
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Query
from typing import List
from services.github_service import GitHubService

load_dotenv()

router = APIRouter(prefix="/repos")
logger = logging.getLogger(__name__)
github = GitHubService()

@router.get("/get-public-repos", response_model=List[str])
async def get_public_repos() -> List[str]:
    """Get list of public repositories endpoint"""
    try:
        return await github.get_public_repos()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get public repositories list.")

@router.get("/get-repo-clone-url")
async def get_repo_clone_url(
    repo: str = Query(..., description="Repo name.")
):
    """Get repository clone URL endpoint"""
    try:
        return await github.get_repo_clone_url(repo_name=repo)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get repository clone URL.")