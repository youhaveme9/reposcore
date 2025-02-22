## Github Repository security score

A python application to scan github repositories and assign a security score based on different well-defined security criterias and provides recommendation to improve the score

#### Scoring Factors

- Vulnerability in dependencies
- Outdated Dependencies
- Leaked secrets
- Repository Activity
- CI/CD misconfigurations*
- OWASP Score*
- Dependency popularity*

#### Installation
 1. Install uv from [here](https://github.com/astral-sh/uv)
 2. Install dependencies
    ```bash
    $ uv sync
    ```
 3. Activate virtual env created by uv
    ```bash
    $ source .venv/bin/activate
    ```

#### Usages

```bash
$ uv run main.py --url <GITHUB_REPO_URL>
```

  
