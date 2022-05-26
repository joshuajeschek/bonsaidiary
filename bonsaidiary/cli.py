import keyring
import os
import yaml
import requests
from typing import Any, Dict, Optional
from github import Github, GithubException

SERVICE = 'bonsaidiary'
HOME = os.path.expanduser('~')
CONFIG_DIRECTORY = os.path.join(HOME, '.config', SERVICE)
CONFIG_PATH = os.path.join(CONFIG_DIRECTORY, f'{SERVICE}.yaml')

DEFAULT_CONFIG: Dict[str, Any] = {
    'diaries': []
}

def save_config(config: dict, path: str = CONFIG_PATH):
    os.makedirs(CONFIG_DIRECTORY, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(config, f)

def load_config(path: str = CONFIG_PATH) -> dict:
    """Load user config."""
    try:
        with open(path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        return {}
    return config

def is_valid_pat(pat: str) -> bool:
    res = requests.get('https://api.github.com/user', headers={'Authorization': f'token {pat}'})
    if res.status_code != 200:
        return False
    return 'repo' in res.headers.get('x-oauth-scopes')

def get_gh_pat() -> Optional[str]:
    """read GitHub Personal Access Token from keyring or user"""
    pat = keyring.get_password(SERVICE, str(os.getuid()))
    while not is_valid_pat(pat):
        pat = input('Could not find a valid Personal Access Token for GitHub. \nPlease provide one with repo scope: ')
    keyring.set_password(SERVICE, str(os.getuid()), pat)
    return pat

def main():
    print('Bonsaidiary 🌱')

    config = load_config()
    if not config:
        print('Loading default config...')
        config = DEFAULT_CONFIG
        save_config(config)

    pat = get_gh_pat()
    gh = Github(pat)

if __name__ == '__main__':
    main()

