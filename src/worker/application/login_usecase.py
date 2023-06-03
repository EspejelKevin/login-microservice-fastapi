from ..domain import UserLoginModel, MongoRepository, SecuritySchema, UserToEncode
from shared.domain import SuccessResponse
from shared.infrastructure import ErrorResponse
from shared.utils import Utils
import uuid


class LoginUserUseCase:
    def __init__(self, mongo_service: MongoRepository):
        self._mongo_service = mongo_service
        self.transaction_id = str(uuid.uuid4())
        self.security_schema = SecuritySchema()

    def execute(self, user: UserLoginModel):
        existing_user = self._mongo_service.get_user(user.username)
        if not existing_user:
            raise ErrorResponse(
                "User does not exist. Verify the input data.",
                self.transaction_id,
                404
            )
        if not Utils.verify_password(user.password, existing_user.get("password", "")):
            raise ErrorResponse(
                "Incorrect password. Try again.",
                self.transaction_id,
                400
            )
        user_to_encode = UserToEncode(**existing_user)
        access_token = self.security_schema.create_access_token(user_to_encode.dict())
        data = {"status": "User logged in with success"}
        meta = {
            "access_token": access_token,
            "token_type": "bearer",
            "secret_key": self.security_schema.secret_key
        }
        return SuccessResponse(data, 200, self.transaction_id, **meta)
