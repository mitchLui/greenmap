from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from .schemas.navigation import NavigationRequest, NavigationResponse

router = APIRouter(
    prefix="/navigation",
    tags=["navigation"],
    responses = {
        404: {"description": "Not found"},
    }   
)


@router.get("/", response_model=NavigationResponse)
async def get_navigation(request: NavigationRequest = Depends()):
    try:
        return JSONResponse({
            "data": {
                "message": "Got data for {}, {}".format(request.src_long, request.src_lat)
            },
            "message": "Got data for {}, {}".format(request.src_long, request.src_lat),
            "success": True
        }, 200)
    except Exception as e:
        return JSONResponse({
            "data": {},
            "message": f"Failed to get data - {e}",
            "success": False
        }, 200)
