from utils import file_utils
from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter, Request
from schemas.pizzabase import PizzaBase, PizzaTask
import httpx
from utils.settings import DRON_URL


router = APIRouter()


@router.get(path="/pizzabases", tags=["PizzaBase"])
def get_pizzabases(
) -> List[PizzaBase]:
    return [PizzaBase]


@router.post(path="/pizzabases", tags=["PizzaBase"], response_model=PizzaBase)
def create_pizzabases(
) -> PizzaBase:
    pizzabase = PizzaBase()
    return {"message": pizzabase.dict()}


@router.get(path="/pizzabases/{pk}/task/", tags=["PizzaBase"], response_model=Union[PizzaTask, Dict[str, Any]])
def get_new_task(
    pk: int
) -> Union[PizzaTask, Dict[str, Any]]:
    pizza_tasks: Optional[PizzaTask] = file_utils.get_new_task_from_csv()
    try:
        pizza_task = next(pizza_tasks)
    except StopIteration:
        return {"code": 404, "message": "There is no more tasks"}
    return pizza_task


@router.get(
    path="/pizzabases/drons/coordinates/",
    tags=["PizzaBase", "Drons"],
    response_model=Dict[str, Any])
def get_drons_coordinate(
    request: Request
) -> Dict[str, Any]:
    with httpx.Client() as client:
        response = client.get(DRON_URL + "/drons/coordinates/")

    print(response)
    return dict()
