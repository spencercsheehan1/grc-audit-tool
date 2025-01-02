# matcha-sip
	

Sometimes during audits (SOX, SOC2, PCI, FedRAMP, etc.) we need to generate a list, or "population" of changes within a given set of github repositories. Depending on the environment, there may be hundreds of thousands of changes required to be generated in a given period. Therefore the Github API is necessary to download this volume of data. The GitHub CLI has too stringent of rate limiting, whereas the API can handle more requests. 

This python script fetches all merged pull requests from the specified repositories via the GitHub API, and filters them by the date range specified in the script.

The script writes the pull requests to a txt file in the following format: 
				
		Pull request number, pull request title, pull request url, merged_at date, author_username


The script creates a text file for each repository in a specified directory and also prints the pull request number to the console as it is being written to the file.


## Usage


  Run the script using the following command: 
	
	python matcha-sip.py


## Requirements
    - Homebrew
    - Python 3,x


## API Token
The script requires a GitHub API token to access the GitHub API.
Please run this script with a token in the GITHUB_TOKEN environment variable.

## Environment Variables
Set the environment variables prior to running the script each time per audit, Here's an example:

	export GITHUB_TOKEN={token_value}
	export START_DATE={YYYY-MM-DD}
	export END_DATE={YYYY-MM-DD}
	export GITHUB_REPOS={list of repos}
	OUTPUT DIR = os-environ {[Output Directory]}

## Date Range
The script filters pull requests by the date range specified in the start date and end date variables.
Please update these variables to the desired date range - you can ask auditors what this should be.


## Repositories
The script fetches pull requests from the repositories specified in the REPOS List.
Please update this list to include the desired repositories. Confirm with auditors what this should be.


## Output
The output location is what you specifiy (see environment variables section above).
The text file for each repository contains the pull requests that were merged within the specified date range.
