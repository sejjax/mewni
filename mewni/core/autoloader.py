import inspect
from types import ModuleType, FunctionType
from typing import Callable
import glob
import os
from pathlib import Path
import importlib.util
import importlib.machinery
from ..utils.prefix import remove_prefix


def load_module(base_path, module_path):
    # FIXME: fix path converting
    module_path = str(module_path)
    if module_path[0] == '/':
        module_path = module_path[1:]
    python_module_path = module_path.split('.')[0].replace('/', '.')
    package = '.'.join(python_module_path.split('.')[:-1])
    module = importlib.import_module(python_module_path, package)
    return module


class AutoLoader:
    base_path: Path

    def __init__(self, base_path=os.getcwd()):
        self.base_path = Path(base_path)

    def load_modules(self, path, recursive: bool = False) -> ModuleType | list[ModuleType]:
        """
        Load all modules by path. If path end to directory then load and return all modules in this directory.
        If path end to file then load and return only module of this file.

        :param path: path to directory of modules or module
        :param recursive: load modules recursively for directories
        """
        path = Path(path)

        if path.is_absolute():
            result_path = path
        else:
            result_path = self.base_path.joinpath(path)

        #  If path is path to file
        if path.is_file():
            module = load_module(self.base_path, path)
            return module
            #  TODO: Prevent several modules reloadings (probably problem with module names)
            #   By this reason doesn't work Config and UserStore
            #   Sequence of module loading so very important (app.py)

        #  If path is path to directory then load all modules in this directory
        modules = []
        find_path = str(result_path.joinpath('**/*.py'))
        for filename in glob.iglob(find_path, recursive=recursive):
            # FIXME: fix path converting
            module = load_module(self.base_path, Path(remove_prefix(str(self.base_path), filename)))
            modules.append(module)
        return modules

    def _module_object_type_filter(self, filter_: Callable, path: str, recursive: bool = False):
        def object_filter(_filter, module):
            objects_names = dir(module)
            objects_ = list(map(lambda item: getattr(module, item), objects_names))
            filtered_objects = list(filter(lambda item: _filter(item), objects_))
            return filtered_objects

        modules = self.load_modules(path, recursive=recursive)
        objects = []
        if type(modules) == list:
            for modul in modules:
                objects += object_filter(filter_, modul)
            return objects

        objects += object_filter(filter_, modules)
        return objects

    def load_functions(self, path: str, recursive=False):
        """
        Will load and return all functions by path.
        :param path:
        :param recursive:
        :return:
        """
        return self._module_object_type_filter(lambda obj: type(obj) == FunctionType, path, recursive)

    def load_objects(self, path: str, type_: any = None, recursive=False):
        """
        Will load and return all objects
        :param path:
        :param type_:
        :param recursive:
        :return:
        """
        if type_ is None:
            return self._module_object_type_filter(lambda obj: obj, path, recursive)
        return list(set(self._module_object_type_filter(lambda obj: type(obj) == type_, path, recursive)))

    def load_function(self, path: str, function_name, recursive=False):
        """
        Will load and return only one function the name of which set in attributes.
        :param path:
        :param function_name:
        :param recursive:
        :return:
        """
        result = list(
            filter(lambda item: item.__name__ == function_name, self.load_functions(path, recursive=recursive))
        )
        if len(result) == 0:
            raise Exception(f'Can not find name {function_name}')
        return result[0]

    def load_classes(self, path, recursive=False):
        """
        Will load and return all classes by path.
        :param path:
        :param recursive:
        :return:
        """
        return self._module_object_type_filter(lambda obj: inspect.isclass(obj), path, recursive)

    def load_class(self, path, class_name, recursive=False):
        """
        Will load and return only one class the name of which set in attributes.
        :param path:
        :param class_name:
        :param recursive:
        :return:
        """
        result = list(filter(lambda item: item.__name__ == class_name, self.load_classes(path, recursive)))
        if len(result) == 0:
            raise Exception(f'Can not find name {class_name}')
        return result[0]
