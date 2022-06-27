from mewni.core import command, send, config, startup, ask
from bot.stores import User

@startup
async def startup():
    for admin in config().ADMINS:
        await send('Hello, bot started', chat=admin)


@command
async def start():
    user = User()
    await send(f'Bot started')
    user.name = (await ask('Enter your name')).text
    user.age = int((await ask('Enter your name')).text)

@command
async def info():
    user = User()
    if user.name is None or user.age is None:
        return await send('Please set your data')
    await send(f'Hello {user.name} with {user.age} years old!')

