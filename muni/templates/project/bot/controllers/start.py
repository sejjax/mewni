from muni.core import command, every, send_message, answer, config


@command
async def start():
    await answer(f'Application started at {config().APP_HOST}:{config().APP_PORT}')


@command
async def click():
    for admin in config().ADMINS:
        await send_message(admin, 'Hello, bot started')