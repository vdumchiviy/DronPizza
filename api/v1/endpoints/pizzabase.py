from auth.auth import Auth
from utils import file_utils
from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.pizzabase import PizzaBase, PizzaTask
import httpx
from utils.settings import DRON_URL


router = APIRouter()
security = HTTPBearer()
auth_handler = Auth()


@router.get(path="/pizzabases", tags=["PizzaBase"])
def get_pizzabases(
) -> List[PizzaBase]:
    return [PizzaBase]


@router.post(path="/pizzabases", tags=["PizzaBase"], response_model=PizzaBase)
def create_pizzabases(
) -> PizzaBase:
    pizzabase = PizzaBase()
    return {"message": pizzabase.dict()}


@router.get(
    path="/pizzabases/newtask",
    tags=["PizzaBase"],
    response_model=Union[PizzaTask, Dict[str, Any]])
def get_new_task(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Union[PizzaTask, Dict[str, Any]]:
    token = credentials.credentials
    auth_result = auth_handler.decode_token(token)
    if type(auth_result) is dict:
        return auth_result
    if auth_result is False:
        return {"code": 404, "message": "Invalid token"}

    pizza_tasks: Optional[PizzaTask] = file_utils.get_new_task_from_csv()
    try:
        pizza_task = next(pizza_tasks)
    except StopIteration:
        return {"code": 404, "message": "There is no more tasks"}
    return pizza_task


@router.get(
    path="/pizzabases/drons/coordinates",
    tags=["PizzaBase", "Drons"],
    response_model=Dict[str, Any])
def get_drons_coordinate(
    request: Request
) -> Dict[str, Any]:
    with httpx.Client() as client:
        response = client.get(DRON_URL + "/drons/coordinates")

    print(response)
    return dict()
