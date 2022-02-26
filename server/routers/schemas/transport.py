from pydantic import BaseModel
from typing import List
from .common import Coordinates, Response

class TransportRequest(Coordinates):
    radius: float

class VehicleData(Coordinates):
    available: int

class TrainStationData(Coordinates):
    distance: float

class BusStationData(Coordinates):
    distance: float

class TransportDataResponse(BaseModel):
    zipcars: List[Coordinates]
    vois: List[VehicleData]
    trains: List[TrainStationData]
    bus_stns: List[Coordinates]
    bicycles: List[VehicleData]
    timestamp: str


class TransportResponse(Response):
    data: TransportDataResponse