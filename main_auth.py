from api.v1.api import api_auth_router
from fastapi import FastAPI, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.auth import Auth

security = HTTPBearer()
auth_hadler = Auth()


app_auth = FastAPI()
app_auth.include_router(api_auth_router, prefix="/api/v1")

@app_auth.get('/')
def home_page():
    return {"message": "Auth"}
