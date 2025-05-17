# FILEPATH: matcha-sip.py

import requests
import json
import os
from datetime import datetime, time

# Environment variables are defined by the user running the script prior to actual script run.
OWNER = "your-repo-name"
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPOS = os.environ["REPOS"].split(',')
OUTPUT_DIR = os.environ["OUTPUT_DIR"]

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"}

# Specify the API endpoint
api_url = "https://api.github.com/"

# Make a GET request
response = requests.get(api_url, headers=headers)

#  Check the status code
if response.status_code == 200:
    print("API connection successful.")
else:
    print("API connection failed. Status code:", response.status_code)

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)

def request_github_api(page, REPO):
    
    # Implementation of rate limit check
    def check_rate_limit():
        rate_limit_url = "https://api.github.com/rate_limit"
        response = requests.get(rate_limit_url, headers=headers)
        if response.status_code == 200:
            return response.json()["resources"]["core"]["remaining"]
        return None  # If API call was unsuccessful, return None

    remaining_requests = check_rate_limit()
    if remaining_requests is not None:
        if remaining_requests <= 0:
            print("GitHub API rate limit exceeded before making request. Please try again later.")
            return None, "Rate limit exceeded"
    if "API rate limit exceeded" in response.text:
        print("Please check if your GitHub API token is valid and has the correct permissions AND has SSO (Single Sign-On enabled) by going to https://github.com/settings/tokens and clicking Configure SSO.")
        return None, "Rate limit exceeded"
    print(f"Remaining requests before rate limit exceeded: {remaining_requests}")

    retries = 3
    for i in range(retries):
        print(f"Retries remaining: {retries - i}")
        response = requests.get(
            f"https://api.github.com/repos/{OWNER}/{REPO}/pulls?state=closed&per_page=100&page={page}",
            headers=headers)
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 403:
            print(f"Rate limit exceeded. Sleeping for {15 * (i + 1)} seconds...")
            time.sleep(15 * (i + 1))
        else:
            print(f"Unexpected status code: {response.status_code}")
            return None, f"Unexpected response {response.status_code} for page {page} of repo {REPO} after {retries} retries."
    print(f"Rate limit still exceeded after {retries} retries. Please try again later.")
    return None, "Rate limit still exceeded after retries. Please check if your GitHub API token is valid and has the correct permissions AND has SSO (Single Sign-On enabled) by going to https://github.com/settings/tokens and clicking Configure SSO."

for REPO in REPOS:
    OUTPUT_FILE_PATH = os.path.expanduser(os.path.join(OUTPUT_DIR, f"{REPO}.txt"))
    os.makedirs(os.path.dirname(OUTPUT_FILE_PATH), exist_ok=True)
    merged_pull_requests = []
    failed_requests = []
    page = 1
    stop_fetching = False  # <-- Flag for stopping the while loop
    while not stop_fetching:
        print(f"Processing page {page} for repository {REPO}")
        data, error = request_github_api(page, REPO)
        
        # Check if the request was successful
        if error:
            failed_requests.append({"page": page, "error": error})
            break
            
        if not data:  # Empty response means we've reached the end
            stop_fetching = True
            continue
            
        for pr in data:
            merged_at = pr.get('merged_at')
            if not merged_at:
                continue
                
            merged_date = datetime.strptime(merged_at, '%Y-%m-%dT%H:%M:%SZ')
            if start_date <= merged_date <= end_date:
                pr_info = {
                    "number": pr['number'],
                    "title": pr['title'],
                    "merged_at": merged_at,
                    "url": pr['html_url']
                }
                merged_pull_requests.append(pr_info)
            elif merged_date < start_date:  # If we've gone past our date range
                stop_fetching = True
                break
                
        page += 1

    # Write results to file
    with open(OUTPUT_FILE_PATH, 'w') as f:
        f.write(f"Pull Requests for {REPO} between {start_date.date()} and {end_date.date()}\n")
        f.write("-" * 80 + "\n\n")
        
        if merged_pull_requests:
            for pr in merged_pull_requests:
                f.write(f"#{pr['number']} - {pr['title']}\n")
                f.write(f"Merged at: {pr['merged_at']}\n")
                f.write(f"URL: {pr['url']}\n\n")
        else:
            f.write("No pull requests found in the specified date range.\n")
            
        if failed_requests:
            f.write("\nFailed Requests:\n")
            f.write("-" * 80 + "\n")
            for fail in failed_requests:
                f.write(f"Page {fail['page']}: {fail['error']}\n")

print("Script execution completed. Check the output files in the specified directory.")
