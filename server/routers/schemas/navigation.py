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
    src: Optional[str] = None
    dest: Optional[str] = None
    dep_time: Optional[str] = None
    arr_time: Optional[str] = None
    line: Optional[str] = None

class Route(BaseModel):
    dep_time: str
    arr_time: str
    time: float
    emissions: float
    distance: float
    legs: List[Leg]

class Routes(BaseModel):
    routes: List[Route]

class NavigationResponse(Response):
    data: Routes