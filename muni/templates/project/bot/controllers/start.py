from muni.core.controllers import command, every, SECOND
from muni.core.app import get_config
from aiogram.types.message import Message


@command(description='Hello World')
async def start(message: Message):
    config = get_config()
    return await message.answer(f'Hello World {config.BOT_NAME}')


# @every(SECOND)
# async def notify():
#     app = get_app()
#     for admin in app.config.ADMINS:
#         await app.bot.send_message(admin, 'Hello Admin')
