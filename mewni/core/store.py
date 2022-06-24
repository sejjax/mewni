import abc
from abc import ABCMeta
from .ctx import message
from mewni.utils.get_class_fields import get_class_fields, ClassField

class Storage:
    """
    Abstract object storage for storing data
    """
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def __setitem__(self, key, value):
        pass

    @abc.abstractmethod
    def __getitem__(self, item):
        pass

    @abc.abstractmethod
    def __delitem__(self, item):
        pass


class MemoryStorage(Storage):
    """
    Specific implementation of Storage. Store all data in memory.
    """
    storage = {}
    current = 0

    def __setitem__(self, key, value):
        self.storage[key] = value

    def __getitem__(self, item):
        return self.storage[item]

    def __delitem__(self, item):
        del self.storage[item]

    def __iter__(self):
        return self

    def __next__(self):
        if self.current + 1 > len(self.storage):
            self.current = 0
            raise StopIteration
        key = list(self.storage)[self.current]
        val = self.storage[key]
        self.current += 1
        return val


class UserStore:
    """
    Class for creating Stores for temporary storing local user data outside of request handlers.
    """
    #  TODO; Solve problem with setters, getters and deleters for attributes of UserStore child classes.
    #   Probably I need to patch AST ("class.attr = val" replace to "class.set('attr', val)")
    _initialized = False
    _first_getting_attr: bool = True
    _storage: Storage
    _fields: list[ClassField] = []
    _instance = None

    def __init__(self):
        if self._initialized:
            return
        self._fields = get_class_fields(self)
        for field in self._fields:
            setattr(self, field.name, None)
        self._initialized = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(UserStore, cls).__new__(cls)
        return cls._instance

    def __setattr__(self, key, value):
        if not self._initialized or key.startswith('_'):
            self.__dict__[key] = value
            return
        # if user data object doesn't exist in storage then create and initialize it
        chat_id = message().chat.id
        if chat_id not in self._storage:
            self._storage[chat_id] = {}
            self._reset()
        self._storage[chat_id][key] = value
        self.__dict__[key] = value

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
        if item in self._storage[chat_id]:
            del self._storage[chat_id][item]
            delattr(self, item)

    def clear(self):
        """Delete all data from storage for this object"""
        chat_id = message().chat.id
        for field in self._fields:
            del self._storage[chat_id][field.name]

    def _reset(self):
        """
        Reset all data from storage for this object to default state and values
        :return:
        """
        for field in self._fields:
            if field.value is not None:
                setattr(self, field.name, field.value)
            else:
                delattr(self, field.name)

    def delete(self):
        """
        Delete user data object from store
        :return:
        """
        chat_id = message().chat.id
        del self._storage[chat_id]