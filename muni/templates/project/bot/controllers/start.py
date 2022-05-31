from muni.core.controllers import command
from muni.core.app import get_app
from aiogram.types.message import Message


@command(description='This is description')
async def start(message: Message):
    app = get_app()
    await message.answer('Hello World')
