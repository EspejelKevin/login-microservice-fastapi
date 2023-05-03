from ..domain import MongoRepository


class MongoService(MongoRepository):
    def __init__(self, mongo_repository: MongoRepository) -> None:
        self.__mongo_repository = mongo_repository

    def create_user(self, user: dict) -> bool:
        return self.__mongo_repository.create_user(user)

    def get_user(self, username: str) -> dict:
        return self.__mongo_repository.get_user(username)
