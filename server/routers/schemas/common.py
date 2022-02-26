from sre_constants import SUCCESS
from pydantic import BaseModel

class Coordinates(BaseModel):
    lat: float
    long: float

class Response(BaseModel):
    data: dict
    message: str
    success: bool