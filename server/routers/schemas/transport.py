from pydantic import BaseModel
from typing import List, Optional
from .common import Coordinates, Response

class TransportRequest(Coordinates):
    radius: float


class ScooterData(BaseModel):
    reg: str
    battery: int
    lat: float
    long: float
    start_price: Optional[float] = None
    minute_cost: Optional[float] = None

class VoiData(Coordinates):
    vehicles: List[ScooterData]

class TierData(Coordinates):
    vehicles: List[ScooterData]

class TrainStationData(Coordinates):
    name: str
    distance: float

class BusStationData(Coordinates):
    name: str
    distance: float

class SantanderBikesData(Coordinates):
    name: str
    distance: float
    bikes: int
    spaces: int
    cost: float

class TransportDataResponse(BaseModel):
    vois: List[VoiData]
    tiers: List[TierData]
    trains: List[TrainStationData]
    bus_stns: List[BusStationData]
    cycles: List[SantanderBikesData]
    timestamp: str


class TransportResponse(Response):
    data: TransportDataResponse