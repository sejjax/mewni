# Mewni is the python telegram bot framework 

## Установка
Поддерживаемая версия - `Python 3.10` и выше

Важно! Если вы на Windows, то запускаете скрипт ниже из консоли запущенной с правами админимтратора, иначе скрипт не добавится в переменную `PATH` и команды `ni` и `mewni` работать не будут.

Напишите `pip install mewni` для установки пакета из [PyPI](https://pypi.org).

Для разработки этого пакета требуется установить [Poetry](https://python-poetry.org/) командой `pip install poetry`. Обязательно посмотрите [документацию](https://python-poetry.org/docs/) этого пакетного менеджера!

Напишите `ni init superbot` для инициализации проекта.

## Проект
### Конфигурация
`bot/config/env.py` Файл для описния переменных среды. 

```python
class EnvConfig:
    BOT_NAME: str
    BOT_TOKEN: str
    ADMINS: list[int]

    APP_HOST: str = 'localhost'
    APP_PORT: int = 8443
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
```
Взгляните на этот кусок кода:
```python
APPHOST: str = 'localhost'
```
`APP_HOST` это поле класса в которое будет подргужено значение из файла `.env` по ключу `APP_HOST`. 

`str` означает, что при подргрузке переменной, ее значение будет приведено к этому типу. 

`'localhost'` - это значение по умолчанию, которое будет использовано в случае отсутствия ключа или его значения в файле `.env`
## Контроллеры 
`bot/controllers` - папака для контроллеров
Все контроллеры подгружаются и регистрируются автоматически при инициализации приложения.

```python
from mewni import command, send
from bot.config import config


@command
async def start():
  await send(f'Application started at {config.APP_HOST}:{config.APP_PORT}')
```
`@command` - это декоратор, который помечает обработчик команд `start()` как команду. Если вы отправите боту `/start`, то он исполнит тело этого обработчика.
По умочанию за имя команду принимается название функции. Вы также можете изменить его изменив значение параметра `name`.
Для добавления описания функции, которое будет отображатся в списке команд Telegram, используйте поле `description`.
```python
@command(name='start', description='Start this bot for you')
def rename_me(): pass
```

`send()` - функция, которая отсылает текст пользователю бота, который вызвал обработку этого коллбека. 
### Получение данных от пользователя 
Для получения данных и текста введеного пользователем, вызовите функцию `message()`
```python
from mewni import command, message

@command
async def start():
    msg = message()
    print(msg)
```
### Запрос данных у пользователя 
`ask()` Отсылает сообщение с просьбой ввести информацию и возвращает обьект сообщения с этой информацией.

```python
from mewni import command, ask, send


@command
async def start():
  name_msg = await ask('Введите ваше имя')
  age_msg = await ask('Теперь введите ваш возраст')

  print(name_msg)
  print(age_msg)

  send(f'Привет {name_msg.text}, которому {age_msg.text} лет')
```
### Другие декораторы для создания контроллеров
`@startup` - Запускает обработчик при запуске приложения 

`@halt` - Запускает обработчик при остановке приложения

`@hear` - Запускает обработчик при получение сообщения с обычным текстом текста


## Хранение данных вне обработчиков
Для сохранения данных введенных пользователем между вызовами разных обработчиков, нужно использовать `UserStore`
```python
# bot/stores/user.py
from mewni import UserStore

class User(UserStore):
    # 'Петр' и 10 - это значение по умолчанию 
    name: str = 'Рома'
    age: int = 16
```
```python
# bot/controllers/start.py
from mewni import ask, command
from bot.stores.User import User

@command
async def start():
    name = await ask('Введите ваше имя')
    age = await ask('Введите ваш возраст')
    user = User()
    user.name = name.text, 
    user.age = int(age.text)

@command
async def info():
    user = User()
    await send(f'Привет {user.name}, которому {user.age} лет')
```
Здесь класс `User` - сохраняет данные не глобально для всех пользователей, а локально именно для этого пользователя в хранилеще по `id` его чата в `Storage`. По умолчанию используется `MemoryStorage`, но потом мы добавим `RedistStorage`, `MongoStorage` и `FileStorage`

`UserStore.clear()` - востанавливает значение хранилища к значениям по умолчанию, если их нет, то удаляет все данные для этого пользователя.
`UserStore.delete()` - полностью удаляет данные этого хранилища для этого пользователя.

## Tasks
- Implement modules autoimport 
- [ ] Implement method `select(message: str, enum: Enum)` which send a message with selection and return option of enum and map selected option to value
- [ ] Implement `LocalStorage()` with the same syntax `name, email, age = LocalStore()` which create storage for each user. For implementation need to use python AST.
- [ ] Make architecture for this project
- [ ] Refactor all project
- [ ] Make documentation better
- [ ] Make errors better
- [ ] Make using Config class from project for type auto complete
- [ ] Add code formatter - black
- [ ] Set name to "bot" folder the same as project
- [ ] Make plugin system
- [ ] Add Template renderer
- [ ] Add `@startup`, `@stop` decorators
- [ ] Add `@hear` decorator
- [ ] Add the ability to work with inline query
- [ ] Add checking for existence value in .env file. If value is not defined then raise error
- [ ] Colorize output
- [ ] Make beautiful serve message
- [ ] Add the ability to adding other threads to app
- [ ] Add `@middleware` decorator
- [ ] Add `@filter` decorator
- [ ] Add questions to init project command
- [ ] Add auto db injection to peewee models
- [ ] Change every event syntax
- [ ] Implement overwrite default `/help` command text and reaction for it
- [ ] Implement `/myuserid` command for improve user experience
- [ ] Implement `setcommand()` function for showing commands at list
- [ ] Schedulling with localization
- [ ] Add logging with structuring for years, month and days
- [ ] Buy website for mewni project
- [ ] Make additional cli commands:
  - [ ] `generate` - generate something project items
  - [ ] `start` - start server
  - [ ] `dev` - start server with auto reloading
  - [ ] `build` - compile all project to one .pyc file
  - [ ] `deploy` - deploy bot to mewni server
  - [ ] `auth` - authorize for mewni server for deploy
- [ ] Implement plugins:
  - [ ] Role plugin
  - [ ] Admin plugin
  - [ ] Analytic plugin
  - [ ] Payment plugin
- [ ] Add notification about startup and stopping for bot admins
- [ ] Detach Mewni from specific service (Telegram) and make it universe:
  - [ ] Telegram
  - [ ] WhatsApp
  - [ ] Discord
  - [ ] Github
  - [ ] Twitter and others social networks
- [ ] Draw logotype for Mewni project
- [ ] Add choosing between requirements.txt and pyproject.toml files (poetry and pip options).