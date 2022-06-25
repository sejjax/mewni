from typing import Type
from .controllers import Controller, Command, OnStartup
from .store import UserStore, Storage
from .loader import Loader
from .ctx import OpenContextMiddleware, CloseContextMiddleware
from .ask_data_middleware import AskDataMiddleware
from .model import inverse_relations
from .db import inject_db
from peewee import Database


class Register:
    """
    Class for registering all needless objects for app.
    """
    user_stores: list[UserStore] = []
    controllers: list[Type[Controller]] = []
    loader: Loader

    ask_data_middleware: AskDataMiddleware

    def __init__(self):
        self.loader = Loader()

    def register_controllers(self, path: str, dispatcher):
        self.controllers = self.loader.load_controllers(path)
        for controller in self.controllers:
            if controller.__class__ == Command:
                controller: Command
                dispatcher.register_message_handler(controller.handler, commands=[controller.name])

    async def on_startup(self):
        for controller in self.controllers:
            if controller.__class__ == OnStartup:
                controller: OnStartup
                await controller.handler()

    def register_middlewares(self, dispatcher):
        self.ask_data_middleware = AskDataMiddleware(dispatcher)
        MIDDLEWARES = [
            OpenContextMiddleware(),
            self.ask_data_middleware,
            CloseContextMiddleware()
        ]
        for middleware in MIDDLEWARES:
            dispatcher.setup_middleware(middleware)

    def register_user_stores(self, path: str, storage: Storage):
        user_stores = self.loader.load_user_stores(path)
        for user_store in user_stores:
            store = user_store()
            # FIXME: fix private variable assignment
            store._storage = storage
            self.user_stores.append(store)

    def register_models(self, path: str, db: Database):
        models = self.loader.load_models(path)
        inverse_relations(models)
        for model in models:
            inject_db(db, model)
        return models

    def register_config(self, path: str):
        return self.loader.load_config(path, 'EnvConfig', '.env')
