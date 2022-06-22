from typing import Optional
from dataclasses import dataclass


def cast_dotenv_string_to_list(string: str, list_type: any):
    string = ''.join(filter(lambda char: char != ' ', string))
    items = string.split(',')
    items = list(map(lambda item: list_type(item), items))
    return list(items)


@dataclass
class ClassField:
    name: str
    type: any
    value: Optional[any]


def get_class_fields(_class, only_public=False) -> list[ClassField]:
    class_fields = {}

    # for type annotated fields

    fields_with_value = list(
        filter(lambda k: not ((k.startswith('__') and k.endswith('__')) or k.startswith('_')), _class.__dict__.keys())
    )

    for key in fields_with_value:
        value = getattr(_class, key)
        _type = type(value)
        class_fields[key] = ClassField(key, _type, value)

    for key, _type in _class.__annotations__.items():
        if key not in class_fields:
            class_fields[key] = ClassField(key, _type, None)

    return list(class_fields.values())
