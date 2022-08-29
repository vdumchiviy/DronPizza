# from jwt.jwt import JWT
from jwt.api_jwt import PyJWT
from jwt.exceptions import ExpiredSignatureError

from datetime import datetime, timedelta
from passlib.context import CryptContext

string = "12345"
hasher = CryptContext(schemes=["bcrypt"])


class Auth():
    jwt = PyJWT()

    def encode_password(self, password):
        return hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return hasher.verify(password, encoded_password)

    def encode_token(self, user_name):
        args = {
            "scope": "access_token",
            "sub": user_name,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(seconds=60),
        }
        return self.jwt.encode(payload=args, key=string, algorithm="HS256")

    def decode_token(self, token):
        try:
            args = self.jwt.decode(jwt=token, key=string, algorithms=['HS256'])
            if args['scope'] == "access_token":
                return args["sub"]
            else:
                return {"message": "Invalid Scope"}
        except ExpiredSignatureError as ex:
            msg = {"message": "Token expired", "details": str(ex)}
            return msg
        except Exception as ex:
            msg = {"message": "Invalid token", "details": str(ex)}
            return msg

    def encode_refresh_token(self, user_name):
        args = {
            "scope": "refresh_token",
            "sub": user_name,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=24),
        }
        return self.jwt.encode(payload=args, key=string, algorithm="HS256")

    def refresh_access_token(self, refresh_token):
        try:
            args = self.jwt.decode(jwt=refresh_token,
                                   key=string, algorithms=['HS256'])
            if args['scope'] == "refresh_token":
                user_name = args["sub"]
                access_token = self.encode_token(user_name=user_name)
                return access_token
            else:
                return {"message": "Invalid Scope"}
        except Exception as ex:
            msg = {"message": "Invalid token", "details": str(ex)}
            return msg
