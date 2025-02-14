import os
import subprocess
import json
from rich.console import Console
from reposcore.utils import Utils

console = Console()
utils = Utils()



def checkOutdatedDependency(path):
    score = 20
    cmd = ["mvn", "versions:display-dependency-updates"]
    
    utils.logInfo('Checking outdated dependencies...')
    result = subprocess.run(cmd, cwd=path, capture_output=True, text=True)
    
    outdated_deps = []
    for line in result.stdout.split("\n"):
        if "->" in line:
            outdated_deps.append(line.strip())
    utils.printTitle('Outdated Dependencies')
    utils.printText(f"Total: {len(outdated_deps)}")
    score = score - len(outdated_deps)
    return score

def checkSecurityDependency(path):
    severity_weights = {"critical": 20, "high": 15, "medium": 10, "low": 5}
    score = 50
    severity = set({})
    cmd = ["snyk", "test", "--json"]
    
    dependencyReport = open('./temp/snyk-report.json', 'w')
    try:
        with console.status("Checking dependencies...", spinner="dots2"):
                result = subprocess.run(cmd, cwd=path, check=True, stdout=dependencyReport, text=True)  
        utils.logInfo('Dependency check completed')
    except Exception as e:
        utils.logError(f"Vulnerabilities Found")

    with open('./temp/snyk-report.json', 'r') as f:
        report = json.loads(f.read())

    for vuln in report.get('vulnerabilities', []):
        severity.add(vuln['severity'])
        utils.logWarning(f"Vulnerability: {vuln['id']} ({vuln['severity']})")
        utils.logWarning(f"  Package: {vuln['packageName']} - {vuln['version']}")
        utils.logWarning(f"  Description: {vuln['title']}")
        print()
   
    for s in severity:
        score = score - severity_weights[s]
    
    return score


        