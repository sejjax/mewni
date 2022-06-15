from muni.core import command, answer, message, ask
from danil.bot.stores.User import User

@command
async def start():
    User.name = (await ask('Введите ваше имя')).text
    User.age = (await ask('Ввудите ваш возраст')).text
    await info()

@command
async def info():
    await answer(f'Привет {User.name}, которому {User.age} лет\n{" ".join(list(map(lambda t: f"#{t}", User.tags)))}')

@command
async def tag():
    User.tags.append(message().get_args())
