from aiogram import types
from aiogram import Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
import asyncio

class AskDataMiddleware(BaseMiddleware):
    futures: dict = {}
    dp: Dispatcher

    def __init__(self, dp: Dispatcher):
        super(AskDataMiddleware, self).__init__()
        self.dp = dp

    async def on_pre_process_message(self, msg: types.Message, data: dict):
        chat_id = msg.chat.id
        if chat_id in self.futures:
            future = self.futures[chat_id]
            # Send message to ask_chat to handler1
            future.set_result(msg)
            self.unsubscribe(chat_id)

    def subscribe(self, chat_id: int, future: asyncio.Future):
        self.futures[chat_id] = future

    def unsubscribe(self, chat_id: int):
        del self.futures[chat_id]
