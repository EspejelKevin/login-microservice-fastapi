from contextlib import contextmanager, suppress
from ..domain import Database, Session
from collections.abc import Iterator
from .settings import get_settings
from pymongo import MongoClient

settings = get_settings()


class MongoSession(Session):
    def __init__(self, db_uri: str, max_pool_size: int, timeout: int) -> None:
        self.__client = MongoClient(db_uri, maxPoolSize=max_pool_size,
                                    serverSelectionTimeoutMS=timeout)

    def __enter__(self):
        return self

    def get_db(self, db_name) -> MongoClient:
        return self.__client[db_name]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__client.close()


class MongoDatabase(Database):
    def __init__(self, db_uri: str, max_pool_size: int, timeout: int) -> None:
        self.__session = MongoSession(db_uri, max_pool_size, timeout)

    @contextmanager
    def session(self) -> Iterator[Session]:
        with suppress(Exception):
            yield self.__session
