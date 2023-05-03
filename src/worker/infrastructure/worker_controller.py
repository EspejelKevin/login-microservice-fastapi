from ..domain import UserModelIn, UserLoginModel
from shared.infrastructure import HttpResponse
from shared.domain import Response
import container


class WorkerResponse(HttpResponse):
    def __init__(self, content: Response) -> None:
        super().__init__(
            content=content,
            status_code=content._status_code,
            excludes={"_status_code"}
        )


class WorkerController:
    @staticmethod
    def register_user(user: UserModelIn):
        with container.SingletonContainer.scope() as app:
            usecase = app.usecases.register_user()
            response = usecase.execute(user)
            return WorkerResponse(content=response)

    @staticmethod
    def login_user(user: UserLoginModel):
        with container.SingletonContainer.scope() as app:
            usecase = app.usecases.login_user()
            response = usecase.execute(user)
            return WorkerResponse(content=response)
