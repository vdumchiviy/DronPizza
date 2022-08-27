from fastapi import APIRouter

from api.v1.endpoints import (dron)

api_router = APIRouter()
api_router.include_router(router=dron.router)
