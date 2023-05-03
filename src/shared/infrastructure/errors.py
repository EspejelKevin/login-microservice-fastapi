from fastapi.exceptions import RequestValidationError
from .http_response import HttpResponse
from ..domain import FailureResponse
from ..utils import Utils
import uuid


class ErrorResponse(Exception):
    def __init__(self, message: str, transaction_id: str, status_code: int = 500, **kwargs) -> None:
        self.status_code = status_code
        self.data = {
            "user_message": message
        }
        self.meta = {
            "transaction_id": transaction_id,
            **kwargs
        }


def error_exception_handler(_, e: ErrorResponse) -> HttpResponse:
    content = FailureResponse(e.data, e.status_code, **e.meta)
    return HttpResponse(content=content, status_code=e.status_code, excludes={"_status_code"})


def parameter_exception_handler(_, ex: RequestValidationError) -> HttpResponse:
    details = Utils.get_error_details(ex.errors())
    data = {"user_message": "Parámetros inválidos"}
    meta = {
        "transaction_id": uuid.uuid4(),
        "details": details
    }
    content = FailureResponse(data, 400, **meta)
    return HttpResponse(content=content, status_code=400, excludes={"_status_code"})
