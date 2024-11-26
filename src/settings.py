from aiogram import Bot, Dispatcher
from pydantic import AnyUrl, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

__all__ = [
        "settings",
        "engine",
        "sessionmaker",
        "bot",
        "dispatcher",
        ]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False, env_file=".env")

    POSTGRES_URL: PostgresDsn
    
    TELEGRAM_SECRET_TOKEN: SecretStr
    TELEGRAM_BOT_TOKEN: SecretStr

    DOMAIN: AnyUrl


settings = Settings()
engine = create_async_engine(url=settings.POSTGRES_URL.unicode_string())
sessionmaker = async_sessionmaker(bind=engine)
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN.get_secret_value()),
dispatcher = Dispatcher()

