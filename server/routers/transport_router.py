from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, wait
from traceback import format_exc
from loguru import logger
from sqlalchemy import JSON

from .internal.chargers import ChargingService
from .internal.voi import VoiService
from .internal.public_transport import PublicTransportService
from .internal.santander_cycles import SantanderCycles
from .schemas.transport import TransportRequest, TransportResponse

router = APIRouter(
    prefix="/transport",
    tags=["transport"],
    responses = {
        404: {"description": "Not found"},
    }   
)

public_transport_service = PublicTransportService("TRANSPORTAPIAPPID", "TRANSPORTAPIAPPKEY")
voi_service = VoiService("VOIAPIAUTHTOCKEN")
ev_charger_service = ChargingService("CHARGERAPIAPPKEY")
santander_cycles_service = SantanderCycles()

@router.get("/", response_model=TransportResponse)
async def get_transport(request: TransportRequest = Depends()):
    try:
        with ThreadPoolExecutor(max_workers=4) as e:
            jobs = [
                e.submit(public_transport_service.get_train_stations, request.lat, request.long),
                e.submit(public_transport_service.get_bus_stations, request.lat, request.long),
                e.submit(ev_charger_service.get_chargers, request.lat, request.long, request.radius),
                e.submit(santander_cycles_service.get_cycles, request.lat, request.long, request.radius),
            ]
            futures, _ = wait(jobs)
            futures = list(futures)
            train_station_data = futures[0].result()
            bus_station_data = futures[1].result()
            ev_charger_data = futures[2].result()
            santander_cycles_data = futures[3].result()
            data = {
                "train_stations": train_station_data,
                "bus_stations": bus_station_data,
                "ev_chargers": ev_charger_data,
                "santander_cycles": santander_cycles_data,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return JSONResponse({
                "data": data,
                "message": "Got data for {}, {}".format(request.lat, request.long),
                "success": True
            }, 200)
    except Exception as e:
        logger.error(e)
        logger.error(format_exc())
        return JSONResponse({
            "data": {},
            "message": f"Failed to get data - {e}",
            "success": False
        }, 500)