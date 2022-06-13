from muni.core.controllers import command, every, SECOND
from muni.core.app import get_app, get_config
from aiogram.types.message import Message

turn = False

@command
async def start(message: Message):
    config = get_config()
    await message.answer(f'Hello World {config.BOT_NAME}')


@command
async def click(message: Message):
    await message.answer('Click on me')