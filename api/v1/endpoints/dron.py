from typing import Any, Dict, List, Tuple, Union
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
    settings.dron_data = {"login": name, "password": name + "12345"}
    with httpx.Client() as client:
        # Signing in
        response = client.post(
            url=settings.AUTH_URL + "/userdrons/signin",
            json=settings.dron_data,
            timeout=120
        )
        if response.status_code != 200:
            raise ValueError("Dron didn't authorized")
        resp = response.json()
        settings.dron_data["hashed_password"] = resp["hashed_password"]

        # Logging in
        response = client.post(
            url=settings.AUTH_URL + "/userdrons/login",
            json=settings.dron_data,
            timeout=120
        )
        if response.status_code != 200:
            raise ValueError("Dron didn't logged in")
        resp = response.json()
        settings.dron_data["access_token"] = resp["access_token"]
        settings.dron_data["refresh_token"] = resp["refresh_token"]

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


@router.get(path="/drons/coordinates", tags=["dron"])
def get_drone_coordinates() -> Union[Tuple[int, int], Dict[str, Any]]:
    if settings.dron is None:
        return {"code": 404, "message": f"Dron not found"}

    return settings.dron.coordinates


@router.get(path="/drons/pizzabases/newtask", tags=["dron", "PizzaBase"])
def get_new_task_from_pizzabase() -> Dict[str, Any]:
    if settings.dron is None:
        return {"code": 400, "message": "There is no dron"}
    headers = {'Authorization': 'Bearer {0}'.format(
        settings.dron_data["access_token"])}

    with httpx.Client() as client:
        response = client.get(
            url=settings.PIZZABASE_URL + "/pizzabases/newtask",
            headers=headers,
            timeout=120)
        dat = response.json()
        if response.status_code != 200:
            return {"code": response.status_code, "message": dat}

        if dat.get("message") == "Token expired":
            # refresh access token and get new task again
            headers = {'Authorization': 'Bearer {0}'.format(
                settings.dron_data["refresh_token"])}
            response = client.get(
                url=settings.AUTH_URL + "/userdrons/refresh_token",
                headers=headers,
                timeout=120)
            dat = response.json()
            if response.status_code != 200:
                return {"code": response.status_code, "message": dat}
            if dat.get("access_token") is not None:
                settings.dron_data["access_token"] = dat["access_token"]

            headers = {'Authorization': 'Bearer {0}'.format(
                settings.dron_data["access_token"])}
            response = client.get(
                url=settings.PIZZABASE_URL + "/pizzabases/newtask",
                headers=headers,
                timeout=120)
            dat = response.json()
            if response.status_code != 200:
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
