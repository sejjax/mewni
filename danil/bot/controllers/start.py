from muni.core import command, every, send_message, answer, config, SECOND, message, ask
from operator import attrgetter

@command
async def start():
    first_name = await ask('Напиши свое имя')
    last_name = await ask('Напиши свою фамилию')
    age = await ask('Напиши свой возраст')
    await answer(f'Привет  {first_name.text} {last_name.text}! Тебе {age.text} лет.')
