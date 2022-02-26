from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from .internal.weather import WeatherService
from .schemas.weather import WeatherRequest, WeatherResponse

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
    responses = {
        404: {"description": "Not found"},
    }   
)

weather_service = WeatherService(api_app_keyname="weather", api_key_keyname="3a03cb7ea3b729fd6424a566b1fff900")

@router.get("/", response_model=WeatherResponse)
async def get_weather(params: WeatherRequest = Depends()):
    return JSONResponse({
        "data": {
            "temp": 69.69,
            "aqi": 69.69,
            "humidity": 69.69
        },
        "message": "weather at BS8 13:13:lol",
        "success": True
    }, 200)