import os
from typing import get_args, TypeVar
import environs

from mewni.utils.get_class_fields import get_class_fields

T = TypeVar('T')


def load_config(class_: T, path_to_dot_env: str, ignore_case: bool = False) -> T:
    env = environs.Env()
    env.read_env(path_to_dot_env)
    class_fields = get_class_fields(class_)
    if ignore_case:
        for class_field in class_fields:
            class_field.name = class_field.name.upper()
    for class_field in class_fields:
        value_from_env = os.environ.get(class_field.name)
        attr_value = getattr(env, class_field.type.__name__)(
            class_field.name) if value_from_env is not None and value_from_env != '' else class_field.value
        if class_field.type.__name__ == 'list' and len(get_args(class_field.type)) > 0:
            _type = get_args(class_field.type)[0]
            attr_value = list(map(lambda item: _type(item), attr_value))
        setattr(class_, class_field.name, attr_value)
    return class_
