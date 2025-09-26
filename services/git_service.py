import git
import os
import shutil
from typing import Optional
import asyncio

class GitService:
    def __init__(self):
        self.repos_dir = "./repos"
        os.makedirs(self.repos_dir, exist_ok=True)
    
    async def clone_repository(self, clone_url: str, repo_name: str) -> str:
        """Clona repositório"""
        repo_path = os.path.join(self.repos_dir, repo_name)
        
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
        
        await asyncio.to_thread(
            git.Repo.clone_from,
            clone_url,
            repo_path
        )
        
        return repo_path
    
    async def create_branch(self, repo_path: str, branch_name: str):
        """Cria nova branch"""
        repo = git.Repo(repo_path)
        new_branch = repo.create_head(branch_name)
        new_branch.checkout()
    
    async def commit_changes(self, repo_path: str, commit_message: str):
        """Commit das alterações"""
        repo = git.Repo(repo_path)
        repo.git.add(A=True)
        repo.index.commit(commit_message)
    
    async def push_branch(self, repo_name: str, branch_name: str):
        """Push da branch"""
        repo = git.Repo(f"./repos/{repo_name}")
        origin = repo.remote(name='origin')
        origin.set_url(f"https://ramonuchoa386:{os.getenv("GITHUB_TOKEN")}@github.com/ramonuchoa386/{repo_name}.git")
        origin.push(branch_name)