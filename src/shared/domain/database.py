from contextlib import AbstractContextManager, contextmanager
from typing import Any, Callable
import abc


class Session:
    pass


class Database:
    @abc.abstractmethod
    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Any]]:
        pass
