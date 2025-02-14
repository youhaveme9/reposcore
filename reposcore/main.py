import os
import sys
import time
from reposcore.utils import Utils
from reposcore.scanners.dependency import checkSecurityDependency, checkOutdatedDependency
from reposcore.scanners.secretsScanner import checkLeaks
from reposcore.scanners.activityScanner import getActivityScore

utils = Utils()

def main(url: str):
    utils.heading()
    utils.cloneRepo(url)

    # score for dependency security
    dependencyScore = checkSecurityDependency(os.path.join(os.getcwd(), 'temp', 'repo'))
    utils.printTitle('Dependency security score')
    utils.printText(f"Score: {dependencyScore}/50")
    print()

    # score for outdated dependencies
    outdatedScore = checkOutdatedDependency(os.path.join(os.getcwd(), 'temp', 'repo'))
    utils.printTitle('Outdated Dependency score')
    utils.printText(f"Score: {outdatedScore}/20")
    print()

    # score for leaked secrets
    secretsScore = checkLeaks(os.path.join(os.getcwd(), 'temp', 'repo'))
    print()
    utils.printTitle('Leaked secrets score')
    utils.printText(f"Score: {secretsScore}/20")
    print()

    # score for activity
    activityScore = getActivityScore(url)
    print()
    utils.printTitle('Repo activity score')
    utils.printText(f"Score: {activityScore}/10")
    print()

    print("==============================")
    utils.printTitle("Overall Score")
    print("==============================")
    utils.printText(f"Vulnerability from dependencies: {dependencyScore}/50")
    utils.printText(f"Outdated dependencies score: {outdatedScore}/20")
    utils.printText(f"Leaked secrets score: {secretsScore}/20")
    utils.printText(f"Activity score: {activityScore}/10")
    print()
    totalScore = dependencyScore + outdatedScore + secretsScore + activityScore
    utils.printText(f"Total repo score: {totalScore}/100")

    # cleanup
    utils.cleanup()

