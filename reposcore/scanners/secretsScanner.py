import os
import subprocess
import json
from rich.console import Console
from reposcore.utils import Utils

console = Console()
utils = Utils()

def checkLeaks(path):
    score = 20
    secrets = []
    subprocess.run(["chmod", "o+w", "./temp"], check=True)
    secretReport = open('./temp/gitleaks-report.json', 'w')
    cmd = ["gitleaks", "dir", path]
    try:
        with console.status("Searching for leaked secrets...", spinner="dots2"):
                os.system(f"gitleaks dir {path} --report-path ./temp/gitleaks-report.json &>/dev/null") 
                
        utils.logInfo('Secrets scanning complete')
    except Exception as e:
        utils.logError(f"Secrets Found")
        print()

    with open('./temp/gitleaks-report.json', 'r') as f:
        report = json.loads(f.read())

    for leak in report:
        secrets.append(leak['Match'])
        utils.logWarning(f"Leak: {leak['RuleID']} ({leak['Description']})")
        utils.logWarning(f"  Secret: {leak['Match']}")
        utils.logWarning(f"  File: {leak['File']}")
        print()
    utils.printText(f"Total secrets found: {len(secrets)}")
    
    if len(secrets) > 2:
        score = score  - 10 - (len(secrets) - 2)
    else:
        score = score - len(secrets) * 5
    
    if score < 0:
        return 0
    return score

