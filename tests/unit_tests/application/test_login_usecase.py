from worker.application import LoginUserUseCase
from shared.infrastructure import ErrorResponse
from shared.domain import SuccessResponse
from worker.domain import UserLoginModel
from shared.utils import Utils
from pytest_mock import MockerFixture
import pytest
import uuid


class TestLoginUsecase:
    def init_mocks(self, mocker: MockerFixture, mock_data: dict):
        self.mongo_repository = mocker.Mock()
        self.user = UserLoginModel(**mock_data["login_user"])
        self.existing_user = {
            "rol": ["read"],
            "email": "test@examples.com",
            "is_active": True
        }
        self.existing_user.update(self.user.dict())

    def test_login_user(self, mocker: MockerFixture, mock_data: dict):
        self.init_mocks(mocker, mock_data)
        self.mongo_repository.get_user.return_value = self.existing_user
        mocker.patch.object(Utils, "verify_password", return_value=True)
        register_usecase = LoginUserUseCase(self.mongo_repository)
        response = register_usecase.execute(self.user)

        assert isinstance(response, SuccessResponse)
        assert isinstance(response.data, dict)
        assert response.data["status"] == "User logged in with success"
        assert response.meta.transaction_id == register_usecase.transaction_id
        assert response._status_code == 200

    def test_verify_existing_user(self, mocker: MockerFixture, mock_data: dict):
        self.init_mocks(mocker, mock_data)
        self.mongo_repository.get_user.return_value = None
        register_usecase = LoginUserUseCase(self.mongo_repository)
        
        with pytest.raises(ErrorResponse) as exc_info:
            register_usecase.execute(self.user)
        
        assert exc_info.value.status_code == 500
        assert exc_info.value.data["user_message"] == "Failed to verify an existing user. Try again"
        assert isinstance(exc_info.value.meta, dict)
        assert exc_info.value.meta["transaction_id"] == register_usecase.transaction_id

    def test_user_not_exists(self, mocker: MockerFixture, mock_data: dict):
        self.init_mocks(mocker, mock_data)
        self.mongo_repository.get_user.return_value = {}
        register_usecase = LoginUserUseCase(self.mongo_repository)
        
        with pytest.raises(ErrorResponse) as exc_info:
            register_usecase.execute(self.user)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.data["user_message"] == "User does not exist. Verify the input data"
        assert isinstance(exc_info.value.meta, dict)
        assert exc_info.value.meta["transaction_id"] == register_usecase.transaction_id

    def test_wrong_password(self, mocker: MockerFixture, mock_data: dict):
        self.init_mocks(mocker, mock_data)
        self.mongo_repository.get_user.return_value = self.existing_user
        mocker.patch.object(Utils, "verify_password", return_value=False)
        register_usecase = LoginUserUseCase(self.mongo_repository)

        with pytest.raises(ErrorResponse) as exc_info:
            register_usecase.execute(self.user)
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.data["user_message"] == "Incorrect password. Try again"
        assert isinstance(exc_info.value.meta, dict)
        assert exc_info.value.meta["transaction_id"] == register_usecase.transaction_id