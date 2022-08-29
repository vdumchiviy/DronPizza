from pydantic import BaseModel, Field


class UserDron(BaseModel):
    pk: int = Field(gte=0, lte=0, default=0)
    name: str
    hashed_password: str
