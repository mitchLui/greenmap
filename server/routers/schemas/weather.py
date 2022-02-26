from pydantic import BaseModel
from .common import Coordinates, Response


class WeatherRequest(Coordinates):
    pass


class WeatherDataResponse(BaseModel):
    temp: float
    aqi: float
    humidity: float
    icon_url: str
    description: str
    description_detailed: str
    timestamp: str

class WeatherResponse(Response):
    data: WeatherDataResponse
