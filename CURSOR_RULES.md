# GRC Audit Tool (matcha-sip) Documentation

## Overview
The GRC Audit Tool, specifically `matcha-sip.py`, is a GitHub Pull Request auditing utility that generates reports of merged pull requests within a specified timeframe. The tool is designed to help teams track and review their pull request history across multiple repositories.

## Key Features
- Fetches merged pull requests from specified GitHub repositories
- Filters PRs by date range (currently set for 2024)
- Handles GitHub API rate limiting with retry mechanism
- Generates formatted text reports for each repository
- Includes error handling and failed request logging

## Prerequisites
Before running the tool, you need:
1. GitHub Personal Access Token with appropriate permissions
2. List of repositories to audit
3. Output directory for reports

## Environment Variables
The following environment variables must be set:

```bash
export GITHUB_TOKEN="your-github-token"        # Your GitHub API authentication token
export REPOS="repo1,repo2,repo3"              # Comma-separated list of repository names
export OUTPUT_DIR="~/pr-reports"              # Directory for output files
```

## Output Format
For each repository, the tool generates a text file (`{repo-name}.txt`) containing:

```
Pull Requests for {REPO} between {start_date} and {end_date}
--------------------------------------------------------------------------------

#{pr_number} - {pr_title}
Merged at: {merged_at}
URL: {url}

[Additional PRs...]

Failed Requests:
--------------------------------------------------------------------------------
[Any API request failures are listed here]
```

## Technical Details

### API Interaction
- Uses GitHub REST API v3
- Implements pagination (100 PRs per page)
- Includes rate limit checking before requests
- Features a 3-attempt retry mechanism for rate limit issues

### Data Collection Process
1. Iterates through each repository in `REPOS`
2. Fetches closed pull requests page by page
3. Filters for:
   - Merged PRs only
   - PRs within specified date range
4. Collects PR metadata:
   - PR number
   - Title
   - Merge timestamp
   - HTML URL

### Error Handling
- Checks API rate limits proactively
- Retries failed requests up to 3 times
- Logs failed requests in output files
- Provides helpful error messages for common issues (e.g., SSO configuration)

## Usage

1. Set up environment variables:
```bash
export GITHUB_TOKEN="your-github-token"
export REPOS="repo1,repo2,repo3"
export OUTPUT_DIR="~/pr-reports"
```

2. Run the script:
```bash
python matcha-sip.py
```

3. Check the output directory for generated reports

## Best Practices
- Ensure your GitHub token has appropriate permissions
- Enable SSO if required for your organization
- Monitor rate limits when auditing many repositories
- Keep the token secure and never commit it to version control

## Limitations
- Currently hardcoded to audit PRs from 2024
- Outputs in text format only
- Requires manual environment variable setup
- Limited to merged pull requests only

## Error Messages
Common error messages and their solutions:

1. "Rate limit exceeded":
   - Check token permissions
   - Verify SSO configuration at https://github.com/settings/tokens
   - Wait for rate limit reset

2. "API connection failed":
   - Verify token is valid
   - Check network connectivity
   - Ensure repository names are correct

## Future Improvements
Potential enhancements could include:
- Configurable date ranges
- CSV/JSON output formats
- Command-line arguments for configuration
- Support for GitHub Enterprise
- Concurrent repository processing 

# Branch Naming Guide

A concise convention for naming Git branches in this Python project. Following these rules keeps our history tidy, lets automation do its job, and helps new contributors ramp up quickly.

## 1 Primary Format

| Rule | Description | Example | Notes |
|------|-------------|---------|--------|
| kebab-case | Lower-case words separated by hyphens | `stone-mill-upgrade` | |
| Prefix | Namespace that explains why the branch exists | `feature/`, `bugfix/`, `hotfix/`, `chore/`, `docs/` | |
| No spaces | Spaces break Git commands & URLs | ✅ `feature/first-harvest` ❌ `feature/first harvest` | |
| Avoid punctuation | Only hyphens (-) and forward-slash prefix are allowed | `bugfix/umami-boost-overflow` | |

**TL;DR** — `<prefix>/<kebab-case-summary>`

## 2 Matcha-Themed A–Z Stubs

Pick the next unused stub (or choose one that best fits your work). Combine it with a prefix to form the final branch name.

| Letter | Stub (kebab-case) | Quick Note |
|--------|------------------|------------|
| A | aerated-leaves | Air-dried leaves; a light starting point |
| B | bitter-balance | Tweaking bitterness vs. sweetness |
| C | ceremonial-grade | Highest matcha quality |
| D | deep-steam | Longer steaming step | 