## ai-gen start (ChatGPT-4o, 2)
import os
from github import Github
from github.PullRequest import PullRequest

REPO = os.getenv("GITHUB_REPOSITORY")
PR_NUMBER = os.getenv("PR_NUMBER")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

run_id = os.getenv("RUN_ID")
repo = os.getenv("GITHUB_REPOSITORY")
server = os.getenv("GITHUB_SERVER_URL", "https://github.com")

# Load images into markdown format
def encode_image(path):
    with open(path, "rb") as f:
        import base64
        b64 = base64.b64encode(f.read()).decode('utf-8')
        return f"![chart]({{data:image/png;base64,{b64}}})"

charts = [
    encode_image("chart_1_weekly_prs.png"),
    encode_image("chart_2_individual_contributions.png"),
    encode_image("chart_3_files_changed.png"),
    encode_image("chart_4_loc_changed.png"),
]

body = """
### Activity Charts

You can download activity charts at the link below:
[Artifacts for this workflow run]({server}/{repo}/actions/runs/{run_id}/artifacts)

"""

# Post comment
g = Github(GITHUB_TOKEN)
repo = g.get_repo(REPO)
pr = repo.get_pull(int(PR_NUMBER))
pr.create_issue_comment(body)

## ai-gen end