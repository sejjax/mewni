import os
from abc import ABCMeta
from typing import get_args

import environs

from .utils.get_class_fields import get_class_fields


class Config:
    __metaclass__ = ABCMeta

    BOT_NAME: str
    BOT_TOKEN: str
    ADMINS: list[int]

    def load_config(self, path_to_dot_env: str):
        env = environs.Env()
        env.read_env(path_to_dot_env)
        class_fields = get_class_fields(type(self))
        for class_field in class_fields:
            value_from_env = os.environ.get(class_field.name)
            attr_value = getattr(env, class_field.type.__name__)(
                class_field.name) if value_from_env is not None and value_from_env != '' else class_field.value
            if class_field.type.__name__ == 'list' and len(get_args(class_field.type)) > 0:
                _type = get_args(class_field.type)[0]
                attr_value = list(map(lambda item: _type(item), attr_value))
            setattr(self, class_field.name, attr_value)
