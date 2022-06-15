from typing import Optional
from dataclasses import dataclass


def cast_dotenv_string_to_list(string: str, list_type: any):
    string = ''.join(filter(lambda char: char is not ' ', string))
    items = string.split(',')
    items = list(map(lambda item: list_type(item), items))
    return list(items)


@dataclass
class ClassField:
    name: str
    type: any
    value: Optional[any]


def get_class_fields(_class) -> list[ClassField]:
    class_fields: list[ClassField] = []

    # for type annotated fields
    for key, _type in _class.__annotations__.items():
        class_fields.append(ClassField(key, _type, None))

    fields_with_value = list(
        filter(lambda k: not (k.startswith('__') and k.endswith('__')), _class.__dict__.keys())
    )

    for key in fields_with_value:
        value = getattr(_class, key)
        _type = type(value)
        class_fields.append(ClassField(key, _type, value))
    return class_fields
