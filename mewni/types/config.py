from enum import Enum


class BotType(Enum):
    USER_BOT = 'USER_BOT'
    TELEGRAM_BOT = 'TELEGRAM_BOT'


class DBType(Enum):
    POSTGRES = 'POSTGRES'
    SQLITE = 'SQLITE'
    MYSQL = 'MYSQL'
