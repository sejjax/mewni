from peewee import CharField, IntegrityError, Field, IntegerField, PrimaryKeyField, ForeignKeyField
from ..utils.get_class_fields import get_class_fields
from enum import Enum
from typing import Type


class Model:
    pass

class EnumField(CharField):
    def __init__(self, enumeration: Type[Enum], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enumeration = enumeration

    def db_value(self, value: Enum) -> str:
        if not isinstance(value, self.enumeration):
            raise TypeError(f"Enum {self.enumeration.__name__} has no value '{value}'")
        return super().db_value(value.name)

    def python_value(self, value: str) -> Enum:
        try:
            return self.enumeration[super().python_value(value)]
        except KeyError:
            raise IntegrityError(
                f"Enum {self.enumeration.__name__} has no value with name '{value}'"
            ) from None


class RelationField(IntegerField):
    model_to: Type[Field]
    args: tuple
    kwargs: dict

    def __init__(self, model_to: Type[Field] | list[Type[Field]], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_to = model_to
        self.args = args
        self.kwargs = kwargs

    def db_value(self, value):
        pass

    def python_value(self, value):
        pass


def inverse_relations(models: list[Type[Field]]):
    for model in models:
        fields = get_class_fields(model)
        for field in fields:
            if hasattr(field.value, '__class__') and isinstance(field.value, RelationField):
                field_value: RelationField = field.value
                model_to = field_value.model_to

                setattr(model_to, model.__name__.lower(), ForeignKeyField(model, backref=getattr(model_to, '_meta').db_table, *field_value.args, **field_value.kwargs))
                delattr(model, field.name)

