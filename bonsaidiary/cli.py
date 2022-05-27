import typer
from . import config


app = typer.Typer(
        no_args_is_help=True,
        help='command line utility for plant based instagram accounts')
app.add_typer(config.app, name='config')

if __name__ == '__main__':
    app()

