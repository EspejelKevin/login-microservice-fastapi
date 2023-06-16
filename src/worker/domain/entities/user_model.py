from pydantic import BaseModel, validator
from pydantic import EmailStr
from typing import Optional


special_characters = "~!@#$%^&*_-+=`|\(){}[]:;'<>,.?/"


class UserModelIn(BaseModel):
    username: str
    email: EmailStr
    name: str
    lastname: str
    age: int
    password: str

    @validator("username", "name", "lastname", pre=True)
    def username_must_be_str(cls, v):
        if isinstance(v, int):
            raise ValueError("must be str")
        if v.isnumeric():
            raise ValueError("must not be a numeric field")
        return v

    @validator("age", pre=True)
    def age_must_be_correct(cls, v):
        if isinstance(v, str):
            raise ValueError("must be int")
        if v < 18 or v > 100:
            raise ValueError("must be a valid age (>=18)")
        return v

    @validator("password", pre=True, always=True)
    def valid_password(cls, v):
        if len(v) < 8:
            raise ValueError("must be at least 8 characters long")
        if not any(character.isupper() for character in v):
            raise ValueError("should contain at least one uppercase character")
        if not any(character.isdigit() for character in v):
            raise ValueError("should contain at least one digit")
        if all(character not in special_characters for character in v):
            raise ValueError("should contain at least one special character")
        return v


class UserModel(UserModelIn):
    rol: Optional[list] = ["read"]
    is_active: bool = True


class UserLoginModel(BaseModel):
    username: str
    password: str

    @validator("username", pre=True)
    def username_must_be_str(cls, v):
        if isinstance(v, int):
            raise ValueError("must be str")
        if v.isnumeric():
            raise ValueError("must not be a numeric field")
        return v

    @validator("password", pre=True, always=True)
    def valid_password(cls, v):
        if len(v) < 8:
            raise ValueError("must be at least 8 characters long")
        if not any(character.isupper() for character in v):
            raise ValueError("should contain at least one uppercase character")
        if not any(character.isdigit() for character in v):
            raise ValueError("should contain at least one digit")
        if all(character not in special_characters for character in v):
            raise ValueError("should contain at least one special character")
        return v
    

class UserToEncode(BaseModel):
    rol: list
    email: str
    is_active: bool
    username: str