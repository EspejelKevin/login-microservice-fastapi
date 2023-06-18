from pydantic import BaseModel, Field, Extra
from typing import List


class SuccessDataSchema(BaseModel):
    """ Success Data Schema """
    status: str = Field(
        default="",
        title="Status", 
        description="Mensaje de éxito"
    )


class SuccessMetaSchema(BaseModel, extra=Extra.allow):
    """ Success Meta Schema """
    transaction_id: str = Field(
        default="8d186e53-9fac-4bbf-b735-a110410cbb69",
        title="Transaction ID",
        description="Identificador único del request"
    )
    timestamp: str = Field(
        default="2023-06-17T09:00:41.738671",
        title="Timestamp",
        description="Fecha y hora del request"
    )


class ErrorDataSchema(BaseModel):
    """ Error Data Schema """
    user_message: str = Field(
        default="",
        title="User Message",
        description="Mensaje de error"
    )


class ErrorMetaSchema(SuccessMetaSchema):
    """ Error Meta Schema """
    details: List[str] = Field(
        default=None,
        title="Details",
        description="Descripción detallada del error"
    )


class VerifyExistingUserSchema(BaseModel):
    data: ErrorDataSchema = Field(
        default=ErrorDataSchema(user_message="Failed to verify an existing user. Try again"),
        title="ErrorDataSchema"
    )
    meta: ErrorMetaSchema = Field(
        default=ErrorMetaSchema(),
        title="ErrorMetaSchema"
    )


error_general_schema = {
    "title": "ErrorGeneralSchema",
    "description": "Error General Schema",
    "type": "object",
    "properties": {
        "data": {
            "title": "ErrorDataSchema",
            "description": "Error Data Schema",
            "type": "object",
            "properties": {
                "user_message": {
                    "title": "User Message",
                    "description": "Mensaje de error",
                    "default": None,
                    "type": "string"
                }
            }
        },
        "meta": {
            "title": "ErrorMetaSchema",
            "description": "Error Meta Schema",
            "type": "object",
            "properties": {
                "transaction_id": {
                    "title": "Transaction ID",
                    "description": "Identificador único del request",
                    "default": "8d186e53-9fac-4bbf-b735-a110410cbb69",
                    "type": "string"
                },
                "timestamp": {
                    "title": "Timestamp",
                    "description": "Fecha y hora del request",
                    "default": "2023-06-17T09:00:41.738671",
                    "type": "string"
                }
            }
        }
    }
}
