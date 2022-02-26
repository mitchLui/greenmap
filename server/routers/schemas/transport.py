from lib2to3.pytree import Base
from pydantic import BaseModel
from typing import List
from .common import Coordinates, Response

class TransportRequest(Coordinates):
    radius: float

class VehicleData(Coordinates):
    available: int

class TransportDataResponse(BaseModel):
    zipcars: List[Coordinates]
    vois: List[VehicleData]
    trains: List[Coordinates]
    bus_stns: List[Coordinates]
    bicycles: List[VehicleData]


class TransportResponse(Response):
    data: TransportDataResponse