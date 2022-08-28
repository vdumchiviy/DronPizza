from fastapi import FastAPI
from api.v1.api import api_pizzabase_router

app_pizzabase = FastAPI()
app_pizzabase.include_router(api_pizzabase_router, prefix="/api/v1")



@app_pizzabase.get('/')
def home_page():
    return {"message": "PizzaBase"}
