from pydantic import BaseModel, Field
from .general_schemas import (
    SuccessDataSchema,
    SuccessMetaSchema,
    ErrorDataSchema,
    ErrorMetaSchema,
    VerifyExistingUserSchema,
    error_general_schema
)
import uuid


class LoginUserSchema(BaseModel):
    """ Login User Schema """
    data: SuccessDataSchema = Field(
        default=SuccessDataSchema(status="User logged in with success"),
        title="SuccessDataSchema"
    )
    meta: SuccessMetaSchema = Field(
        default=SuccessMetaSchema(
            access_token=uuid.uuid4().hex,
            token_type="bearer",
            secret_key=uuid.uuid4().hex
        ),
        title="SuccessMetaSchema"
    )


class InvalidInputDataSchema(BaseModel):
    data: ErrorDataSchema = Field(
        default=ErrorDataSchema(user_message="Parámetros inválidos"),
        title="ErrorDataSchema"
    )
    meta: ErrorMetaSchema = Field(
        default=ErrorMetaSchema(
            details=[
                "username: must be str in body",
                "username: must not be a numeric field in body",
                "password: must be at least 8 characters long",
                "password: should contain at least one uppercase character",
                "password: should contain at least one digit",
                "password: should contain at least one special character"
            ]
        ),
        title="ErrorMetaSchema"
    )


class WrongPasswordSchema(BaseModel):
    data: ErrorDataSchema = Field(
        default=ErrorDataSchema(user_message="Incorrect password. Try again"),
        title="ErrorDataSchema"
    )
    meta: ErrorMetaSchema = Field(
        default=ErrorMetaSchema(),
        title="ErrorMetaSchema"
    )


class UserNotExistsSchema(BaseModel):
    data: ErrorDataSchema = Field(
        default=ErrorDataSchema(user_message="User does not exist. Verify the input data"),
        title="ErrorDataSchema"
    )
    meta: ErrorMetaSchema = Field(
        default=ErrorMetaSchema(),
        title="ErrorMetaSchema"
    )


bad_request_errors = {
    "description": "Bad Request",
    "content": {
        "application/json": {
            "schema": error_general_schema,
            "examples": {
                "WrongPasswordSchema": {"value": WrongPasswordSchema()},
                "InvalidInputDataSchema": {"value": InvalidInputDataSchema()}
            }
        }
    }
}


login_user_responses = {
    200: {"model": LoginUserSchema},
    400: bad_request_errors,
    404: {"model": UserNotExistsSchema},
    500: {"model": VerifyExistingUserSchema}
}