from sre_constants import SUCCESS
from pydantic import BaseModel

class Coordinates(BaseModel):
    long: float
    lat: float

class Response(BaseModel):
    data: dict
    message: str
    success: bool