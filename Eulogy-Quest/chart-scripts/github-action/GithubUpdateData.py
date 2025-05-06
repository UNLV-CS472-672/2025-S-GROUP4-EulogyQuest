## ai-gen start (ChatGPT-4o, 2)

import os
import requests
import json
from collections import defaultdict

REPO_OWNER = 'UNLV-CS472-672'
REPO_NAME = '2025-S-GROUP4-EulogyQuest'
BASE_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}'
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

nickname_map = {
    "kennethken73": "Ken",
    "adamohamou": "Adam",
    "michaelsoffer": "Michael",
    "risingchart719": "Parham",
    "kemoshu": "Kevin",
    "hhrh": "Hardy",
    "tannerdonovan": "Tanner",
    "kirchpa": "Jayson",
    "richvar": "Richard",
    "john-zaleschuk": "John"
}

HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github+json'
}

def fetch_all_paginated(url, params=None, filter_fn=None):
    items = []
    page = 1
    while True:
        paginated_params = params.copy() if params else {}
        paginated_params.update({'per_page': 100, 'page': page})
        resp = requests.get(url, headers=HEADERS, params=paginated_params)
        if resp.status_code != 200:
            print(f"Failed to fetch {url}: {resp.status_code} - {resp.text}")
            break
        data = resp.json()
        if not data:
            break
        if filter_fn:
            data = [item for item in data if filter_fn(item)]
        items.extend(data)
        page += 1
    return items

def fetch_pull_requests():
    print("Fetching all pull request data...")
    all_prs = fetch_all_paginated(f'{BASE_URL}/pulls', params={'state': 'all'})
    return [pr for pr in all_prs if pr['state'] == 'open' or pr['merged_at'] is not None]

def fetch_issues():
    print("Fetching all issue data...")
    return fetch_all_paginated(
        f'{BASE_URL}/issues',
        params={'state': 'all'},
        filter_fn=lambda i: 'pull_request' not in i
    )

def aggregate_contributions(prs, issues):
    print("Aggregating contributions...")
    contributions = defaultdict(lambda: {
        'Name': '',
        'PR Count': 0,
        'PR Dates': [],
        'PR Reviews': 0,
        'Issue Count': 0,
        'Issue Comments': 0,
        'Files Changed': 0,
        'LOC Changed': 0
    })

    for pr in prs:
        number = pr['number']
        pr_author = pr['user']['login'].lower()
        contributions[pr_author]['Name'] = nickname_map.get(pr_author, pr_author)
        contributions[pr_author]['PR Count'] += 1
        contributions[pr_author]['PR Dates'].append(pr['created_at'])

        pr_url = f"{BASE_URL}/pulls/{number}"
        resp = requests.get(pr_url, headers=HEADERS)
        if resp.status_code == 200:
            details = resp.json()
            contributions[pr_author]['Files Changed'] += details.get('changed_files', 0)
            contributions[pr_author]['LOC Changed'] += (
                details.get('additions', 0) + details.get('deletions', 0)
            )

        review_url = f"{BASE_URL}/pulls/{number}/reviews"
        reviews = fetch_all_paginated(review_url)
        VALID_REVIEW_STATES = {'APPROVED', 'CHANGES_REQUESTED', 'COMMENTED'}

        for r in reviews:
            reviewer = r['user']['login'].lower()
            if r['state'] in VALID_REVIEW_STATES:
                contributions[reviewer]['Name'] = nickname_map.get(reviewer, reviewer)
                contributions[reviewer]['PR Reviews'] += 1

    for issue in issues:
        user = issue['user']['login'].lower()
        contributions[user]['Name'] = nickname_map.get(user, user)
        contributions[user]['Issue Count'] += 1
        contributions[user]['Issue Comments'] += issue.get('comments', 0)

    return dict(contributions)

def main():
    prs = fetch_pull_requests()
    issues = fetch_issues()
    contributions = aggregate_contributions(prs, issues)

    print("Writing contributions to chart_data.json!")
    with open('chart_data.json', 'w') as f:
        json.dump(contributions, f, indent=4)

if __name__ == '__main__':
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN environment variable not set.")
    else:
        main()

## ai-gen end