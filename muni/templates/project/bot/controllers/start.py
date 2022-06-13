from muni.core.controllers import command, every, SECOND
from muni.core.app import get_app
from aiogram.types.message import Message


@command(description='This is description')
async def start(message: Message):
    app = get_app()
    await message.answer(f'Hello World {app.config.BOT_NAME}')


@every(SECOND)
async def notify():
    app = get_app()
    for admin in app.config.ADMINS:
        await app.bot.send_message(admin, 'Hello Admin')
