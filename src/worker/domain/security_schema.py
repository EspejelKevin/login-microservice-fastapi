from jose import jwt
import datetime
import secrets


class SecuritySchema:
    def __init__(self):
        self.secret_key = secrets.token_hex()
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    def create_access_token(self, data: dict):
        access_token_expires = datetime.timedelta(minutes=self.access_token_expire_minutes)
        expire = datetime.datetime.utcnow() + access_token_expires
        to_encode = {
            "sub": data,
            "exp": expire
        }
        return jwt.encode(to_encode, self.secret_key, self.algorithm)
