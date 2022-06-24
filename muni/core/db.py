from peewee import Database, SqliteDatabase, MySQLDatabase, PostgresqlDatabase, Model
from typing import Type
from enum import Enum


class DBType(Enum):
    POSTGRES = 'POSTGRES'
    SQLITE = 'SQLITE'
    MYSQL = 'MYSQL'


def connect_db(
        db_type: DBType,
        path: str | None,
        database: str | None,
        user: str | None,
        password: str | None,
        host: str | None,
        port: int | None
) -> Database:
    if db_type == DBType.SQLITE:
        return SqliteDatabase(path)
    elif db_type == DBType.POSTGRES:
        return PostgresqlDatabase(database=database, user=user, password=password, host=host, port=port)
    elif db_type == DBType.MYSQL:
        return MySQLDatabase(database=database, user=user, password=password, host=host, port=port)
    raise TypeError('Unsupported DB type')


def inject_db(db: Database, model: Type[Model]):
    getattr(model, '_meta').database = db
    return model
