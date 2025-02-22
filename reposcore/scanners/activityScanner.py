import re
import requests
from reposcore.utils import Utils

utils = Utils()
def getActivityScore(url: str) -> int:
    score = 0
    urlPattern = r'''https://github\.com/([\w-]+)/([\w-]+)(\.git)?$'''
    match = re.match(urlPattern, url)

    owner, repo = match.groups()[:2]
    apiUrl = f"https://api.github.com/repos/{owner}/{repo}"
    repo_api = f"{apiUrl}"
    commits_api = f"{apiUrl}/commits"
    issues_api = f"{apiUrl}/issues"
    pulls_api = f"{apiUrl}/pulls"

    try:
        repo_data = requests.get(repo_api).json()
        commits_data = requests.get(commits_api).json()
        issues_data = requests.get(issues_api).json()
        pulls_data = requests.get(pulls_api).json()

        stars = repo_data.get("stargazers_count", 0)
        forks = repo_data.get("forks_count", 0)
        open_issues = len(issues_data) if isinstance(issues_data, list) else 0
        open_pulls = len(pulls_data) if isinstance(pulls_data, list) else 0
        last_updated = repo_data.get("pushed_at", "Unknown")
    except Exception:
        utils.logError("Error fetching data. Please try again.")
        return
    
        
    score += min(len(commits_data), 2)  
    score += min(open_issues * 2, 2)   
    score += min(open_pulls * 3, 2)    
    score += min(stars // 10, 2)     
    score += min(forks // 5, 2)        
      
    score = min(score, 10)
    
    utils.printTitle('Activities')
    utils.printText(f"Stars: {stars}")
    utils.printText(f"Forks: {forks}")
    utils.printText(f"Open Issues: {open_issues}")
    utils.printText(f"Open Pull Requests: {open_pulls}")
    utils.printText(f"Last Updated: {last_updated}")
    return score

   