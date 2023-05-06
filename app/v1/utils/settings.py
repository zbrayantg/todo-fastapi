import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    _db_name: str = os.getenv("DB_NAME")
    db_user: str = os.getenv("DB_USER")
    db_pass: str = os.getenv("DB_PASS")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")

    secret_key: str = os.getenv("SECRET_KEY")
    token_expire: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    redis_url: str = os.getenv("REDIS_URL")
    redis_port: str = os.getenv("REDIS_PORT")
    redis_db: str = os.getenv("REDIS_DB")

    @property
    def db_name(self):
        if os.getenv("RUN_ENV") == "test":
            return "test_" + self._db_name

        return self._db_name
