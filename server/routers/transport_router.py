from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from datetime import datetime

from .internal.chargers import ChargingService
from .internal.voi import VoiService
from .internal.public_transport import PublicTransportService
from .schemas.transport import TransportRequest, TransportResponse

router = APIRouter(
    prefix="/transport",
    tags=["transport"],
    responses = {
        404: {"description": "Not found"},
    }   
)

public_transport_service = PublicTransportService("TRANSPORTAPIAPPID", "TRANSPORTAPIAPPKEY")
voi_service = VoiService(api_app_keyname="voi", api_key_keyname="voi")
ev_charger_service = ChargingService("CHARGERAPIAPPKEY")

@router.get("/", response_model=TransportResponse)
async def get_transport(request: TransportRequest = Depends()):
    train_station_data = public_transport_service.get_train_stations(request.lat, request.long)
    bus_station_data = public_transport_service.get_bus_stations(request.lat, request.long)
    ev_charger_data = ev_charger_service.get_chargers(request.lat, request.long, request.radius)
    data = {
        "train_stations": train_station_data,
        "bus_stations": bus_station_data,
        "ev_chargers": ev_charger_data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return JSONResponse({
        "data": data,
        "message": "Got data for {}, {}".format(request.lat, request.long),
        "success": True
    }, 200)