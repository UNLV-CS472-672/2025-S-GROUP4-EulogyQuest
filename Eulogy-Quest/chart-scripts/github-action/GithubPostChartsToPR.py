## ai-gen start (ChatGPT-4o, 1)

from github import Github
import os

token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY")
pr_number = int(os.getenv("PR_NUMBER"))
run_id = os.getenv("RUN_ID")
server = os.getenv("GITHUB_SERVER_URL", "https://github.com")

body = f"""
### Activity Charts

You can download team activity charts at the link below under Artifacts:

[Team Activity Charts]({server}/{repo_name}/actions/runs/{run_id})

"""

g = Github(token)
repo = g.get_repo(repo_name)
pr = repo.get_pull(pr_number)

# Look for an existing bot comment that starts with the same heading
existing_comment = None
for comment in pr.get_issue_comments():
    if comment.user.type == "Bot" and comment.user.login == "github-actions[bot]" and comment.body.startswith("### Activity Charts"):
        existing_comment = comment
        break

if existing_comment:
    existing_comment.edit(body)
    print("Updated existing PR comment.")
else:
    pr.create_issue_comment(body)
    print("Created new PR comment.")

## ai-gen end