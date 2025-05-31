# FILEPATH: matcha-sip.py

import requests
import json
import os
import csv
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Only GitHub token is loaded from .env file
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable is required. Please set it in your .env file.")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"}

# Verify API connection before proceeding
def verify_api_connection():
    """Test the GitHub API connection and provide detailed troubleshooting if it fails."""
    print("Verifying GitHub API connection...")
    
    # Test basic API endpoint
    api_url = "https://api.github.com/"
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        print("✓ API connection successful")
        
        # Also test authenticated endpoint
        user_url = "https://api.github.com/user"
        user_response = requests.get(user_url, headers=headers)
        
        if user_response.status_code == 200:
            user_data = user_response.json()
            print(f"✓ Authenticated as: {user_data.get('login', 'Unknown')}")
            return True
        elif user_response.status_code == 401:
            print("\n❌ Authentication failed!")
            print_auth_troubleshooting()
            return False
    else:
        print(f"\n❌ API connection failed. Status code: {response.status_code}")
        print_connection_troubleshooting()
        return False

def print_auth_troubleshooting():
    """Print detailed authentication troubleshooting steps."""
    print("\n" + "="*60)
    print("AUTHENTICATION TROUBLESHOOTING")
    print("="*60)
    
    print("\n1. CHECK YOUR .env FILE FORMAT:")
    print("   Your .env file should contain exactly:")
    print("   GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx")
    print("\n   Common mistakes:")
    print("   ❌ GITHUB_TOKEN=\"ghp_xxx\"  (no quotes!)")
    print("   ❌ GITHUB_TOKEN = ghp_xxx   (no spaces!)")
    print("   ❌ GITHUB_API_TOKEN=ghp_xxx (wrong variable name!)")
    
    print("\n2. VERIFY TOKEN LOCATION:")
    print(f"   Current directory: {os.getcwd()}")
    print("   Your .env file must be in the same directory as matcha-sip.py")
    
    print("\n3. CHECK TOKEN VALIDITY:")
    print("   • Go to: https://github.com/settings/tokens")
    print("   • Verify your token hasn't expired")
    print("   • Ensure it has 'repo' scope selected")
    print("   • If using SSO, click 'Configure SSO' and authorize for your organization")
    
    print("\n4. CREATE A NEW TOKEN:")
    print("   • Go to: https://github.com/settings/tokens")
    print("   • Click 'Generate new token' → 'Generate new token (classic)'")
    print("   • Select scopes: ✓ repo (Full control of private repositories)")
    print("   • Copy the token immediately (starts with ghp_)")
    print("   • Add to .env file: GITHUB_TOKEN=ghp_your_token_here")
    
    print("\n5. TEST YOUR TOKEN:")
    print("   Run this command to test your token:")
    print(f"   curl -H \"Authorization: token {GITHUB_TOKEN[:10]}...\" https://api.github.com/user")
    
    print("\n" + "="*60)

def print_connection_troubleshooting():
    """Print general connection troubleshooting steps."""
    print("\n" + "="*60)
    print("CONNECTION TROUBLESHOOTING")
    print("="*60)
    
    print("\n1. CHECK INTERNET CONNECTION:")
    print("   Try: curl https://api.github.com/")
    
    print("\n2. CHECK PROXY/FIREWALL:")
    print("   If behind a corporate firewall, you may need proxy settings")
    
    print("\n3. CHECK GITHUB STATUS:")
    print("   Visit: https://www.githubstatus.com/")
    
    print("\n" + "="*60)

# Get the owner of the repository
def get_org_name_or_user_name():
    owner = input("Enter the owner of the repository: ").strip()
    if owner == "":
        print("Name of owner of repos required. Can be the name of the GitHub organization if repo is owned by an organization, or alternatively, the GitHub username if repo is owned by a user. Please try again.")
        return get_org_name_or_user_name()
    return owner

# Get the name of the repository
def get_repo_name():
    print("\n=== Repository Input ===")
    print("You can enter repositories in two ways:")
    print("1. All at once: separate multiple repos with commas")
    print("   Example: repo1,repo2,repo3")
    print("2. One at a time: press Enter after each repo")
    print("   When finished, press Enter on an empty line\n")
    
    repos = []
    while True:
        repo_input = input("Enter repository name(s): ").strip()
        
        if ',' in repo_input:
            # Handle comma-separated input
            new_repos = [r.strip() for r in repo_input.split(',') if r.strip()]
            if new_repos:
                repos.extend(new_repos)
                print(f"Added {len(new_repos)} repositories")
                break
            else:
                print("No valid repository names found. Please try again.")
        elif repo_input:
            # Handle single repository
            repos.append(repo_input)
            print(f"Added repository: {repo_input}")
        elif not repo_input and repos:
            # Empty input with some repos already added - we're done
            break
        elif not repo_input:
            # Empty input with no repos - ask again
            print("Please enter at least one repository name")
            continue
    
    print(f"\nFinal repository list ({len(repos)}):")
    for i, repo in enumerate(repos, 1):
        print(f"{i}. {repo}")
    
    return repos

# Get the start date
def get_start_date():
    start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
    if start_date == "":
        print("Start date is required. Please try again.")
        return get_start_date()
    return start_date

