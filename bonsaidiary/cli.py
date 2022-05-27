import keyring
import os
import yaml
import requests
import getpass
from typing import Any, Dict, Tuple, Optional
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
    '''Load user config.'''
    try:
        with open(path, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        return {}
    return config

def is_valid_pat(pat: str) -> Tuple[int, str]:
    '''checks the GitHub Personal Access Token'''
    res = requests.get('https://api.github.com/user', headers={'Authorization': f'token {pat}'})
    if res.status_code != 200:
        return res.status_code, res.reason
    if  'repo' not in res.headers.get('x-oauth-scopes'):
        return 401, 'missing repo scope'
    return ()

def get_gh_pat() -> Optional[str]:
    '''read GitHub Personal Access Token from keyring or user'''
    pat = keyring.get_password(SERVICE, str(os.getuid()))
    pat = getpass.getpass('Please provide a GitHub Personal Access Token with repo scope: ') if not pat else pat
    while status := is_valid_pat(pat):
        if status[0] != 401:
            return print(f'[error] {status[1]}')
        pat = getpass.getpass(f'There is an error with your GitHub PAT ({status[1]}). \nPlease provide a valid token: ')
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
    if not pat:
        exit(-1)
    gh = Github(pat)

if __name__ == '__main__':
    main()

