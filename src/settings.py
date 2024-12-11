from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisEventIsolation, RedisStorage
from pydantic import AnyUrl, PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

__all__ = [
    "settings", 
    "sessionmaker", 
    "engine", 
    "bot", 
    "dp",
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False, 
        env_file=".env"
    )

    POSTGRES_URL: PostgresDsn
    
    TELEGRAM_SECRET_TOKEN: SecretStr
    TELEGRAM_BOT_TOKEN: SecretStr

    DOMAIN: AnyUrl

    FSM_STORAGE_URL: RedisDsn


settings = Settings()
engine = create_async_engine(
    url=settings.POSTGRES_URL.unicode_string()
)
sessionmaker = async_sessionmaker(
    bind=engine
)
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN.get_secret_value(),
)
fsm_storage = RedisStorage.from_url(
    url=settings.FSM_STORAGE_URL.unicode_string()
)
events_isolation = RedisEventIsolation(
    redis=fsm_storage.redis
)
dp = Dispatcher(
    storage=fsm_storage, 
    events_isolation=events_isolation
)

