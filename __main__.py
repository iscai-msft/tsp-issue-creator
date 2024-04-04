import argparse
from issues import create_issue, get_github_auth, get_repo, create_epic_issue
from typing import Dict, List

TYPESPEC_EPIC_REPO: str = "Azure/typespec-azure"

# mapping of codegen repos to assignees
TYPESPEC_CODEGEN_REPOS: Dict[str, List[str]] = {
    "Azure/autorest.python": ["iscai-msft", "tadelesh", "msyyc"],
    "Azure/autorest.typescript": ["joheredi", "qiaozha", "MaryGao"],
    "Azure/autorest.csharp": ["m-nash", "archerzz", "ArcturusZhang", "pshao25", "chunyu3"],
    "Azure/autorest.java": ["weidongxu-microsoft", "srnagar", "haolingdong-msft", "XiaofeiCao"],
    "Azure/autorest.go": ["jhendrixMSFT"],
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a github issue")
    parser.add_argument('--title', dest="title", type=str, help="Title of the feature you want to create an issue for")
    parser.add_argument('--body', dest="body", type=str, help="Body of the feature issue. Make it language agnostic, it will go into the issues for every language", default="")

    args = parser.parse_args()

    auth = get_github_auth()

    # create issues in each language emitter
    repos = [get_repo(repo_name, auth) for repo_name in TYPESPEC_CODEGEN_REPOS.keys()]
    issues = [
        create_issue(
            repo,
            title=args.title,
            body=args.body,
            assignees=TYPESPEC_CODEGEN_REPOS[repo.full_name],
        )
        for repo in repos
    ]

    # create epic issue keeping track of all of the emitters
    epic_issue = create_epic_issue(
        repo=get_repo(TYPESPEC_EPIC_REPO, auth), 
        title=args.title, 
        issues=issues
    )

    print(f"Created issues for feature: {args.title}"
          f"\nEpic issue: {epic_issue.html_url}")