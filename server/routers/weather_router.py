from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from .internal.weather import Weather
from .schemas.weather import WeatherRequest, WeatherResponse

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
    responses = {
        404: {"description": "Not found"},
    }   
)

weater = Weather()

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