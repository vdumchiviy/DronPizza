from typing import Any, Dict, List, Union
from fastapi import APIRouter, Body, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.auth import UserDron
from utils import settings
from auth.auth import Auth

auth_handler = Auth()
router = APIRouter()
security = HTTPBearer()


@router.post("/userdrons/signin")
def create_userdrons(
    data=Body(...)
) -> Union[UserDron, Dict[str, Any]]:
    login = data.get("login")
    password = data.get("password")
    if login in [x.name for x in settings.auth_base]:
        return {"code": 400, "message": "Cannot create dublicate dron user"}
    try:
        hashed_password = auth_handler.encode_password(password)
        new_dron: UserDron = UserDron(
            pk=0, name=login, hashed_password=hashed_password)
        settings.auth_base.append(new_dron)
        return new_dron
    except Exception as ex:
        return {"code": 400, "message": str(ex)}


@router.post("/userdrons/login")
def login_userdrons(
    data=Body(...)
) -> Dict[str, Any]:
    login = data.get("login")
    password = data.get("password")
    users: List[UserDron] = list(
        filter(lambda x: x.name == login, settings.auth_base))
    if len(users) == 0:
        return {"code": 400, "message": f"Cannot find dron user with name={login}"}
    user: UserDron = users[0]
    if not auth_handler.verify_password(password, user.hashed_password):
        return {"code": 400, "message": f"Invalid password"}

    access_token = auth_handler.encode_token(user_name=login)
    refresh_token = auth_handler.encode_refresh_token(user_name=login)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/userdrons/refresh_token")
def refresh_userdons_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    refresh_token = credentials.credentials
    new_access_token = auth_handler.refresh_access_token(refresh_token)
    return {'access_token': new_access_token}
