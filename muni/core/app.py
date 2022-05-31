import os
from pathlib import Path

from aiogram.types import BotCommand
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from .utils.singleton import singleton
from aiogram import Dispatcher, Bot, executor
from .autoloader import AutoLoader
from .utils.muni_meta import get_muni_meta, has_muni_meta
from .types import MuniCallbackMeta
from .config import Config
import asyncio


# Entry point
@singleton
class Muni:
    config: Config
    bot: Bot
    dp: Dispatcher
    autoloader: AutoLoader

    i18n: I18nMiddleware

    def __init__(self, skip_updates=False):
        self.skip_updates = skip_updates
        self.autoloader = AutoLoader()

        self.load_config()

        self.bot = Bot(self.config.BOT_TOKEN)
        self.dp = Dispatcher(self.bot)

        LOCALES_DIR = Path(os.getcwd()).joinpath('bot/locales')
        self.i18n = I18nMiddleware(self.config.BOT_NAME, LOCALES_DIR)
        self.dp.setup_middleware(self.i18n)

        self.register_controllers()

    def run(self):
        executor.start_polling(self.dp, skip_updates=self.skip_updates)

    def load_config(self):
        app_config_module_path = 'bot/config/app.py'
        AppConfig = self.autoloader.load_class(app_config_module_path, 'AppConfig')

        working_dir = os.getcwd()
        relative_file_path = '.env'
        path_to_config_file = Path(working_dir).joinpath(relative_file_path)

        self.config = AppConfig()
        self.config.load_config(str(path_to_config_file))

    def generate_help(self, commands: list[MuniCallbackMeta]) -> help:
        help = ''
        for command in commands:
            meta = get_muni_meta(command)
            help += f'/{meta.value.command} - {meta.value.value}\n'
        return help

    def set_commands(self, commands):
        _commands = [BotCommand(
            get_muni_meta(command).value.command,
            get_muni_meta(command).value.value
        ) for command in commands]
        asyncio.get_event_loop().run_until_complete(self.bot.set_my_commands(_commands))

    def register_controllers(self):
        functions = self.autoloader.load_functions('bot/controllers', recursively=True)
        commands = list(filter(lambda item: has_muni_meta(item), functions))
        for command in commands:
            self.dp.register_message_handler(command, commands=[get_muni_meta(command).value.command])
        self.set_commands(commands)

        async def help(message):
            await self.bot.send_message(message.from_user.id, self.generate_help(commands))

        self.dp.register_message_handler(help, commands=['help'])
        self.set_commands(commands)


def get_app():
    return Muni()
