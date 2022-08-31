# DronPizza
## _Automated pizzeria with dron delivery_

[![Build status](https://github.com/vdumchiviy/dronpizza/actions/workflows/checks.yml/badge.svg?branch=develop)](https://github.com/vdumchiviy/dronpizza/actions/workflows/checks.yml)
---


### Steps:
##### 1. Designing microservice architecture
##### 2. Decomposition
##### 3. Prototype without authorization and async
#### **4. Prototype with authorization** (current step)
##### 5. Full tests coverage
##### 6. Pre-prod (add real world to app)
##### 7. Prod
---

## Description:
Create a backend service to calculate routes for a small pizza chain that recently purchased one drone to deliver their pizzas. 

Drone range is 25 miles and must come back to the store for a new battery before it runs out.
The drone will reach out to your backend service to receive its next destination in GPS coordinates. The drone will only request the next destination once it is ready to leave the pizza store, or once it has reached a previously commanded destination and made a delivery.

Assumptions:
- Assume the only requirement to come back to the Pizza store is to get new batteries (Infinite Pizza storage capacity).
- Assume the drone has a constant and stable internet connection.
- You cannot send direct commands to the drone, but you may assume that another service exists which will provide you with any information you may need about the drone (example: remaining range, current location, etc).

Expected functionality:
1. Given a CSV file with order time and delivery address, calculate the optimal path (you are free to define what “optimal path” means to you).
2. Provide a HTTP GET endpoint that will send the drone its next destination in GPS coordinates upon request. Remember, the drone will only reach out to your backend service to get the next destination once it has completed its previous destination or when it’s ready to leave the pizza store.
3. The drone will reach out to your backend service with a set username and password to authenticate itself. Your backend service must authenticate the drone and provide it with a token that it can use to authorize all subsequent requests to your REST API. This token must be validated before providing the drone any data. The token must expire 1 hour after being issued and the drone must request to refresh the token or obtain a new one.

You are welcome to implement any additional functionality you think is important for this scenario.

## Tech:
- Python 3.8.10
- FastAPI
- PyJWT + passlib
- csv
- Pytest + httpx
- Pydantic
- flake8
- mypy

## Features
There are 3 microservices: 
- Auth
- Dron
- PizzaBase

Using Dron you should create a new dron (it couses automatical registration and logging in Auth Service). Using Dron's endpoint ".../drons/pizzabases/newtask" Dron will get a new task from PizzaBase endpoint using credentials from Auth Service. 
Access Token expired in 60 sec.
Refresh Token expires in 24 hours.



## Installation
Using ```pip install -r requirements.txt``` install the requirements:
```anyio==3.6.1
asgiref==3.5.2
atomicwrites==1.4.1
attrs==22.1.0
bcrypt==4.0.0
certifi==2022.6.15
cffi==1.15.1
charset-normalizer==2.1.1
click==8.1.3
colorama==0.4.5
cryptography==37.0.4
dnspython==2.2.1
email-validator==1.2.1
fastapi==0.80.0
flake8==5.0.4
greenlet==1.1.3
h11==0.12.0
httpcore==0.15.0
httptools==0.4.0
httpx==0.23.0
idna==3.3
iniconfig==1.1.1
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.1
mccabe==0.7.0
mypy==0.971
mypy-extensions==0.4.3
orjson==3.8.0
packaging==21.3
passlib==1.7.4
pluggy==1.0.0
py==1.11.0
pycodestyle==2.9.1
pycparser==2.21
pydantic==1.9.2
pyflakes==2.5.0
PyJWT==2.4.0
pyparsing==3.0.9
pytest==7.1.2
python-dotenv==0.20.0
python-multipart==0.0.5
PyYAML==6.0
requests==2.28.1
rfc3986==1.5.0
six==1.16.0
sniffio==1.2.0
starlette==0.19.1
tomli==2.0.1
typing_extensions==4.3.0
ujson==5.4.0
urllib3==1.26.12
uvicorn==0.17.6
watchgod==0.8.2
websockets==10.3
```

## Run
According to utils/config.py there are ip's assigned to microservices:

| Microservice | IP                               |
| ------------ | -------------------------------- |
| Auth         | http://127.0.0.1:**8008**/api/v1 |
| PizzaBase    | http://127.0.0.1:**8000**/api/v1 |
| Dron         | http://127.0.0.1:**8001**/api/v1 |

## License
**Free Software**
