from lib2to3.pytree import Base
from wsgiref.validate import validator
from pydantic import BaseModel
from typing import List, Optional
from .common import Response

class NavigationRequest(BaseModel):
    src_long: float
    src_lat: float
    dest_long: float
    dest_lat: float

class Leg(BaseModel):
    mode: str
    path: List[List[int]]
    cost: Optional[float] = None
    distance: float

    @validator("path")
    def path_validator(cls, v):
        for u in v:
            if len(u) != 2:
                raise ValueError("Path must have 2 values")

class Route(BaseModel):
    time: float
    emissions: float
    distance: float
    legs: List[Leg]

class Routes(BaseModel):
    routes: List[Route]

class NavigationResponse(Response):
    data: Routes