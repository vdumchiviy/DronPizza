from typing import Any, Dict, List, Optional
from schemas.auth import UserDron
from schemas.dron import Dron
from schemas.pizzabase import PizzaTask


PIZZABASE_URL = "http://127.0.0.1:8000/api/v1"
DRON_URL = "http://127.0.0.1:8001/api/v1"
AUTH_URL = "http://127.0.0.1:8008/api/v1"


dron: Optional[Dron] = None
dron_data: Optional[Dict[str, Any]] = None

task: Optional[PizzaTask] = None

auth_base: Optional[List[UserDron]] = list()
