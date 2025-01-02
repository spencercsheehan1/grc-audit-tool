# FILEPATH: matcha-sip.py

"""
matcha-sip.py
Description:
    -This script fetches all merged pull requests from the specified repositories and filters them by the date range specified in the script.
    -Recommended to sip matcha while running this script.
    
    The script then writes the pull requests to a text file in the following format:
        -Pull request number, pull request title, pull request url, merged_at date, and author username.

    The script creates a text file for each repository in a specified directory and also prints the pull request number to the console as it is being written to the file.

Usage:
    Run the script using the following command: python matcha-sip.py

Requirements:
    - Homebrew
    - Python 3,x

API Token:
    The script requires a GitHub API token to access the GitHub API.
    Please run this script with a token in the GITHUB_TOKEN environment variable.

Environment Variables:
    Set the environment variables prior to running the script each time per audit, Here's an example:
    export GITHUB_TOKEN={token_value}
    export START_DATE={YYYY-MM-DD}
    export END_DATE={YYYY-MM-DD}
    export GITHUB_REPOS={list of repos}
    OUTPUT DIR = os-environ {[Output Directory]}

Date Range:
    The script filters pull requests by the date range specified in the start date and end date variables.
    Please update these variables to the desired date range - you can ask auditors what this should be.

Repositories:
    The script fetches pull requests from the repositories specified in the REPOS List.
    Please update this list to include the desired repositories. Confirm with auditors what this should be.

Output:
    The output location is what you specifiy (see environment variables section above).
    The text file for each repository contains the pull requests that were merged within the specified date range.
    Yes, we know text files are annoying but this is the easiest way to get the data into the spreadsheet. We can work on a better solution later! :)
"""

import requests
import json
import os
from datetime import datetime, time

OWNER = "your-repo-name"
# these variables are defined by the user running the script prior to actual script run.
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
            headers=headers
        )
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
