#  This is core cli file. You can call it using "ni" or "mewni" commands
import os

import click
import shutil
import pathlib
import jinja2
import enum


@click.group()
def cli():
    pass


@cli.command()
@click.argument('project_name', type=click.Path())
def init(project_name):
    workdir = pathlib.Path().resolve()
    template_folder_path = pathlib.Path(__file__).parent.joinpath('templates/project')
    generated_project_path = pathlib.Path(workdir).joinpath(project_name)
    print(f'Initializing project {project_name}')
    shutil.copytree(template_folder_path, generated_project_path)


def write_render_template(template_path: str, out_path: str) -> str:
    out_file_name = pathlib.Path(out_path).name
    out_path = pathlib.Path(out_path).parent.joinpath(out_file_name.capitalize())
    out_file_name = pathlib.Path(out_path).stem

    print(f'{template_path} {out_path}')
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('mewni'),
        autoescape=jinja2.select_autoescape()
    )
    template = env.get_template(template_path)
    out = template.render({
        'name': out_file_name
    })
    with open(out_path, 'w') as file:
        file.write(out)


class ObjectTypes(enum.Enum):
    MODEL = 'model'
    CONTROLLER = 'controller'
    FILTER = 'filter'
    STORE = 'store'
    TEMPLATE = 'template'


def get_absolute_out_path(relative_out_path: str) -> str:
    """

    :param relative_out_path: path started at bot directory
    :return: {project_dir}/bot/{relative_out_path}
    """
    return str(pathlib.Path(os.getcwd()).joinpath(f'bot/{relative_out_path}').resolve())

def write_render(relative_template_path: str, relative_out_path: str):
    write_render_template(
        relative_template_path,
        get_absolute_out_path(relative_out_path)
    )

#  Using: mewni create <model|controller|filter|store|template> <name>
@cli.command()
@click.argument('object_type')
@click.argument('generated_file')
def create(object_type: str, generated_file):
    object_type: enum.Enum = ObjectTypes(object_type)

    if object_type == ObjectTypes.MODEL:
        write_render('model.txt', f'models/{generated_file}.py')
    elif object_type == ObjectTypes.STORE:
        write_render('store.txt', f'stores/{generated_file}.py')
    elif object_type == ObjectTypes.CONTROLLER:
        write_render('controller.txt', f'controllers/{generated_file}.py')
    elif object_type == ObjectTypes.FILTER:
        write_render('filter.txt', f'filters/{generated_file}.py')




def main():
    cli()
