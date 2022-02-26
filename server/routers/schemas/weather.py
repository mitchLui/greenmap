from pydantic import BaseModel
from .common import Coordinates, Response


class WeatherRequest(Coordinates):
    radius: float


class WeatherDataResponse(BaseModel):
    temp: float
    api: float
    humidity: float


class WeatherResponse(Response):
    data: WeatherDataResponse
