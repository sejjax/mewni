from muni.core.config import Config


# EnvironmentConfig - config used .env file
class AppConfig(Config):
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
