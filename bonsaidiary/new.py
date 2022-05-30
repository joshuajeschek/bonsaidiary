import os
import typer
from . import util
from . import cli

app = typer.Typer()

state = { 'name_default': os.getcwd().split(os.sep)[-1] }

def directory_callback(value: str):
    value = os.path.normpath(value)
    state['name_default'] = value.split(os.sep)[-1]
    return value

@app.callback(invoke_without_command = True)
def main(
        directory: str = typer.Option(
            default = os.getcwd(),
            show_default = False,
            prompt = typer.style('Where should the diary be created?', bg=typer.colors.BLACK),
            help = 'the directory of the diary [default: <current directory>]',
            callback = directory_callback),
        name: str = typer.Option(
            default = lambda: state['name_default'],
            show_default = False,
            prompt = typer.style('What should the diary be called?', bg=typer.colors.BLACK),
            help = 'the name of the diary [default: <directory name>]'),
        git: bool = typer.Option(
            default = True,
            help = 'wether a git repository should be created'),
        add: bool = typer.Option(
            default = False,
            help = 'wether th diary already exists')
        ):
    '''
    Create a new Diary.
    
     - pass `--no-git` to create a local-only diary
    
     - pass `--add` to add an existing diary (local or remote) to your configuration

     - to run the command without any more required input, pass directory and name as options
    '''
    typer.echo()
    typer.echo(f'directory: {typer.style(directory, fg = typer.colors.GREEN)}')
    typer.echo(f'name: {typer.style(name, fg = typer.colors.GREEN)}')
    typer.echo(f'create git repo: {util.styled.YES if git else util.styled.NO}')
    typer.echo(f'exists: {util.styled.YES if add else util.styled.NO}')

    typer.confirm(f'{"Add" if add else "Create"} diary with the above configuration?',
            default = True, abort = True)

    typer.echo(f'{"Adding" if add else "Creating"} {typer.style(name, fg = typer.colors.GREEN)}...')

