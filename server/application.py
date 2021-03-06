import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routers import weather_router
from routers import transport_router
from routers import navigation_router

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(weather_router.router)
app.include_router(transport_router.router)
app.include_router(navigation_router.router)


@app.get("/")
def app_root() -> JSONResponse:
    return JSONResponse(content={"message": "app is running"}, status_code=200)


if __name__ == "__main__":
    uvicorn.run("application:app", host="localhost", port=8080, reload=True)
