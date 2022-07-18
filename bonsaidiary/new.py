import os
import typer
from . import util
from . import cli
from . import diary

app = typer.Typer()

state = { 'name_default': os.getcwd().split(os.sep)[-1] }

def directory_callback(value: str):
    value = os.path.normpath(value)
    state['name_default'] = value.split(os.sep)[-1]
    return value

def add(directory: str, name: str, git: bool):
    typer.echo(f'Adding {typer.style(name, fg = typer.colors.GREEN)}...')
    if not os.path.exists(directory):
        typer.echo('Diary does not exist - cannot add non-existing directory')
        raise typer.Abort()

def create(directory: str, name: str, git: bool):
    typer.echo(f'Creating {typer.style(name, fg = typer.colors.GREEN)}...')
    os.makedirs(directory, exist_ok=True)
    os.chdir(directory)
    if os.listdir(directory):
        typer.echo('Directory not empty - cannot create new diary')
        raise typer.Abort()
    
    new_diary = diary.Diary()
    new_diary.save(os.path.join(directory, 'diary.json'))

@app.callback(invoke_without_command = True)
def main(
        directory: str=typer.Option(
            default=os.getcwd(),
            show_default=False,
            prompt=typer.style('Where should the diary be created?', bg=typer.colors.BLACK),
            help='the directory of the diary [default: <current directory>]',
            callback=directory_callback),
        name: str=typer.Option(
            default=lambda: state['name_default'],
            show_default=False,
            prompt=typer.style('What should the diary be called?', bg=typer.colors.BLACK),
            help='the name of the diary [default: <directory name>]'),
        git: bool=typer.Option(
            default=True,
            help='wether a git repository should be created'),
        exists: bool=typer.Option(
            default=False,
            help='wether th diary already exists')
        ):
    '''
    Create a new Diary.
    
     - pass `--no-git` to create a local-only diary
    
     - pass `--add` to add an existing diary (local or remote) to your configuration

     - to run the command without any more required input, pass directory and name as options
    '''

    typer.echo()

    directory =  os.path.abspath(os.path.expanduser(os.path.normpath(directory)))

    typer.echo(f'directory: {typer.style(directory, fg = typer.colors.GREEN)}')
    typer.echo(f'name: {typer.style(name, fg = typer.colors.GREEN)}')
    typer.echo(f'create git repo: {util.styled.YES if git else util.styled.NO}')
    typer.echo(f'exists: {util.styled.YES if exists else util.styled.NO}')

    typer.confirm(f'{"Add" if exists else "Create"} diary with the above configuration?',
            default=True, abort=True)
    
    if exists:
        add(directory, name, git)
    else:
        create(directory, name, git) 
    
