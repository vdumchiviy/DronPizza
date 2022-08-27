from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class Dron(BaseModel):
    pk: int = Field(gte=0, lte=0, default=0)
    name: Optional[str]
    coordinates: Optional[Dict[str, Any]]
    fuel: Optional[int] = 20


class DronOut(Dron):
    pk: int
