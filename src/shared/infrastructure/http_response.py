from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from shared.domain import Response


class HttpResponse(JSONResponse):

    def __init__(self, status_code: int, content: Response, excludes: set = {}, *args, **kwargs) -> None:
        content_data = jsonable_encoder(content, exclude=excludes)
        super().__init__(
            content=content_data,
            status_code=status_code,
            *args,
            **kwargs
        )
