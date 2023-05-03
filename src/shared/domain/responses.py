from datetime import datetime
from ..utils import Utils


class MetaDataResponse:
    def __init__(self, transaction_id: str, **kwargs) -> None:
        self.transaction_id = transaction_id
        self.timestamp = datetime.now()
        Utils.add_attributes(self, kwargs)
        Utils.discard_empty_attributes(self)


class Response:
    def __init__(self, data: dict, meta: MetaDataResponse) -> None:
        self.data = data
        self.meta = meta


class SuccessResponse(Response):
    def __init__(self, data: dict, status_code: int, transaction_id: str, **kwargs) -> None:
        self._status_code = status_code
        meta = MetaDataResponse(transaction_id, **kwargs)
        super().__init__(data, meta)


class FailureResponse(Response):
    def __init__(self, data: dict, status_code: int, transaction_id: str, **kwargs) -> None:
        self._status_code = status_code
        meta = MetaDataResponse(transaction_id, **kwargs)
        super().__init__(data, meta)
