import pathlib
import os
import jinja2
import enum


def generate_artifacts(object_type, generated_file):
    def write_render_template(template_path: str, out_path: str) -> str:
        out_file_name = pathlib.Path(out_path).name
        out_path = pathlib.Path(out_path).parent.joinpath(out_file_name.capitalize())
        out_file_name = pathlib.Path(out_path).stem

        print(f'{template_path} {out_path}')
        env = jinja2.Environment(
            loader=jinja2.PackageLoader('mewni.py'),
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
    object_type: enum.Enum = ObjectTypes(object_type)

    if object_type == ObjectTypes.MODEL:
        write_render('model.txt', f'models/{generated_file}.py')
    elif object_type == ObjectTypes.STORE:
        write_render('store.txt', f'stores/{generated_file}.py')
    elif object_type == ObjectTypes.CONTROLLER:
        write_render('controller.txt', f'controllers/{generated_file}.py')
    elif object_type == ObjectTypes.FILTER:
        write_render('filter.txt', f'filters/{generated_file}.py')

