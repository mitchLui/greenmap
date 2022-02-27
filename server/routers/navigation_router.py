from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse


from .internal.recommended_routes import RecommendedRoutesService
from .schemas.navigation import NavigationRequest, NavigationResponse

router = APIRouter(
    prefix="/navigation",
    tags=["navigation"],
    responses = {
        404: {"description": "Not found"},
    }   
)

rrs = RecommendedRoutesService()


@router.get("/", response_model=NavigationResponse)
async def get_navigation(request: NavigationRequest = Depends()):
    try:
        recommended_routes = rrs.get_recommend_routes(request.src_lat, request.src_long, request.dest_lat, request.dest_long)
        return JSONResponse({
            "data": {
                "routes": recommended_routes
            },
            "message": f"Got data for directions from {request.src_lat}, {request.src_long} to {request.dest_lat}, {request.dest_long}",
            "success": True
        }, 200)
    except Exception as e:
        return JSONResponse({
            "data": {},
            "message": f"Failed to get data - {e}",
            "success": False
        }, 200)
