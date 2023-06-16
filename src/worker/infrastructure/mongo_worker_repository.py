from shared.infrastructure import get_settings
from ..domain import MongoRepository


settings = get_settings()


class MongoWorkerRepository(MongoRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def create_user(self, user: dict) -> bool:
        with self.session_factory() as session:
            db = session.get_db(settings.MONGO_DB_NAME)
            collection = db.users
            result = collection.insert_one(user)
            return result.inserted_id is not None

    def get_user(self, username: str) -> dict:
        with self.session_factory() as session:
            db = session.get_db(settings.MONGO_DB_NAME)
            collection = db.users
            result = collection.find_one(
                {"username": username},
                projection={"_id": False}
            )
            return result if result else {}
