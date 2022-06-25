import pathlib
import shutil


def initialize_project(project_name):
    workdir = pathlib.Path().resolve()
    template_folder_path = pathlib.Path(__file__).parent.parent.joinpath('templates/project')
    generated_project_path = pathlib.Path(workdir).joinpath(project_name)
    print(f'Initializing project {project_name}')
    shutil.copytree(template_folder_path, generated_project_path)