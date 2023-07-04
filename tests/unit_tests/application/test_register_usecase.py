from worker.domain import UserModelIn
from worker.application import RegisterUserUseCase
from shared.infrastructure import ErrorResponse
from shared.domain import SuccessResponse
from pytest_mock import MockerFixture
import pytest


class TestRegisterUsecase:
    def init_mocks(self, mocker: MockerFixture, mock_data: dict):
        self.mongo_repository = mocker.Mock()
        self.user = UserModelIn(**mock_data["register_user"])

    def test_register_usecase(self, mocker: MockerFixture, mock_data: dict):
        self.init_mocks(mocker, mock_data)
        self.mongo_repository.get_user.return_value = {}
        register_usecase = RegisterUserUseCase(self.mongo_repository)
        response = register_usecase.execute(self.user)
        
        assert isinstance(response, SuccessResponse)
        assert isinstance(response.data, dict)
        assert response.data["status"] == "User registered with success"
        assert response._status_code == 200

    def test_verify_existing_user(self, mocker: MockerFixture, mock_data: dict):
        self.init_mocks(mocker, mock_data)
        self.mongo_repository.get_user.return_value = None
        register_usecase = RegisterUserUseCase(self.mongo_repository)
        
        with pytest.raises(ErrorResponse) as exc_info:
            register_usecase.execute(self.user)
        
        assert exc_info.value.status_code == 500
        assert exc_info.value.data["user_message"] == "Failed to verify an existing user. Try again"
        assert isinstance(exc_info.value.meta, dict)
        assert exc_info.value.meta["transaction_id"] == register_usecase.transaction_id
        
    def test_user_already_exists(self, mocker: MockerFixture, mock_data: dict):
        self.init_mocks(mocker, mock_data)
        self.mongo_repository.get_user.return_value = True
        register_usecase = RegisterUserUseCase(self.mongo_repository)

        with pytest.raises(ErrorResponse) as exc_info:
            register_usecase.execute(self.user)
        
        assert exc_info.value.status_code == 400
        assert exc_info.value.data["user_message"] == "User already exists. Try with different username"
        assert isinstance(exc_info.value.meta, dict)
        assert exc_info.value.meta["transaction_id"] == register_usecase.transaction_id

    def test_create_user_failed(self, mocker: MockerFixture, mock_data: dict):
        self.init_mocks(mocker, mock_data)
        self.mongo_repository.get_user.return_value = {}
        self.mongo_repository.create_user.return_value = False
        register_usecase = RegisterUserUseCase(self.mongo_repository)

        with pytest.raises(ErrorResponse) as exc_info:
            register_usecase.execute(self.user)

        assert exc_info.value.status_code == 500
        assert exc_info.value.data["user_message"] == "User no registered. Try again"
        assert isinstance(exc_info.value.meta, dict)
        assert exc_info.value.meta["transaction_id"] == register_usecase.transaction_id