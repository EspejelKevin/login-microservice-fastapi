from abc import ABCMeta, abstractmethod


class MongoRepository(metaclass=ABCMeta):
    @abstractmethod
    def create_user(self, user: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_user(self, username: str) -> dict:
        raise NotImplementedError
