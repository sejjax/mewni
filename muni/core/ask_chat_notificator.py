from aiogram import types
from aiogram import Dispatcher
import asyncio
from dataclasses import dataclass


@dataclass
class FutureMsg:
    chat_id: int
    future: asyncio.Future


class AskChatNotificator:
    subscribers: list[FutureMsg] = []
    dp: Dispatcher

    def __init__(self, dp: Dispatcher):
        self.dp = dp

    async def handler(self, msg: types.Message):
        subscribers = list(filter(lambda item: item.chat_id == msg.chat.id, self.subscribers))
        if len(subscribers) > 0:
            subscriber: FutureMsg = subscribers[0]
            # Send message to ask_chat to handler
            subscriber.future.set_result(msg)
            self.unsubscribe(subscriber)
        return

    def register_handler(self):
        self.dp.register_message_handler(self.handler, state="*")

    def subscribe(self, chat_id: int, future: asyncio.Future):
        self.subscribers.append(FutureMsg(chat_id, future))

    def unsubscribe(self, subscriber: FutureMsg):
        self.subscribers.remove(subscriber)
