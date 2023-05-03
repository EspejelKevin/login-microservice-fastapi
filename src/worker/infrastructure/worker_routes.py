from shared.infrastructure import HttpResponse, get_settings
from ..domain import UserModelIn, UserLoginModel
from ..infrastructure import WorkerController
from fastapi import APIRouter


settings = get_settings()
api_version = settings.API_VERSION
namespace = settings.NAMESPACE
path_base = f"/{namespace}/{api_version}"
router = APIRouter(prefix=path_base)


@router.post("/register", tags=["Users"])
def register_user(user: UserModelIn) -> HttpResponse:
    return WorkerController.register_user(user)


@router.post("/login", tags=["Users"])
def login_user(user: UserLoginModel) -> HttpResponse:
    return WorkerController.login_user(user)
