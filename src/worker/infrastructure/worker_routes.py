from shared.infrastructure import HttpResponse, get_settings
from worker.domain import (
    UserModelIn, 
    UserLoginModel, 
    register_user_responses, 
    login_user_responses
)
from worker.infrastructure import WorkerController
from fastapi import APIRouter


settings = get_settings()
api_version = settings.API_VERSION
namespace = settings.NAMESPACE
path_base = f"/{namespace}/{api_version}"
router = APIRouter(prefix=path_base)


@router.post("/register", tags=["Users"], responses=register_user_responses)
def register_user(user: UserModelIn) -> HttpResponse:
    return WorkerController.register_user(user)


@router.post("/login", tags=["Users"], responses=login_user_responses)
def login_user(user: UserLoginModel) -> HttpResponse:
    return WorkerController.login_user(user)
