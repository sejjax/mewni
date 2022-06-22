import asyncio

from aiogram import Dispatcher
from typing import Type
from .controllers import Controller, Command, OnStartup
from .store import UserStore, Storage
from .config import load_config
from .loader import Loader
from aiogram.dispatcher.middlewares import BaseMiddleware
from .ctx import OpenContextMiddleware, CloseContextMiddleware
from .ask_data_middleware import AskDataMiddleware


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

    def register_controllers(self, dispatcher):
        self.controllers = self.loader.load_controllers('bot/controllers')
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

    def register_user_stores(self, storage: Storage):
        user_stores = self.loader.load_user_stores('bot/stores')
        for user_store in user_stores:
            store = user_store()
            # FIXME: fix private variable assignment
            store._storage = storage
            self.user_stores.append(store)

    def register_config(self):
        return self.loader.load_config('bot/config/env.py', 'EnvConfig', '.env')