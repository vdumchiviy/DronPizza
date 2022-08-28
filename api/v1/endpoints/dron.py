from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter
from schemas.dron import Dron, DronOut
from utils import settings

router = APIRouter()


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
def get_drone_coordinates() -> Union[int, Dict[str, Any]]:
    if settings.dron is not None:
        return settings.dron.coordinates
    else:
        return {"code": 404, "message": f"Dron not found"}
