# Importing os module to interact with the operating system
import os

# Importing load_dotenv function from python-dotenv module
from dotenv import load_dotenv

# Importing BaseSettings class from pydantic module
from pydantic import BaseSettings

# Loading environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    # Defining class attributes to store the configuration settings
    _db_name: str = os.getenv("DB_NAME")
    db_user: str = os.getenv("DB_USER")
    db_pass: str = os.getenv("DB_PASS")
    db_host: str = os.getenv("DB_HOST")
    db_port: str = os.getenv("DB_PORT")

    # Secret key used for encryption and decryption of data
    secret_key: str = os.getenv("SECRET_KEY")
    # Number of minutes after which an access token should expire
    token_expire: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    redis_url: str = os.getenv("REDIS_URL")
    redis_port: str = os.getenv("REDIS_PORT")
    redis_db: str = os.getenv("REDIS_DB")

    @property
    def db_name(self):
        """Getter method to return the database name with a prefix of 'test_'
        if the environment variable RUN_ENV is set to 'test'."""
        if os.getenv("RUN_ENV") == "test":
            return "test_" + self._db_name

        return self._db_name
