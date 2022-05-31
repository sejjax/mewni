import os
from pathlib import Path
from importlib.machinery import SourceFileLoader
import types
import inspect
import glob
from typing import Union


class AutoLoader:
    base_path: Path

    def __init__(self, base_path=os.getcwd()):
        self.base_path = Path(base_path)

    def load_modules(self, path, recursively=False) -> Union[types.ModuleType, list[types.ModuleType]]:
        path = Path(path)

        if path.is_absolute():
            result_path = path
        else:
            result_path = self.base_path.joinpath(path)

        if path.is_file():
            name = Path(path).name.split('.')[0]
            return SourceFileLoader(name, str(result_path)).load_module()

        modules = []
        for filename in glob.iglob(str(result_path) + '**/**', recursive=recursively):
            if Path(filename).suffix == '.py':
                name = Path(filename).name.split('.')[0]
                mod = SourceFileLoader(name, str(filename)).load_module()
                modules.append(mod)
        return modules

    def _module_object_type_filter(self, _filter, path):
        def object_filter(_filter, module):
            objects_names = dir(module)
            objects = list(map(lambda item: getattr(module, item), objects_names))
            filtered_objects = list(filter(lambda item: _filter(item), objects))
            return filtered_objects

        modules = self.load_modules(path)
        objects = []
        if type(modules) == list:
            for modul in modules:
                objects += object_filter(_filter, modul)
            return objects

        objects += object_filter(_filter, modules)
        return objects

    def load_functions(self, path):
        return self._module_object_type_filter(lambda obj: type(obj) == types.FunctionType, path)

    def load_classes(self, path):
        return self._module_object_type_filter(lambda obj: inspect.isclass(obj), path)

    def load_function(self, path, function_name):
        result = list(filter(lambda item: item.__name__ == function_name, self.load_functions(path)))
        if len(result) == 0:
            raise Exception(f'Can not find name {function_name}')
        return result[0]

    def load_class(self, path, class_name):
        result = list(filter(lambda item: item.__name__ == class_name, self.load_classes(path)))
        if len(result) == 0:
            raise Exception(f'Can not find name {class_name}')
        return result[0]
