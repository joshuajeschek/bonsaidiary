import yaml
import os
import typer
import keyring
import getpass
import requests
import click_spinner 
from github import Github
from typing import Any, Dict, Optional, Tuple

SERVICE = 'bonsaidiary'
HOME = os.path.expanduser('~')
CONFIG_DIRECTORY = os.path.join(HOME, '.config', SERVICE)
CONFIG_PATH = os.path.join(CONFIG_DIRECTORY, f'{SERVICE}.yaml')

DEFAULT_CONFIG: Dict[str, Any] = {
    'diaries': []
}


def save_config(config: dict = DEFAULT_CONFIG, path: str = CONFIG_PATH):
    '''save user config'''
    os.makedirs(CONFIG_DIRECTORY, exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(config, f)

def load_config(path: str = CONFIG_PATH) -> dict:
    '''load user config'''
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
            return typer.secho(f'[error] {status[1]}', fg=typer.colors.RED)
        pat = getpass.getpass(f'There is an error with your GitHub PAT ({status[1]}). \nPlease provide a valid token: ')
    keyring.set_password(SERVICE, str(os.getuid()), pat)
    return pat

app = typer.Typer(no_args_is_help=True, help='configure the cli')

@app.command()
def clear():
    '''clear the saved configuration'''
    if not typer.confirm('Clear current configuration?'):
        raise typer.Abort()
    os.rmdir(CONFIG_DIRECTORY)
    typer.echo('Cleared configuration')

@app.command()
def logout():
    '''logout by deleting the GitHub PAT'''
    if not typer.confirm('Delete stored GitHub Personal Access Token?'):
        raise typer.Abort()
    keyring.delete_password(SERVICE, os.getuid())
    typer.echo('Deleted Github Personal Access Token!')

@app.command()
def show():
    '''show the current configuration'''
    config = load_config()
    if not config:
        typer.echo('No config available')
    else:
        typer.secho('Configuration:', bold=True)
        typer.echo('  ' + str(yaml.dump(config)).replace('\n', '\n  '))

    with click_spinner.spinner():
        pat = get_gh_pat()
        if not pat:
            return typer.echo('No GitHub Personal Access Token stored.')
        user = Github(pat).get_user().login
    typer.echo(f'Logged into GitHub as {typer.style(user, fg=typer.colors.GREEN)}')

