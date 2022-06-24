from abc import abstractmethod, ABCMeta


class MewniObject:
    __meta_class_ = ABCMeta

    @abstractmethod
    def on_register(self, *args, **kwargs):
        """Calling when an object will be registered"""
