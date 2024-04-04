import github
import github.Issue
import github.Repository

from dotenv import load_dotenv
from typing import List
import os

def create_task_list(title: str, issues: List[github.Issue.Issue]) -> str:
    """
    Creates a task list with the given issues and task type.

    Args:
        issues (list[Issue]): A list of issues.
        task_type (str): The type of task.

    Returns:
        str: The task list as a string.
    """
    buffer = f"```[tasklist]\n### {title}\n"
    for issue in issues:
        buffer += f"- [ ] {issue.html_url}\n"
    buffer += "```"
    return buffer

def get_issue(repo: github.Repository.Repository, issue_number: int) -> github.Issue.Issue:
    """Get the issue object for the given issue number in the given github repository"""
    print(f"Getting issue number: {issue_number}")
    print(f"Repo: {repo.full_name}")
    return repo.get_issue(number=issue_number)

def create_epic_issue(repo: github.Repository.Repository, *, title: str, issues: List[github.Issue.Issue]) -> github.Issue.Issue:
    print(f"Creating epic issue for feature: {title}")
    print(f"Repo: {repo.full_name}")
    body = create_task_list(title, issues)
    return repo.create_issue(title, body, assignee="iscai-msft")

def create_issue(repo: github.Repository.Repository, *, title: str, body: str, assignees: List[str]) -> github.Issue.Issue:
    """Create an issue in the given github repository"""
    print(f"Creating issue for feature: {title}")
    print(f"Repo: {repo.full_name}")
    repo.create_issue(title, body)
    return repo.create_issue(title, body, assignees=assignees)

def get_repo(repo_name: str, auth: github.Auth.Token) -> github.Repository.Repository:
    """Get the github repository object for the given repo name"""
    g = github.Github(auth=auth)
    return g.get_repo(repo_name)

def get_github_auth() -> github.Auth.Token:
    """Get the git hub token from the .env file"""
    # Load environment variables from .env file
    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN is not set in .env file. Please create a .env file at the root of this repo and set GITHUB_TOKEN=<your-github-token>")
    return github.Auth.Token(token)