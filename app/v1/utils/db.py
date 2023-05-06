from contextvars import ContextVar

import aioredis
import peewee
from fastapi import Depends

from app.v1.utils.settings import Settings

settings = Settings()

DB_NAME = settings.db_name
DB_USER = settings.db_user
DB_PASS = settings.db_pass
DB_HOST = settings.db_host
DB_PORT = settings.db_port

REDIS_HOST = settings.redis_url
REDIS_PORT = settings.redis_port
REDIS_DB = settings.redis_db

db_state_default = {
    "closed": None,
    "conn": None,
    "ctx": None,
    "transactions": None,
}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


db = peewee.PostgresqlDatabase(
    DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
)

db._state = PeeweeConnectionState()


async def reset_db_state():
    db._state._state.set(db_state_default.copy())
    db._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        db.connect()
        yield
    finally:
        if not db.is_closed():
            db.close()


redis_pool = None


async def get_redis_pool():
    global redis_pool
    if not redis_pool:
        redis_pool = await aioredis.from_url(
            f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
        )
    return redis_pool


async def close_redis_pool():
    if redis_pool:
        redis_pool.close()
        await redis_pool.wait_closed()


async def reset_redis_pool():
    global redis_pool
    redis_pool = None
