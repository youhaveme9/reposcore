import re
import os
import sys
import requests
import subprocess
from rich import print
from pyfiglet import Figlet
from rich.console import Console

console = Console()

class Utils:
    def heading(self):
        f = Figlet(font='slant')
        print(f.renderText('RepoScore'))
        print("[bold green]v0.1.0[/bold green]")
        print("[bold green]------[/bold green]")
        print("[bold green]Get a security score for git repos[/bold green]")
        print("\n\n")

    def logInfo(self, message: str):
        print(f"[bold blue][+] {message}[/bold blue]")
    
    def logError(self, message: str):
        print(f"[bold red][-] {message}[/bold red]")

    def logWarning(self, message: str):
        print(f"[bold yellow][!] {message}[/bold yellow]")

    def printTitle(self, title: str):
        print(f"[bold green][{title}] : [/bold green]")

    def printText(self, text: str):
        print(f"[yellow]{text}[/yellow]")

    def validateUrl(self, url: str):
        urlPattern = r'''https://github\.com/([\w-]+)/([\w-]+)(\.git)?$'''
        match = re.match(urlPattern, url)

        # Check if url is valid
        if not match:
            self.logError('Invalid github repo url')
            sys.exit(1)

        owner, repo = match.groups()[:2]
        apiUrl = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(apiUrl)
        # Check if repo exists
        if response.status_code != 200:
            self.logError('Repo not found')
            sys.exit(1)
        return True
    
    def cloneRepo(self, url: str):
        path = os.path.join(os.getcwd(), 'temp', 'repo')
        if os.path.exists(path):
            self.logInfo('Repo directory already exists...')
            return
        self.validateUrl(url)
        try:
            with console.status("Cloning repo...", spinner="dots2"):
                subprocess.run(['git', 'clone', url, path], check=True)
            self.logInfo('Repo cloned successfully')
        except subprocess.CalledProcessError:
            self.logError('Failed to clone repo')
            sys.exit(1)

    def cleanup(self):
        path = os.path.join(os.getcwd(), 'temp')
        if os.path.exists(path):
            subprocess.run(['rm', '-rf', path])
        else:
            self.logInfo('Nothing to cleanup')