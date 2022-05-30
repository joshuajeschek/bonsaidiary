import typer
from . import config
from . import new

app = typer.Typer(no_args_is_help = True)
app.add_typer(config.app, name = 'config')
app.add_typer(new.app, name = 'new')

YES = False

@app.callback()
def main(yes: bool = False):
    '''
    command line utility for plant based instagram accounts
    '''
    YES = yes

if __name__ == '__main__':
    app()

