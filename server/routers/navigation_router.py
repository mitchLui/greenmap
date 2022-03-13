from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse


from .internal.recommended_routes import RecommendedRoutesService
from .schemas.navigation import NavigationRequest, NavigationResponse

import json

router = APIRouter(
    prefix="/navigation",
    tags=["navigation"],
    responses = {
        404: {"description": "Not found"},
    }   
)

rrs = RecommendedRoutesService()

def cache():
    with open("./routers/cache.json", "r") as file:
        return json.load(file)


@router.get("/", response_model=NavigationResponse)
async def get_navigation(request: NavigationRequest = Depends()):
    try:
        #TODO REMOVE AT SOME POINT
        if request.src_long==-2.6027 and request.src_lat==51.4545 and request.dest_long==-2.6220 and request.dest_lat==51.4637:
            recommended_routes = cache()
        else:
            recommended_routes = rrs.get_recommend_routes(request.src_lat, request.src_long, request.dest_lat, request.dest_long)
        #TODO END
        return JSONResponse({
            "data": recommended_routes,
            "message": f"Got data for directions from {request.src_lat}, {request.src_long} to {request.dest_lat}, {request.dest_long}",
            "success": True
        }, 200)
    except Exception as e:
        return JSONResponse({
            "data": {},
            "message": f"Failed to get data - {e}",
            "success": False
        }, 200)
