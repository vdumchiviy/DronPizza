from pydantic import BaseModel, Field


class PizzaTask(BaseModel):
    order_id: int
    fuel_destination: int
    pizza_amount: int


class PizzaBase(BaseModel):
    pk: int = Field(default=0, gte=0, lte=0)
    name: str
    fuel_amount: int = 1000
