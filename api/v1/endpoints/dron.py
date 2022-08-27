from typing import List, Optional
from fastapi import APIRouter
from schemas.dron import Dron, DronOut

router = APIRouter()


@router.get(path="/drons", tags=["dron"])
def get_drons(
) -> List[Dron]:
    return [Dron]


@router.post(path="/drons", tags=["dron"], response_model=DronOut)
def create_dron(
    name: str,
    fuel: int
) -> Dron:
    dron = Dron(name=name, fuel=fuel)
    print(dron)

    result = DronOut(**dron.dict())
    print(result)
    return result


@router.get(path="/dron/{name}}", tags="dron")
def get_drone(
    name: str
) -> Dron:
    return Dron(name=name)
