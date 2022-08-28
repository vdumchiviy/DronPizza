from fastapi import APIRouter

from api.v1.endpoints import (
    dron,
    pizzabase
)


api_router = APIRouter()
api_router.include_router(router=dron.router)

api_pizzabase_router = APIRouter()
api_pizzabase_router.include_router(router=pizzabase.router)
