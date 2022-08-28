from typing import Any, Dict, List, Optional, Tuple, Union
from fastapi import APIRouter
from schemas.dron import Dron, DronOut
from schemas.pizzabase import PizzaTask
from utils import settings
import httpx

router = APIRouter()


def define_next_coordinate(dron: Dron, task: PizzaTask):
    # assume that distance to next point the same as
    # a distance to base from next point
    if dron.fuel < task.fuel_destination * 2:
        dron.next_coordinates = (0, 0)
    else:
        dron.next_coordinates = (-1, -1)
        dron.distance_to_base = task.fuel_destination


@router.get(path="/drons", tags=["dron"])
def get_drons(
) -> Union[List[Dron], Dict[str, Any]]:
    if settings.dron is not None:
        return [settings.dron]
    else:
        return {"code": 404, "message": "Drons not found"}


@router.post(path="/drons", tags=["dron"], response_model=DronOut)
def create_dron(
    name: str = "0",
    fuel: int = 20
) -> DronOut:
    settings.dron = Dron(name=name, fuel=fuel)
    print(settings.dron)

    result = DronOut(**settings.dron.dict())
    print(result)
    return result


@router.get(path="/drons/{name}}", tags=["dron"])
def get_drone(
    name: str
) -> Union[Dron, Dict[str, Any]]:
    if settings.dron is not None and settings.dron.name == name:
        return settings.dron
    else:
        return {"code": 404, "message": f"Dron with name {name} not found"}


@router.get(path="/drons/coordinates/", tags=["dron"])
def get_drone_coordinates() -> Union[Tuple[int, int], Dict[str, Any]]:
    if settings.dron is None:
        return {"code": 404, "message": f"Dron not found"}

    return settings.dron.coordinates


@router.get(path="/drons/pizzabases/newtask", tags=["dron", "PizzaBase"])
def get_new_task_from_pizzabase() -> Dict[str, Any]:
    if settings.dron is None:
        return {"code": 400, "message": "There is no dron"}
    with httpx.Client() as client:
        response = client.get(settings.PIZZABASE_URL + "/pizzabases/newtask/")
        dat = response.json()
        if response.status_code != 200 and dat.get("code") is None:
            return {"code": response.status_code, "message": dat}
        if dat.get("message") == "There is no more tasks":
            # flying to the PizzaBase
            settings.dron.next_coordinates = (0, 0)
            settings.dron.fuel -= settings.dron.distance_to_base
            settings.dron.coordinates = (0, 0)
            settings.dron.distance_to_base = 0
            return {"code": 200, "message": f"Oreders finished"}

        settings.task = PizzaTask(**dat)

    define_next_coordinate(settings.dron, settings.task)
    if settings.dron.next_coordinates == (0, 0):
        # flying to the PizzaBase
        settings.dron.fuel -= settings.dron.distance_to_base
        settings.dron.coordinates = (0, 0)

        # refueling
        settings.dron.fuel = 20

        # defying new coordinates
        define_next_coordinate(settings.dron, settings.task)

    # flying to the point
    settings.dron.fuel -= settings.task.fuel_destination
    result = {"code": 200,
              "message": f"Oreder {settings.task.order_id} has been completed"}

    return result
