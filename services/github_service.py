from github import Github
import os

class GitHubService:
    def __init__(self):
        self.github = Github(os.getenv("GITHUB_TOKEN"))
    
    async def create_pull_request(
        self,
        repo_full_name: str,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str
    ) -> str:
        """Cria pull request"""
        repo = self.github.get_repo(repo_full_name)
        
        pr = repo.create_pull(
            title=title,
            body=body,
            head=head_branch,
            base=base_branch
        )
        
        return pr.html_url
    
    # async def update_file(
    #     self,
    #     file_path: str,
    #     commit_message: str,
    #     file_content: str,
    #     file_prev_sha: str,
    #     branch: str
    # ) -> str:
    #     """Cria pull request"""
    #     repo = self.github.get_repo()
        
    #     pr = repo.update_file(
    #         path=file_path,
    #         message=commit_message,
    #         content=file_content,
    #         sha=file_prev_sha,
    #         branch=branch
    #     )
        
    #     return pr.html_url
    
    async def get_public_repos(self):
        """Resgatar lista de repositórios no Github"""
        public_repos = self.github.get_user().get_repos()

        return [repo.name for repo in public_repos]
    
    async def get_repo_clone_url(self, repo_name: str) -> str:
        """Resgatar a URL para clonar um repositório no Github"""
        repo_detail = self.github.get_user().get_repo(repo_name)

        return repo_detail.clone_url
    
    async def get_issue_comments(
        self,
        repo_full_name: str,
        issue_number: int
    ) -> str:
        """Resgata todos os comentários em uma issue"""
        repo = self.github.get_repo(repo_full_name)
        issue = repo.get_issue(
            number=issue_number,
        )
        comments = issue.get_comments()
        all_comments = []

        for comment in comments:
            all_comments.append(comment.body)

        comments_string = "\n".join(all_comments)
        
        return comments_string