# Get the end date
def get_end_date():
    end_date = input("Enter the end date (YYYY-MM-DD): ").strip()
    if end_date == "":
        print("End date is required. Please try again.")
        return get_end_date()
    return end_date

# Get the output directory
def get_output_directory():
    print("\n=== Output Directory ===")
    print("Enter the directory where you want to save the PR reports.")
    print("Examples: ~/pr-reports, ./output, /Users/username/audit-reports")
    
    output_dir = input("Enter output directory path: ").strip()
    if output_dir == "":
        print("Output directory is required. Please try again.")
        return get_output_directory()
    
    # Expand user home directory if needed
    output_dir = os.path.expanduser(output_dir)
    
    # Create directory if it doesn't exist
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Output directory set to: {output_dir}")
        return output_dir
    except Exception as e:
        print(f"Error creating directory: {e}")
        print("Please enter a valid directory path.")
        return get_output_directory()

# Request the GitHub API
def request_github_api(page, owner, repo):
    
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
    print(f"Remaining requests before rate limit exceeded: {remaining_requests}")

    retries = 3
    for i in range(retries):
        print(f"Retries remaining: {retries - i}")
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&per_page=100&page={page}",
            headers=headers)
        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 403:
            if "API rate limit exceeded" in response.text:
                print("Please check if your GitHub API token is valid and has the correct permissions AND has SSO (Single Sign-On enabled) by going to https://github.com/settings/tokens and clicking Configure SSO.")
                return None, "Rate limit exceeded"
            print(f"Rate limit exceeded. Sleeping for {15 * (i + 1)} seconds...")
            time.sleep(15 * (i + 1))
        else:
            print(f"Unexpected status code: {response.status_code}")
            return None, f"Unexpected response {response.status_code} for page {page} of repo {repo} after {retries} retries."
    print(f"Rate limit still exceeded after {retries} retries. Please try again later.")
    return None, "Rate limit still exceeded after retries. Please check if your GitHub API token is valid and has the correct permissions AND has SSO (Single Sign-On enabled) by going to https://github.com/settings/tokens and clicking Configure SSO."

def main():
    # Verify API connection first
    if not verify_api_connection():
        print("\n⚠️  Exiting due to API connection failure.")
        print("Please fix the issues above and try again.")
        return
    
    print("\n" + "-"*60)
    print("Starting repository audit...")
    print("-"*60 + "\n")
    
    #1. Get owner of the repository
    owner = get_org_name_or_user_name()

    #2. Get repositories
    repos = get_repo_name()

    #3. Get start date
    start_date_str = get_start_date()
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

    #4. Get end date
    end_date_str = get_end_date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    #5. Get output directory
    output_dir = get_output_directory()

    #6. Process each repository
    for repo in repos:
        print(f"\nProcessing repository: {owner}/{repo}")
        page = 1
        stop_fetching = False
        merged_pull_requests = []
        failed_requests = []
        
        while not stop_fetching:
            print(f"Processing page {page}")
            data, error = request_github_api(page, owner, repo)
            
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
                        "url": pr['html_url'],
                        "author": pr['user']['login'] if pr.get('user') else 'Unknown'
                    }
                    merged_pull_requests.append(pr_info)
                elif merged_date < start_date:  # If we've gone past our date range
                    stop_fetching = True
                    break
                    
            page += 1

        # Write results to CSV file for this repository
        OUTPUT_FILE_PATH = os.path.join(output_dir, f"{repo}.csv")
        
        with open(OUTPUT_FILE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['PR Number', 'Title', 'Author', 'Merged At', 'URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write header
            writer.writeheader()
            
            # Write metadata as comment rows
            writer.writerow({
                'PR Number': f'# Repository: {owner}/{repo}',
                'Title': '',
                'Author': '',
                'Merged At': '',
                'URL': ''
            })
            writer.writerow({
                'PR Number': f'# Date Range: {start_date.date()} to {end_date.date()}',
                'Title': '',
                'Author': '',
                'Merged At': '',
                'URL': ''
            })
            writer.writerow({
                'PR Number': f'# Total PRs: {len(merged_pull_requests)}',
                'Title': '',
                'Author': '',
                'Merged At': '',
                'URL': ''
            })
            
            # Empty row for separation
            writer.writerow({})
            
            # Write PR data
            if merged_pull_requests:
                for pr in merged_pull_requests:
                    writer.writerow({
                        'PR Number': f"#{pr['number']}",
                        'Title': pr['title'],
                        'Author': pr['author'],
                        'Merged At': pr['merged_at'],
                        'URL': pr['url']
                    })
            
            # Write failed requests if any
            if failed_requests:
                # Add empty rows for separation
                writer.writerow({})
                writer.writerow({})
                writer.writerow({
                    'PR Number': '# Failed Requests:',
                    'Title': '',
                    'Author': '',
                    'Merged At': '',
                    'URL': ''
                })
                for fail in failed_requests:
                    writer.writerow({
                        'PR Number': f"# Page {fail['page']}",
                        'Title': fail['error'],
                        'Author': '',
                        'Merged At': '',
                        'URL': ''
                    })
        
        print(f"CSV file created: {OUTPUT_FILE_PATH}")

    print(f"\nScript execution completed. Check the CSV files in {output_dir}")

if __name__ == "__main__":
    main()
    