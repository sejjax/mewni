import inspect
from types import ModuleType, FunctionType
from typing import Callable
import glob
import os
from pathlib import Path
from importlib.machinery import SourceFileLoader


class AutoLoader:
    base_path: Path

    def __init__(self, base_path=os.getcwd()):
        self.base_path = Path(base_path)

    def load_modules(self, path, recursive: bool = False) -> ModuleType | list[ModuleType]:
        path = Path(path)

        if path.is_absolute():
            result_path = path
        else:
            result_path = self.base_path.joinpath(path)

        if path.is_file():
            name = Path(path).name.split('.')[0]
            return SourceFileLoader(name, str(result_path)).load_module()

        modules = []
        find_path = str(result_path.joinpath('**/*.py'))
        for filename in glob.iglob(find_path, recursive=recursive):
            name = Path(filename).name.split('.')[0]
            mod = SourceFileLoader(name, str(filename)).load_module()
            modules.append(mod)
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
        return self._module_object_type_filter(lambda obj: type(obj) == FunctionType, path, recursive)

    def load_function(self, path: str, function_name, recursive=False):
        result = list(
            filter(lambda item: item.__name__ == function_name, self.load_functions(path, recursive=recursive))
        )
        if len(result) == 0:
            raise Exception(f'Can not find name {function_name}')
        return result[0]

    def load_classes(self, path, recursive=False):
        return self._module_object_type_filter(lambda obj: inspect.isclass(obj), path, recursive)

    def load_class(self, path, class_name, recursive=False):
        result = list(filter(lambda item: item.__name__ == class_name, self.load_classes(path, recursive)))
        if len(result) == 0:
            raise Exception(f'Can not find name {class_name}')
        return result[0]
