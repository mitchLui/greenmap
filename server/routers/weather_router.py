from datetime import datetime
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

weather_service = WeatherService(api_app_keyname = "weather", api_key_keyname="OPENWEATHERAPIKEY")

@router.get("/", response_model=WeatherResponse)
async def get_weather(params: WeatherRequest = Depends()):
    return JSONResponse({
        "data": {
            "temp": 7,
            "aqi": 41,
            "humidity": 81,
            "icon_url": "http://openweathermap.org/img/wn/01d@2x.png",
            "description": "Clear",
            "description_detailed": "clear sky",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "message": "got weather",
        "success": True
    }, 200)
    """
    data, status_code = weather_service.get_weather(params.long, params.lat)
    if status_code == 200:
        message = f"Got data for {params.long}, {params.lat}"
        success = True
    else:
        message = data["message"]
        success = False
    return JSONResponse({
        "data": data,
        "message": message,
        "success": success
    }, status_code)
    """