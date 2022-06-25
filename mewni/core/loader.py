from typing import Type
import os
from pathlib import Path
from .controller import Controller
from .store import UserStore
from .autoloader import AutoLoader
from inspect import isclass
from .config import load_config
from .model import Model


class Loader:
    autoloader: AutoLoader

    def __init__(self):
        self.autoloader = AutoLoader()

    def load_controllers(self, path: str) -> list[Type[Controller]]:
        _objects = self.autoloader.load_objects(path, recursive=True)
        return list(filter(lambda obj: issubclass(obj.__class__, Controller), _objects))

    def load_middlewares(self):
        pass

    def load_user_stores(self, path: str) -> list[Type[UserStore]]:
        _objects = self.autoloader.load_objects(path, recursive=True)
        return list(filter(lambda obj: isclass(obj) and issubclass(obj, UserStore) and obj != UserStore, _objects))

    def load_models(self, path: str):
        _objects = self.autoloader.load_objects(path, recursive=True)
        return list(filter(lambda obj: isclass(obj) and issubclass(obj, Model) and obj != Model, _objects))

    def load_config(self, path: str, config_class_name: str, dot_env_file_name: str = '.env'):
        EnvConfig = self.autoloader.load_class(path, config_class_name)
        working_dir = os.getcwd()
        path_to_config_file = Path(working_dir).joinpath(dot_env_file_name)
        print(path_to_config_file)
        config = load_config(EnvConfig, str(path_to_config_file))
        return config


