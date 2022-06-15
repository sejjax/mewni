import abc
from abc import ABCMeta
from .ctx import message
from .utils.get_class_fields import get_class_fields, ClassField


class Storage:
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def __setattr__(self, key, value):
        pass

    @abc.abstractmethod
    def __getattr__(self, item):
        pass

    @abc.abstractmethod
    def __delattr__(self, item):
        pass


class MemoryStorage(Storage):
    storage = {}

    def __setattr__(self, key, value):
        self.storage[key] = value

    def __getattr__(self, item):
        return self.storage[item]

    def __delattr__(self, item):
        del self.storage[item]


class UserStore:
    _initialized = False
    _first_getting_attr: bool = True
    _storage: Storage
    _fields: list[ClassField]

    def __init__(self):
        self._fields = get_class_fields(self)
        for field in self._fields:
            setattr(self, field.name, None)
        self._initialized = True

    def __setattr__(self, key, value):
        if not self._initialized or key.startswith('_'):
            self.__dict__[key] = value
            return
        chat_id = message().chat.id
        # if user data object doesn't exist in storage then create and initialize it
        if chat_id not in self._storage:
            self._storage[chat_id] = {}
            self.reset()
        self._storage[chat_id][key] = value

    def __getattr__(self, item):
        if item.startswith('_'):
            return self.__dict__[item]
        if self._first_getting_attr:
            self._reset()
            self._first_getting_attr = False
        chat_id = message().chat.id
        return self._storage[chat_id][item]

    def __delattr__(self, item):
        if item.startswith('_'):
            del self.__dict__[item]
            return
        chat_id = message().chat.id
        del self._storage[chat_id][item]

    def clear(self):
        """Delete all data from storage for this object"""
        chat_id = message().chat.id
        for field in self._fields:
            del self._storage[chat_id][field.name]

    def _reset(self):
        """Reset all data from storage for this object to default state and values"""
        for field in self._fields:
            if field.value is not None:
                setattr(self, field.name, field.value)
            else:
                delattr(self, field.name)

    def delete(self):
        """Delete user data object from store"""
        chat_id = message().chat.id
        del self._storage[chat_id]