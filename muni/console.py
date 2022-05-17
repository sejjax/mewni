import click
import shutil
import pathlib


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project_name', type=click.Path())
def init(project_name):
    workdir = pathlib.Path().resolve()
    template_folder_path = pathlib.Path(__file__).parent.joinpath('template')
    generated_project_path = pathlib.Path(workdir).joinpath(project_name)
    print(f'Initializing project {project_name}')
    shutil.copytree(template_folder_path, generated_project_path)


def main():
    cli()
