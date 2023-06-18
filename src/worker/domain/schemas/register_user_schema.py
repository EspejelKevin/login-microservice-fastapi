from pydantic import BaseModel, Field
from .general_schemas import (
    SuccessDataSchema,
    SuccessMetaSchema,
    ErrorDataSchema,
    ErrorMetaSchema,
    VerifyExistingUserSchema,
    error_general_schema
)


class UserRegisteredSchema(BaseModel):
    """ User Registered Schema """
    data: SuccessDataSchema = Field(
        default=SuccessDataSchema(status="User registered with success"),
        title="SuccessDataSchema"
    )
    meta: SuccessMetaSchema = Field(...)


class UserAlreadyExistsSchema(BaseModel):
    data: ErrorDataSchema = Field(
        default=ErrorDataSchema(user_message="User already exists. Try with different username"),
        title="ErrorDataSchema"
    )
    meta: ErrorMetaSchema = Field(
        default=ErrorMetaSchema(),
        title="ErrorMetaSchema"
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
                "name: must be str in body",
                "name: must not be a numeric field in body",
                "lastname: must be str in body",
                "lastname: must not be a numeric field in body",
                "age: must be int in body",
                "age: must be a valid age (>=18) in body",
                "password: must be at least 8 characters long",
                "password: should contain at least one uppercase character",
                "password: should contain at least one digit",
                "password: should contain at least one special character"
            ]
        ),
        title="ErrorMetaSchema"
    )


class UnregisteredUserSchema(BaseModel):
    data: ErrorDataSchema = Field(
        default=ErrorDataSchema(user_message="User no registered. Try again"),
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
                "UserAlreadyExistsSchema": {"value": UserAlreadyExistsSchema()},
                "InvalidInputDataSchema": {"value": InvalidInputDataSchema()}
            }
        }
    }
}


internal_errors = {
    "description": "Internal Server Error",
    "content": {
        "application/json": {
            "schema": error_general_schema,
            "examples": {
                "VerifyExistingUserSchema": {"value": VerifyExistingUserSchema()},
                "UnregisteredUserSchema": {"value": UnregisteredUserSchema()}
            }
        }
    }
}


register_user_responses = {
    200: {"model": UserRegisteredSchema},
    400: bad_request_errors,
    500: internal_errors
}