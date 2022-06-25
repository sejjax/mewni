#  This is Entry point to all framework. In this file going on
from mewni.utils.singleton import singleton
from .register import Register
from .bot import Bot
from aiogram import Dispatcher
from .store import MemoryStorage
from peewee import Database
from .db import connect_db, DBType


@singleton
class Mewni:
    """
    Application entry point.
    """
    bot: Bot
    register: Register
    db: Database
    config: any

    def __init__(self):
        self.register = Register()
        self.config = self.register.register_config('bot/config/env.py')

        self.bot = Bot(self.config.BOT_TOKEN)

        self.register.register_user_stores('bot/stores', MemoryStorage())
        self.register.register_controllers('bot/controllers', self.bot.dp)
        self.register.register_middlewares(self.bot.dp)
        self.bot.startup_callback = self.register.on_startup
        self.db = connect_db(
            DBType(self.config.DB_TYPE),
            self.config.DB_PATH,
            self.config.DB_NAME,
            self.config.DB_USER,
            self.config.DB_PASSWORD,
            self.config.DB_HOST,
            self.config.DB_PORT
        )
        models = self.register.register_models('bot/models', self.db)


    def run(self, skip_updates: bool = False):
        self.bot.startup(skip_updates)


def get_app() -> Mewni:
    """
    Return main instance of application. If it's not there then create and return it
    :return: application instance
    """
    return Mewni()


def get_dp() -> Dispatcher:
    """
    Return aiogram bot dispatcher
    :return: aiogram bot dispatcher
    """
    return get_app().bot.dp


def get_bot() -> Bot:
    """
    Return instance of class Bot
    :return: application config
    """
    return get_app().bot


def get_config():
    """
    Return application config
    :return: application config
    """
    return get_app().config
