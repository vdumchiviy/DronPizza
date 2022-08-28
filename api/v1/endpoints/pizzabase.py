from utils import file_utils
from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter
from schemas.pizzabase import PizzaBase, PizzaTask

router = APIRouter()


@router.get(path="/pizzabases", tags=["PizzaBase"])
def get_pizzabases(
) -> List[PizzaBase]:
    return [PizzaBase]


@router.post(path="/pizzabases", tags="PizzaBase", response_model=PizzaBase)
def create_pizzabases(
) -> PizzaBase:
    pizzabase = PizzaBase()
    return {"message": pizzabase.dict()}


@router.get(path="/pizzabases/{pk}/task/", response_model=Union[PizzaTask, Dict[str, Any]])
def get_new_task(
    pk: int
) -> Union[PizzaTask, Dict[str, Any]]:
    pizza_tasks: Optional[PizzaTask] = file_utils.get_new_task_from_csv()
    try:
        pizza_task = next(pizza_tasks)
    except StopIteration:
        return {"code": 404, "message": "There is no more tasks"}
    return pizza_task
