import os
from pathlib import Path

import asyncio
from aiogram.types import BotCommand
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import Dispatcher, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .utils.singleton import singleton
from .autoloader import AutoLoader
from .utils.muni_meta import get_muni_meta, has_muni_meta
from .types import MuniCallbackMeta, MuniScheduler, MuniCommand
from .config import Config
from .schedulling import start_scheduling
from .ctx import OpenContextMiddleware, CloseContextMiddleware
from .ask_chat_notificator import AskChatNotificator


def generate_help(commands: list[MuniCallbackMeta]) -> str:
    help_ = '/help - Show helpful information\n'
    for command in reversed(commands):
        meta = get_muni_meta(command)
        help_ += f'/{meta.value.command} - {meta.value.value}\n'

    return help_


@singleton
class Muni:
    config: Config
    bot: Bot
    dp: Dispatcher
    autoloader: AutoLoader

    i18n: I18nMiddleware
    ask_chat_notificator: AskChatNotificator

    def __init__(self, skip_updates=False):
        self.skip_updates = skip_updates
        self.autoloader = AutoLoader()

        self.load_config()

        self.bot = Bot(self.config.BOT_TOKEN)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(self.bot, storage=self.storage)

        self.ask_chat_notificator = AskChatNotificator(self.dp)

        self.dp.setup_middleware(OpenContextMiddleware())

        LOCALES_DIR = Path(os.getcwd()).joinpath('bot/locales')
        self.i18n = I18nMiddleware(self.config.BOT_NAME, LOCALES_DIR)
        self.dp.setup_middleware(self.i18n)

        self.register_controllers()
        self.ask_chat_notificator.register_handler()
        self.dp.setup_middleware(CloseContextMiddleware())

    def run(self):
        async def on_startup(_):
            asyncio.create_task(start_scheduling())

        executor.start_polling(self.dp, skip_updates=self.skip_updates, on_startup=on_startup)

    def load_config(self):
        app_config_module_path = 'bot/config/app.py'
        LoadedAppConfig = self.autoloader.load_class(app_config_module_path, 'AppConfig')

        working_dir = os.getcwd()
        relative_file_path = '.env'
        path_to_config_file = Path(working_dir).joinpath(relative_file_path)

        self.config = LoadedAppConfig()
        self.config.load_config(str(path_to_config_file))

    def set_commands(self, commands):
        _commands = [BotCommand(
            get_muni_meta(command).value.command,
            get_muni_meta(command).value.value
        ) for command in commands]
        asyncio.get_event_loop().run_until_complete(self.bot.set_my_commands(_commands))

    def register_controllers(self):
        functions = self.autoloader.load_functions('bot/controllers', recursive=True)
        commands = list(
            filter(lambda item: has_muni_meta(item) and isinstance(get_muni_meta(item).value, MuniCommand), functions))
        schedulers = list(
            filter(lambda item: has_muni_meta(item) and isinstance(get_muni_meta(item).value, MuniScheduler),
                   functions))

        async def help_command(message):
            await self.bot.send_message(message.from_user.id, generate_help(commands))

        self.dp.register_message_handler(help_command, commands=['help'])
        for command in commands:
            self.dp.register_message_handler(command, commands=[get_muni_meta(command).value.command])
        self.set_commands(commands)

        for schedule in schedulers:
            schedule()


def get_app() -> Muni:
    return Muni()


def get_config() -> Config:
    return get_app().config


def get_dp() -> Dispatcher:
    return get_app().dp


def get_bot() -> Bot:
    return get_app().bot
