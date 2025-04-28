import getpass
import sys
import json
import requests
import time

REPO_URL = 'UNLV-CS472-672/2025-S-GROUP4-EulogyQuest'

# ai-gen start (ChatGPT-4-turbo, 1)
def githubRequest(url, headers):
    request = requests.get(url, headers)

    # Handle rate limits
    if request.status_code == 403 and "X-RateLimit-Remaining" in request.headers:
        reset_time = int(request.headers["X-RateLimit-Reset"])
        wait_seconds = reset_time - int(time.time())
        print(f"Rate limit reached. Sleeping for {wait_seconds} seconds...")
        time.sleep(wait_seconds + 1)
        print('Continuing...')
        return githubRequest(url, headers)  # Retry request after waiting
    
    if request.status_code != 200:
        print(f"Error fetching data from {url}: {request.status_code}, {request.text}")
        sys.exit(1)

    return request.json()
# ai-gen end

if __name__ == '__main__':
    # Prompt user for token
    token = getpass.getpass("Enter GitHub Token: ")
    headers = {'Authorization': f'Bearer {token}'}

    # Get data
    with open('chart_data.json', 'r') as file:
        chart_data = json.load(file)

    # Update data
    for username, userdata in chart_data.items():
        print('Getting data from ' + username)

        # Getting PR Count and Dates
        api_data = githubRequest(f'https://api.github.com/search/issues?q=author:{username}' + 
                                 f'+type:pr+repo:{REPO_URL}', headers).get('items')
        userdata['PR Dates'] = [pr['pull_request']['merged_at'] for pr in api_data 
                                if pr['pull_request']['merged_at'] != None]
        userdata['PR Count'] = len(userdata['PR Dates'])

        # Getting files changed and LOC changed count
        unique_files = set()
        LOC_changed = 0
        pr_urls = [pr['pull_request']['url'] for pr in api_data 
                   if pr['pull_request']['merged_at'] != None]
        for pr_url in pr_urls:
            files_url = f'{pr_url}/files'
            files = githubRequest(files_url, headers)
            for file in files:
                unique_files.add(file['filename'])
                LOC_changed += file.get('additions') + file.get('deletions')
        userdata['Files Changed'] = len(unique_files)
        userdata['LOC Changed'] = LOC_changed

        # Getting PR Review Count
        api_data = githubRequest(f'https://api.github.com/search/issues?q=reviewed-by:{username}' + 
                                 f'+type:pr+repo:{REPO_URL}', headers).get('items')
        userdata['PR Reviews'] = len([pr['pull_request']['merged_at'] for pr in api_data 
                                  if pr['pull_request']['merged_at'] != None 
                                  and pr['user']['login'] != username])

        # Getting Issue Count
        api_data = githubRequest(f'https://api.github.com/search/issues?q=author:{username}' + 
                                 f'+type:issue+repo:{REPO_URL}', headers).get('items')
        userdata['Issue Count'] = len([issue['state_reason'] for issue in api_data 
                                    if issue['state_reason'] == 'completed'])

        # Getting Issue Comment Count
        api_data = githubRequest(f'https://api.github.com/search/issues?q=commenter:{username}' + 
                                 f'+type:issue+repo:{REPO_URL}', headers).get('items')
        userdata['Issue Comments'] = len([issue['state_reason'] for issue in api_data 
                                  if issue['state_reason'] == 'completed' 
                                  and issue['user']['login'] != username])

    # # Write data to json file
    with open('chart_data.json', 'w') as file:
        json.dump(chart_data, file, indent=4)