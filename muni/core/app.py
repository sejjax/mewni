import os
from pathlib import Path
from .utils.singleton import singleton
from aiogram import Dispatcher, Bot, executor
from .autoloader import AutoLoader


# Entry point
@singleton
class Muni:
    instance = None
    config = None
    bot = None
    dp = None
    autoloader: AutoLoader

    def __init__(self, skip_updates=False):
        self.skip_updates = skip_updates
        self.autoloader = AutoLoader()

        self.load_config()

        self.bot = Bot(self.config.BOT_TOKEN)
        self.dp = Dispatcher(self.bot)

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
        self.config.load_config(path_to_config_file)

    def register_controllers(self):
        functions = self.autoloader.load_functions('bot/controllers', recursively=True)
        print('')

