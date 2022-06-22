from aiogram import Dispatcher, Bot as AiogramBot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from types import CoroutineType


class Bot:
    dp: Dispatcher
    bot: AiogramBot
    startup_callback: CoroutineType

    def __init__(self, bot_token: str):
        STORAGE = MemoryStorage()
        self.bot = AiogramBot(bot_token)
        self.dp = Dispatcher(self.bot, STORAGE)

    def startup(self, skip_updates):
        #  FIXME: fix problem with typing
        async def on_startup(_):
            await self.startup_callback()
        executor.start_polling(self.dp, skip_updates=skip_updates, on_startup=on_startup)
