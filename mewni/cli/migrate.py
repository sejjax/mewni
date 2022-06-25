from ..core.register import Register
from ..core.db import connect_db, DBType
import pathlib
import os


def migrate_db():
    register = Register()
    workdir = os.getcwd()
    config = register.register_config(str(pathlib.Path(workdir).joinpath('bot/config/env.py')))
    db = connect_db(
        DBType(config.DB_TYPE),
        config.DB_PATH,
        config.DB_NAME,
        config.DB_USER,
        config.DB_PASSWORD,
        config.DB_HOST,
        config.DB_PORT
    )
    models = register.register_models(str(pathlib.Path(workdir).joinpath('bot/models')), db)
    db.create_tables(models)