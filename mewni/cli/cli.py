import click
from .init import initialize_project
from .generate import generate_artifacts
from .migrate import migrate_db


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project_name', type=click.Path())
def init(project_name):
    initialize_project(project_name)


@cli.command()
@click.argument('object_type')
@click.argument('generated_file')
def create(object_type: str, generated_file):
    generate_artifacts(object_type, generated_file)


@cli.command()
def migrate():
    migrate_db()


def main():
    cli()
