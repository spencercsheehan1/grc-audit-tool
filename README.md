# matcha-sip

```
♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪

███╗   ███╗ █████╗ ████████╗ ██████╗██╗  ██╗ █████╗ 
████╗ ████║██╔══██╗╚══██╔══╝██╔════╝██║  ██║██╔══██╗
██╔████╔██║███████║   ██║   ██║     ███████║███████║
██║╚██╔╝██║██╔══██║   ██║   ██║     ██╔══██║██╔══██║
██║ ╚═╝ ██║██║  ██║   ██║   ╚██████╗██║  ██║██║  ██║
╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝

   ███████╗    ██╗    ██████╗     ██╗
   ██╔════╝    ██║    ██╔══██╗    ██║
   ███████╗    ██║    ██████╔╝    ██║
   ╚════██║    ██║    ██╔═══╝     ╚═╝
   ███████║    ██║    ██║         ██╗
   ╚══════╝    ╚═╝    ╚═╝         ╚═╝

♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪ ♫ ♪

   🍵 GitHub PR Audit Tool 🍵
```
*Note: This ASCII art displays in green when running the actual script!*
	

Sometimes during audits (SOX, SOC2, PCI, FedRAMP, etc.) we need to generate a list, or "population" of changes within a given set of github repositories. Depending on the environment, there may be hundreds of thousands of changes required to be generated in a given period. Therefore the Github API is necessary to download this volume of data. The GitHub CLI has too stringent of rate limiting, whereas the API can handle more requests. 

This python script fetches all merged pull requests from the specified repositories via the GitHub API, and filters them by the date range specified interactively.

The script writes the pull requests to a CSV file in the following format: 
				
		PR Number, Title, Author, Merged At, URL


The script creates a CSV file for each repository in a specified directory and also prints progress to the console as it processes.


## Requirements
- Homebrew
- Python 3.x
- pip (Python package installer)

## Setup

### 1. Virtual Environment (.venv)
First, create and activate a virtual environment to isolate project dependencies:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables (.env)
Create a `.env` file in the project root with your GitHub token:

```
# GitHub API Token (required)
GITHUB_TOKEN=your_github_token_here
```

Note: The `.env` file should never be committed to version control as it contains sensitive information.

## Usage
After setting up the virtual environment and GitHub token:

```bash
python matcha-sip.py
```

The script will interactively prompt you for:

1. **Repository Owner**: The GitHub organization or username that owns the repositories
   - Example: `microsoft`, `facebook`, or your personal GitHub username

2. **Repository Names**: The repositories you want to audit
   - You can enter multiple repositories in two ways:
     - All at once, separated by commas: `repo1,repo2,repo3`
     - One at a time (press Enter after each, then Enter on empty line when done)

3. **Start Date**: Beginning of the date range (format: YYYY-MM-DD)
   - Example: `2024-01-01`

4. **End Date**: End of the date range (format: YYYY-MM-DD)
   - Example: `2024-12-31`

5. **Output Directory**: Where to save the audit reports
   - Examples: `~/pr-reports`, `./output`, `/Users/username/audit-reports`
   - The directory will be created if it doesn't exist

## API Token
The script requires a GitHub API token to access the GitHub API. You can generate one at:
https://github.com/settings/tokens

If your organization uses SSO, make sure to enable it for your token.

## Output
The script generates one CSV file per repository in your specified output directory.
Each CSV file contains:
- Header row with column names
- Metadata comments with repository name, date range, and total PR count
- List of merged pull requests with:
  - PR number
  - Title
  - Author username
  - Merge timestamp
  - URL to the PR
- Any failed API requests (if applicable)

The CSV format makes it easy to:
- Import into Excel, Google Sheets, or other spreadsheet applications
- Sort and filter by any column
- Generate pivot tables and charts
- Share with auditors in a standard format

## Troubleshooting

### Virtual Environment
- If you see import errors, make sure you've activated the virtual environment
- Check that all dependencies are installed: `pip list`
- If needed, reinstall dependencies: `pip install -r requirements.txt`

### Environment Variables
- If you get environment variable errors, check that:
  - Your `.env` file exists and has the correct format
  - The GITHUB_TOKEN is properly set
- Make sure there are no spaces around the `=` in your `.env` file

### Rate Limiting
- The script includes automatic retry logic for rate limit issues
- If you consistently hit rate limits, ensure your token has proper permissions
- For SSO-enabled organizations, configure SSO for your token at https://github.com/settings/tokens
