from typing import Any, Dict
from fastapi import FastAPI
from api.v1.api import api_router

appdron = FastAPI()
appdron.include_router(api_router, prefix="/api/v1")

appmain = FastAPI()


@appmain.get('/')
def home_page() -> Dict[str, Any]:
    return {"message": "It works!"}
