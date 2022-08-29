from typing import Any, Dict, Optional, Tuple
from pydantic import BaseModel, Field


class Dron(BaseModel):
    pk: int = Field(gte=0, lte=0, default=0)
    name: Optional[str]
    coordinates: Optional[Tuple[int, int]] = (0, 0)
    fuel: Optional[int] = 25
    distance_to_base = 0
    next_coordinates: Optional[Tuple[int, int]] = (0, 0)


class DronOut(Dron):
    pk: int
