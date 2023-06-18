from worker.domain import MongoRepository, UserModelIn, UserModel
from shared.domain import Response, SuccessResponse
from shared.infrastructure import ErrorResponse
from shared.utils import Utils
import uuid


class RegisterUserUseCase:
    def __init__(self, mongo_service: MongoRepository):
        self._mongo_service = mongo_service
        self.transaction_id = str(uuid.uuid4())

    def execute(self, user: UserModelIn) -> Response:
        old_user = self._mongo_service.get_user(user.username)
        if old_user is None:
            raise ErrorResponse(
                "Failed to verify an existing user. Try again",
                self.transaction_id,
                500
            )
        if old_user:
            raise ErrorResponse(
                "User already exists. Try with different username",
                self.transaction_id,
                400
            )
        user = UserModel(**user.dict())
        user.password = Utils.hash_password(user.password)
        result = self._mongo_service.create_user(user.dict())
        if result:
            data = {"status": "User registered with success"}
            return SuccessResponse(data, 200, self.transaction_id)
        raise ErrorResponse(
            "User no registered. Try again",
            self.transaction_id,
            500
        )

